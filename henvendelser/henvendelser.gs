/**
 * Olsen Skogmann – henvendelseslogg.
 * Lagrer hver forespørsel fra nettsiden i arket «Henvendelser», og gir eiersiden (/admin/)
 * oversikten: status per henvendelse (ny → kontaktet → befaring → tilbud → vunnet/tapt), notater og tall.
 * Limes inn i Utvidelser → Apps Script i regnearket. Se henvendelser/README.md.
 *
 * Bygget på samme mønster som leveringskalenderen til Follo Bjørkeved.
 * Sikkerhet:
 *  - Passordet til eiersiden lages av skriptet (menyen «Henvendelser» i regnearket) og lagres bare som
 *    en saltet SHA-256-sjekksum i skriptegenskapene. Det står aldri i koden eller i GitHub.
 *  - Eiersiden får en tilfeldig innloggingsbillett som utløper (12 timer, eller 30 dager med «husk meg»).
 *  - Maks 10 feil passord per 15 minutter, deretter stengt i 15 minutter.
 *  - All tekst fra nettsiden lagres som ren tekst, så den aldri kan bli en formel i arket.
 *  - Maks 30 nettforespørsler per time (vern mot søppel).
 *  - Uten innlogging kan man bare legge inn en ny henvendelse – aldri lese noe.
 */

var ARK = "Henvendelser";
var TIDSSONE = "Europe/Oslo";
var KOLONNER = ["ID", "Status", "Tjeneste", "Navn", "Telefon", "Adresse", "Beskrivelse", "Side", "Kilde",
                "Verdi", "Notat", "Registrert", "Oppdatert"];
var STATUSER = ["Ny", "Kontaktet", "Befaring", "Tilbud sendt", "Vunnet", "Tapt"];
var MAKS_NETT_PER_TIME = 30;
var MAKS_FEIL_PASSORD = 10;
var BILLETT_TIMER = 12, BILLETT_HUSK_DAGER = 30;

// ------------------------------------------------------------------ meny i regnearket

function onOpen() {
  SpreadsheetApp.getUi().createMenu("Henvendelser")
    .addItem("Lag nytt passord til eiersiden", "lagNyttPassord")
    .addItem("Logg ut alle enheter", "loggUtAlle")
    .addToUi();
}

function lagNyttPassord() {
  ark_();
  var tegn = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789", pw = "";
  var bytes = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, Utilities.getUuid() + Utilities.getUuid());
  for (var i = 0; i < 20; i++) pw += tegn.charAt((bytes[i] + 256) % tegn.length);
  pw = pw.replace(/(.{5})(?!$)/g, "$1-");
  var salt = Utilities.getUuid();
  var props = PropertiesService.getScriptProperties();
  props.setProperty("pw_salt", salt);
  props.setProperty("pw_hash", sha_(salt + pw));
  slettBilletter_();
  var tekst = "Nytt passord til eiersiden (/admin/):\n\n" + pw +
    "\n\nSkriv det ned eller lagre det i en passordbehandler. Det vises ikke igjen. Alle enheter er logget ut.";
  try { SpreadsheetApp.getUi().alert(tekst); } catch (e) { Logger.log(tekst); }
}

function loggUtAlle() {
  slettBilletter_();
  try { SpreadsheetApp.getUi().alert("Alle enheter er logget ut av eiersiden."); } catch (e) { Logger.log("Alle enheter er logget ut."); }
}

// ------------------------------------------------------------------ hjelpere

function ark_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(ARK);
  if (!sh) {
    sh = ss.insertSheet(ARK);
    sh.appendRow(KOLONNER);
    sh.setFrozenRows(1);
  }
  return sh;
}

function sha_(s) {
  return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, s, Utilities.Charset.UTF_8)
    .map(function (b) { return ("0" + ((b + 256) % 256).toString(16)).slice(-2); }).join("");
}

