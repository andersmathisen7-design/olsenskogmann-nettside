// Eiersiden (/admin/): henvendelser fra nettsiden og telefon, med status, notat og tall.
// Data ligger i Google-arket (henvendelser/henvendelser.gs). Samme innlogging som eiersiden til Follo Bjørkeved.
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var A = {};
  try { A = JSON.parse($("admin-cfg").textContent); } catch (e) {}
  var KEY = "osAdminToken", token = "";
  var store = {
    get: function () { try { return sessionStorage.getItem(KEY) || localStorage.getItem(KEY) || ""; } catch (e) { return token; } },
    set: function (t, remember) { token = t; try { (remember ? localStorage : sessionStorage).setItem(KEY, t); } catch (e) {} },
    clear: function () { token = ""; try { localStorage.removeItem(KEY); sessionStorage.removeItem(KEY); } catch (e) {} }
  };
  token = store.get();
  var leads = [], statuses = ["Ny", "Kontaktet", "Befaring", "Tilbud sendt", "Vunnet", "Tapt"], view = "aktive";
  var ACTIVE = ["Ny", "Kontaktet", "Befaring", "Tilbud sendt"], CLOSED = ["Vunnet", "Tapt"];

  if (!A.leadsUrl) { $("a-nocal").hidden = false; return; }

  var esc = function (s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  };
  var ERR = {
    passord: "Feil passord.", sperret: "For mange feil forsøk. Vent 15 minutter og prøv igjen.",
    "ikke-satt-opp": "Passordet er ikke laget ennå. Åpne regnearket og velg Henvendelser → Lag nytt passord til eiersiden.",
    token: "Du er logget ut. Logg inn igjen."
  };
  // «2026-10-17 10:15» → Date (lokal tid).
  var parse = function (s) {
    var m = /^(\d{4})-(\d{2})-(\d{2})(?: (\d{2}):(\d{2}))?/.exec(s || "");
    return m ? new Date(+m[1], +m[2] - 1, +m[3], +(m[4] || 0), +(m[5] || 0)) : null;
  };
  var ago = function (d) {
    if (!d) return "";
    var h = (Date.now() - d.getTime()) / 36e5;
    if (h < 1) return "nå nettopp";
    if (h < 24) return Math.floor(h) + " t siden";
    var days = Math.floor(h / 24);
    return days + (days === 1 ? " dag" : " dager") + " siden";
  };
  var kr = function (v) {
    var n = parseInt(String(v).replace(/[^\d]/g, ""), 10);
    return isNaN(n) ? 0 : n;
  };

  function post(body) {
    if (body.action !== "login") body.token = token;
    return fetch(A.leadsUrl, {
      method: "POST", headers: { "Content-Type": "text/plain;charset=utf-8" }, body: JSON.stringify(body)
    }).then(function (r) { return r.json(); });
  }

  function showLogin(msg) {
    $("a-app").hidden = true; $("a-actions").hidden = true; $("a-login").hidden = false;
    $("a-login-msg").textContent = msg || "";
    $("a-key").focus();
  }

  function load() {
    $("a-updated").textContent = "Henter …";
    return post({ action: "list" }).then(function (j) {
      if (!j.ok) { store.clear(); return showLogin(ERR[j.error] || "Noe gikk galt: " + (j.error || "ukjent")); }
      leads = j.leads || []; statuses = j.statuses || statuses;
      $("a-login").hidden = true; $("a-app").hidden = false; $("a-actions").hidden = false;
      $("a-updated").textContent = "Oppdatert " + new Date().toLocaleTimeString("nb-NO", { hour: "2-digit", minute: "2-digit" });
      render();
    }).catch(function () { $("a-updated").textContent = "Fikk ikke kontakt med arket. Prøv Oppdater."; });
  }

  // ---------------------------------------------------------------- tall
  function stats() {
    var now = Date.now(), d30 = now - 30 * 864e5, d90 = now - 90 * 864e5;
    var last30 = leads.filter(function (l) { var d = parse(l.registered); return d && d.getTime() >= d30; });
    var closed90 = leads.filter(function (l) { var d = parse(l.updated) || parse(l.registered); return CLOSED.indexOf(l.status) >= 0 && d && d.getTime() >= d90; });
    var won90 = closed90.filter(function (l) { return l.status === "Vunnet"; });
    var nye = leads.filter(function (l) { return l.status === "Ny"; });
    var late = nye.filter(function (l) { var d = parse(l.registered); return d && now - d.getTime() > 24 * 36e5; });
    var work = leads.filter(function (l) { return ["Kontaktet", "Befaring", "Tilbud sendt"].indexOf(l.status) >= 0; });
    var tile = function (n, label, warn) {
      return '<div class="tile' + (warn ? " warn" : "") + '"><strong>' + n + "</strong><span>" + label + "</span></div>";
    };
    $("a-stats").innerHTML =
      tile(nye.length, late.length ? "nye, " + late.length + " eldre enn 1 døgn" : "nye", late.length > 0) +
      tile(work.length, "under arbeid") +
      tile(last30.length, "henvendelser siste 30 dager") +
      tile(closed90.length ? Math.round(won90.length / closed90.length * 100) + " %" : "–", "vunnet av avsluttede (90 dager)") +
      tile(won90.reduce(function (s, l) { return s + kr(l.value); }, 0).toLocaleString("nb-NO") + " kr", "vunnet verdi (90 dager)");

    // Per tjeneste og per kilde, siste 90 dager.
    var group = function (key) {
      var m = {};
      leads.forEach(function (l) {
        var d = parse(l.registered);
        if (!d || d.getTime() < d90) return;
        var k = key(l) || "Ukjent";
        m[k] = m[k] || { n: 0, won: 0 };
        m[k].n++; if (l.status === "Vunnet") m[k].won++;
      });
      return Object.keys(m).sort(function (a, b) { return m[b].n - m[a].n; }).map(function (k) {
        return "<tr><td>" + esc(k) + "</td><td>" + m[k].n + "</td><td>" + m[k].won + "</td></tr>";
      }).join("") || '<tr><td colspan="3" class="muted">Ingen ennå</td></tr>';
    };
    var src = function (l) {
      var s = (l.source || "").split(" → ")[0];
      if (/google/.test(s)) return "Google";
      if (/bing|duckduckgo/.test(s)) return "Bing/DuckDuckGo";
      if (/chatgpt|openai|perplexity|copilot|gemini/.test(s)) return "KI-søk";
      if (/facebook|instagram/.test(s)) return "Facebook/Instagram";
      if (/mittanbud/.test(s)) return "Mittanbud";
      return s || "Ukjent";
    };
    $("a-breakdown").innerHTML =
      '<div class="table-card"><h3>Per tjeneste</h3><table><thead><tr><th>Tjeneste</th><th>Henv.</th><th>Vunnet</th></tr></thead><tbody>' + group(function (l) { return l.service; }) + "</tbody></table></div>" +
      '<div class="table-card"><h3>Per kilde</h3><table><thead><tr><th>Kilde</th><th>Henv.</th><th>Vunnet</th></tr></thead><tbody>' + group(src) + "</tbody></table></div>";
  }

  // ---------------------------------------------------------------- liste
  function render() {
    stats();
    var list = leads.filter(function (l) {
      return view === "aktive" ? ACTIVE.indexOf(l.status) >= 0 : view === "avsluttet" ? CLOSED.indexOf(l.status) >= 0 : true;
    });
    var rank = {}; statuses.forEach(function (s, i) { rank[s] = i; });
    list.sort(function (a, b) {
      return view === "aktive" ? (rank[a.status] - rank[b.status]) || (a.registered < b.registered ? -1 : 1)
        : (a.registered < b.registered ? 1 : -1);
    });
    if (!list.length) {
      $("a-list").innerHTML = '<p class="admin-empty">' + (view === "aktive" ? "Ingen åpne henvendelser. Bra jobba!" : "Ingen henvendelser her ennå.") + "</p>";
      return;
    }
    $("a-list").innerHTML = list.map(card).join("");
  }

  function card(l) {
    var d = parse(l.registered), late = l.status === "Ny" && d && Date.now() - d.getTime() > 24 * 36e5;
    var maps = "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(l.address + ", Oslo");
    var tel = l.phone.replace(/[^\d+]/g, "");
    var btns = statuses.map(function (s) {
      return '<button type="button" class="chip' + (l.status === s ? " on" : "") + '" data-id="' + esc(l.id) + '" data-status="' + esc(s) + '"' +
        (l.status === s ? " disabled" : "") + ">" + esc(s) + "</button>";
    }).join("");
    return '<article class="lead st-' + esc(l.status.toLowerCase().replace(/\s+/g, "-")) + (late ? " late" : "") + '">' +
      '<div class="lead-head"><strong>' + esc(l.name || l.phone || "(uten navn)") + '</strong><span class="pill">' + esc(l.service || "Ukjent") + "</span></div>" +
      '<p class="lead-meta">' + esc(l.registered) + " · " + esc(ago(d)) + (late ? ' · <span class="warn-text">ikke kontaktet</span>' : "") + "</p>" +
      '<p class="lead-contact">' +
        (tel ? '<a href="tel:' + esc(tel) + '">Ring ' + esc(l.phone) + '</a><a href="sms:' + esc(tel) + '">SMS</a>' : "") +
        (l.address ? '<a href="' + maps + '" target="_blank" rel="noopener">Kart: ' + esc(l.address) + "</a>" : "") + "</p>" +
      (l.message ? '<p class="lead-msg">' + esc(l.message) + "</p>" : "") +
      '<p class="lead-src">Kilde: ' + esc(l.source || "ukjent") + "</p>" +
      '<div class="chips" role="group" aria-label="Status">' + btns + "</div>" +
      '<form class="lead-note" data-id="' + esc(l.id) + '">' +
        '<label>Notat<input name="note" value="' + esc(l.note) + '" maxlength="500" placeholder="F.eks. befaring tirsdag kl. 16"></label>' +
        '<label>Verdi (kr)<input name="value" value="' + esc(l.value) + '" inputmode="numeric" maxlength="40" placeholder="Tilbud/faktura"></label>' +
        '<button type="submit" class="btn btn-sm">Lagre</button></form>' +
      "</article>";
  }

  $("a-list").addEventListener("click", function (e) {
    var b = e.target.closest("button[data-status]");
    if (!b) return;
    b.disabled = true; b.textContent = "Lagrer …";
    post({ action: "status", id: b.dataset.id, status: b.dataset.status }).then(function (j) {
      if (!j.ok) alert(ERR[j.error] || "Kunne ikke lagre: " + (j.error || "ukjent feil"));
      return load();
    }).catch(function () { alert("Fikk ikke kontakt med arket."); load(); });
  });
  $("a-list").addEventListener("submit", function (e) {
    var f = e.target.closest(".lead-note");
    if (!f) return;
    e.preventDefault();
    var btn = f.querySelector("button"); btn.disabled = true; btn.textContent = "Lagrer …";
    post({ action: "note", id: f.dataset.id, note: f.elements.note.value.trim(), value: f.elements.value.value.trim() })
      .then(function (j) { if (!j.ok) alert(ERR[j.error] || "Kunne ikke lagre."); return load(); })
      .catch(function () { alert("Fikk ikke kontakt med arket."); load(); });
  });

  document.querySelectorAll(".admin-tabs button").forEach(function (b) {
    b.addEventListener("click", function () {
      view = b.dataset.view;
      document.querySelectorAll(".admin-tabs button").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      render();
    });
  });

  $("a-login").addEventListener("submit", function (e) {
    e.preventDefault();
    var pw = $("a-key").value.trim(), remember = $("a-remember").checked, btn = $("a-login").querySelector("button");
    if (!pw) return;
    btn.disabled = true; $("a-login-msg").textContent = "";
    post({ action: "login", password: pw, remember: remember }).then(function (j) {
      btn.disabled = false;
      if (!j.ok) return showLogin(ERR[j.error] || "Noe gikk galt.");
      $("a-key").value = "";
      store.set(j.token, remember);
      load();
    }).catch(function () { btn.disabled = false; showLogin("Fikk ikke kontakt med arket."); });
  });
  $("a-logout").addEventListener("click", function () {
    post({ action: "logout" }).catch(function () {});
    store.clear(); showLogin();
  });
  $("a-refresh").addEventListener("click", load);

  // Telefonhenvendelse: legges inn som «Kontaktet».
  $("ad-tjeneste").innerHTML = (A.services || []).concat(["Annet"]).map(function (s) { return "<option>" + esc(s) + "</option>"; }).join("");
  $("a-add").addEventListener("submit", function (e) {
    e.preventDefault();
    var msg = $("a-add-msg"), v = function (id) { return $(id).value.trim(); };
    if (!v("ad-tlf") && !v("ad-navn")) { msg.className = "form-msg err"; msg.textContent = "Fyll inn telefon eller navn."; return; }
    msg.className = "form-msg"; msg.textContent = "Lagrer …";
    post({ action: "add", service: $("ad-tjeneste").value, name: v("ad-navn"), phone: v("ad-tlf"),
      address: v("ad-adresse"), message: v("ad-melding"), source: $("ad-kilde").value, page: "" })
      .then(function (j) {
        if (!j.ok) { msg.className = "form-msg err"; msg.textContent = ERR[j.error] || "Kunne ikke lagre."; return; }
        msg.className = "form-msg ok"; msg.textContent = "Lagret.";
        ["ad-navn", "ad-tlf", "ad-adresse", "ad-melding"].forEach(function (id) { $(id).value = ""; });
        load();
      }).catch(function () { msg.className = "form-msg err"; msg.textContent = "Fikk ikke kontakt med arket."; });
  });

  if (token) load(); else showLogin();
})();
