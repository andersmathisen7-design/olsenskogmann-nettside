// Olsen Skogmann – målinger og henvendelseslogg. Siden virker helt uten dette skriptet.
// Hendelser i GoatCounter (hvis slått på i config.py):
//   ring-*, sms-* (klikk på telefon/SMS, satt med data-goatcounter-click i HTML-en)
//   begin_form            – begynte å fylle ut skjemaet
//   form_invalid:<felt>   – trykket Send, men feltet manglet
//   generate_lead         – sendte skjemaet (/takk/ teller også som fullført)
//   lead_tjeneste:<valg>  – hvilken tjeneste forespørselen gjaldt
(function () {
  "use strict";

  function gc(name) {
    try {
      if (window.goatcounter && window.goatcounter.count) {
        window.goatcounter.count({ path: name, title: name, event: true, referrer: location.pathname });
      }
    } catch (e) {}
  }

  // Husk hvor besøket kom fra (første side i økta), så henvendelsen kan knyttes til kilden.
  var SKEY = "osKilde";
  function source() {
    try {
      var s = sessionStorage.getItem(SKEY);
      if (s) return s;
      var p = new URLSearchParams(location.search), utm = p.get("utm_source");
      var ref = document.referrer && document.referrer.indexOf(location.host) < 0 ? new URL(document.referrer).host : "";
      s = utm ? "utm:" + utm + (p.get("utm_campaign") ? "/" + p.get("utm_campaign") : "") : (ref || "direkte");
      s += " → " + location.pathname;
      sessionStorage.setItem(SKEY, s);
      return s;
    } catch (e) { return ""; }
  }
  source();

  var form = document.querySelector(".quote-form");
  if (!form) return;

  var begun = false;
  form.addEventListener("focusin", function () {
    if (!begun) { begun = true; gc("begin_form"); }
  });

  // Nettleseren stopper innsendingen hvis et påkrevd felt mangler; tell hvilket.
  form.addEventListener("invalid", function (e) {
    var label = form.querySelector('label[for="' + e.target.id + '"]');
    gc("form_invalid:" + (label ? label.textContent.trim() : e.target.name));
  }, true);

  form.addEventListener("submit", function () {
    var val = function (n) { var el = form.elements[n]; return el ? String(el.value || "").trim() : ""; };
    gc("generate_lead");
    gc("lead_tjeneste:" + val("Tjeneste"));

    // Kopi til henvendelsesloggen (Google-ark). E-posten fra FormSubmit går uansett.
    var url = form.getAttribute("data-leads");
    if (!url || form.elements._honey.value) return;
    var body = JSON.stringify({
      service: val("Tjeneste"), name: val("Navn"), phone: val("Telefon"), address: val("Adresse") + (val("Område") ? " (" + val("Område") + ")" : ""),
      message: val("Beskrivelse") + (form.elements.Bilde && form.elements.Bilde.files.length ? " [" + form.elements.Bilde.files.length + " bilde(r) på e-post]" : ""),
      page: location.pathname, source: source()
    });
    try {
      fetch(url, { method: "POST", mode: "no-cors", keepalive: true, headers: { "Content-Type": "text/plain;charset=utf-8" }, body: body });
    } catch (e) {}
  });
})();