function likt_(a, b) {
  a = String(a); b = String(b);
  var diff = a.length ^ b.length;
  for (var i = 0; i < Math.max(a.length, b.length); i++) diff |= (a.charCodeAt(i) || 0) ^ (b.charCodeAt(i) || 0);
  return diff === 0;
}

function na_() { return Utilities.formatDate(new Date(), TIDSSONE, "yyyy-MM-dd HH:mm"); }

function tid_(v) {
  return v instanceof Date ? Utilities.formatDate(v, TIDSSONE, "yyyy-MM-dd HH:mm") : String(v || "");
}

// Tekst fra nettsiden: kortes ned og lagres som ren tekst (et ' foran gjør at Sheets aldri tolker den som formel).
function tekst_(v, max) {
  var s = String(v == null ? "" : v).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, "").slice(0, max);
  return /^[=+\-@\t\r]/.test(s) ? "'" + s : s;
}

function svar_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

// ------------------------------------------------------------------ innlogging

function loggInn_(passord, husk) {
  var props = PropertiesService.getScriptProperties(), cache = CacheService.getScriptCache();
  var salt = props.getProperty("pw_salt"), hash = props.getProperty("pw_hash");
  if (!salt || !hash) return { ok: false, error: "ikke-satt-opp" };
  var feil = Number(cache.get("feil_passord")) || 0;
  if (feil >= MAKS_FEIL_PASSORD) return { ok: false, error: "sperret" };
  if (!likt_(sha_(salt + String(passord || "")), hash)) {
    cache.put("feil_passord", String(feil + 1), 15 * 60);
    return { ok: false, error: "passord" };
  }
  ryddBilletter_();
  var billett = (Utilities.getUuid() + Utilities.getUuid()).replace(/-/g, "");
  var utloper = Date.now() + (husk ? BILLETT_HUSK_DAGER * 864e5 : BILLETT_TIMER * 36e5);
  props.setProperty("billett_" + sha_(billett), String(utloper));
  return { ok: true, token: billett, expires: utloper };
}

function gyldigBillett_(billett) {
  if (!billett || String(billett).length < 40) return false;
  var utloper = Number(PropertiesService.getScriptProperties().getProperty("billett_" + sha_(String(billett))));
  return utloper > Date.now();
}

function loggUt_(billett) {
  if (billett) PropertiesService.getScriptProperties().deleteProperty("billett_" + sha_(String(billett)));
}

function ryddBilletter_() {
  var props = PropertiesService.getScriptProperties(), alle = props.getProperties(), na = Date.now();
  Object.keys(alle).forEach(function (k) {
    if (k.indexOf("billett_") === 0 && Number(alle[k]) < na) props.deleteProperty(k);
  });
}

function slettBilletter_() {
  var props = PropertiesService.getScriptProperties(), alle = props.getProperties();
  Object.keys(alle).forEach(function (k) { if (k.indexOf("billett_") === 0) props.deleteProperty(k); });
}

// ------------------------------------------------------------------ henvendelser

// Kolonnene finnes etter navn, så rekkefølgen i arket kan endres. Rader uten ID får «rad-<nummer>».
function henvendelser_() {
  var rows = ark_().getDataRange().getValues(), head = rows[0], out = [];
  var col = function (r, navn) { var i = head.indexOf(navn); return i < 0 ? "" : r[i]; };
  for (var i = 1; i < rows.length; i++) {
    var r = rows[i];
    if (!col(r, "Telefon") && !col(r, "Navn") && !col(r, "Beskrivelse")) continue;
    out.push({
      id: String(col(r, "ID") || "rad-" + (i + 1)), status: String(col(r, "Status") || "Ny"),
      service: String(col(r, "Tjeneste")), name: String(col(r, "Navn")), phone: String(col(r, "Telefon")),
      address: String(col(r, "Adresse")), message: String(col(r, "Beskrivelse")), page: String(col(r, "Side")),
      source: String(col(r, "Kilde")), value: String(col(r, "Verdi")), note: String(col(r, "Notat")),
      registered: tid_(col(r, "Registrert")), updated: tid_(col(r, "Oppdatert"))
    });
  }
  return out;
}

function leggTil_(b, status) {
  var id = Utilities.getUuid().slice(0, 8);
  var verdier = {
    "ID": id, "Status": status, "Tjeneste": tekst_(b.service, 60), "Navn": tekst_(b.name, 80),
    "Telefon": tekst_(b.phone, 30), "Adresse": tekst_(b.address, 120), "Beskrivelse": tekst_(b.message, 1500),
    "Side": tekst_(b.page, 120), "Kilde": tekst_(b.source, 120), "Verdi": "", "Notat": tekst_(b.note, 500),
    "Registrert": new Date(), "Oppdatert": new Date()
  };
  var sh = ark_(), head = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
  sh.appendRow(head.map(function (h) { return h in verdier ? verdier[h] : ""; }));
  return id;
}

// Endrer ett eller flere felt (status, notat, verdi) på én henvendelse.
function endre_(id, felt) {
  var sh = ark_(), rows = sh.getDataRange().getValues(), head = rows[0];
  var iId = head.indexOf("ID");
  for (var i = 1; i < rows.length; i++) {
    var radId = String((iId >= 0 && rows[i][iId]) || "rad-" + (i + 1));
    if (radId !== id) continue;
    Object.keys(felt).forEach(function (navn) {
      var c = head.indexOf(navn);
      if (c >= 0) sh.getRange(i + 1, c + 1).setValue(felt[navn]);
    });
    var u = head.indexOf("Oppdatert");
    if (u >= 0) sh.getRange(i + 1, u + 1).setValue(new Date());
    return { ok: true };
  }
  return { ok: false, error: "fant ikke henvendelsen" };
}

// ------------------------------------------------------------------ nettadressen

function doGet() {
  return svar_({ ok: true });
}

function doPost(e) {
  var b;
  try { b = JSON.parse(e.postData.contents); } catch (err) { return svar_({ ok: false, error: "ugyldig" }); }
  if (!b || typeof b !== "object") return svar_({ ok: false, error: "ugyldig" });

  // Eiersiden.
  if (b.action === "login") return svar_(loggInn_(b.password, b.remember === true));
  if (b.action === "logout") { loggUt_(b.token); return svar_({ ok: true }); }
  if (["list", "status", "note", "add"].indexOf(b.action) >= 0) {
    if (!gyldigBillett_(b.token)) return svar_({ ok: false, error: "token" });
    if (b.action === "list") return svar_({ ok: true, leads: henvendelser_(), now: na_(), statuses: STATUSER });
    if (b.action === "status") {
      if (STATUSER.indexOf(String(b.status)) < 0) return svar_({ ok: false, error: "ugyldig" });
      return svar_(endre_(String(b.id || ""), { "Status": String(b.status) }));
    }
    if (b.action === "note") {
      return svar_(endre_(String(b.id || ""), { "Notat": tekst_(b.note, 500), "Verdi": tekst_(b.value, 40) }));
    }
    if (!(String(b.phone || "").trim() || String(b.name || "").trim())) return svar_({ ok: false, error: "ugyldig" });
    b.source = b.source || "Telefon";
    return svar_({ ok: true, id: leggTil_(b, "Kontaktet") });
  }
  if (b.action) return svar_({ ok: false, error: "ugyldig" });

  // Henvendelse fra skjemaet på nettsiden.
  if (!String(b.phone || "").trim()) return svar_({ ok: false, error: "ugyldig" });
  var lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    var cache = CacheService.getScriptCache(), n = Number(cache.get("nett")) || 0;
    if (n >= MAKS_NETT_PER_TIME) return svar_({ ok: false, error: "travelt" });
    var id = leggTil_(b, "Ny");
    cache.put("nett", String(n + 1), 3600);
    return svar_({ ok: true, id: id });
  } finally {
    lock.releaseLock();
  }
}
