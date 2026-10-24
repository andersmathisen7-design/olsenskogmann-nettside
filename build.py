# -*- coding: utf-8 -*-
"""Bygger nettsiden til public/. Kjør: python3 build.py"""
import html
import json
import os
import shutil
from datetime import date

import config as C
import artikler_build as AB
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "public")
B = C.BASE_PATH
ASSET_V = date.today().strftime("%Y%m%d")

e = html.escape


def url(path=""):
    """Intern lenke med BASE_PATH (testdomenet ligger i en undermappe)."""
    return f"{B}/{path}".replace("//", "/") if path else f"{B}/"


def abs_url(path=""):
    return f"{C.SITE_URL}/{path}" if path else f"{C.SITE_URL}/"


def tel():
    return f"tel:+47{C.PHONE}"


def sms():
    return f"sms:+47{C.PHONE}"


def picture(name, alt, widths, sizes, cls="", eager=False):
    widths = sorted(widths)
    webp = ", ".join(f"{url(f'img/{name}-{w}.webp')} {w}w" for w in widths)
    jpg = ", ".join(f"{url(f'img/{name}-{w}.jpg')} {w}w" for w in widths)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture class="{cls}"><source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img src="{url(f"img/{name}-{widths[0]}.jpg")}" srcset="{jpg}" sizes="{sizes}" alt="{e(alt)}" {load} decoding="async"></picture>')


# ---------------------------------------------------------------------------
# Strukturerte data
# ---------------------------------------------------------------------------
def business_ld():
    return {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "@id": abs_url() + "#firma",
        "name": C.NAME,
        "alternateName": f"{C.NAME} – {C.TAGLINE}",
        "url": abs_url(),
        "logo": abs_url("img/logo.png"),
        "image": abs_url("img/olsen-pa-jobb-880.jpg"),
        "telephone": f"+47{C.PHONE}",
        "email": C.EMAIL,
        "taxID": C.ORGNR.replace(" ", ""),
        "address": {"@type": "PostalAddress", "postalCode": C.POSTCODE,
                    "addressLocality": C.CITY, "addressCountry": "NO"},
        "areaServed": [{"@type": "City", "name": "Oslo"}, {"@type": "City", "name": "Lørenskog"}],
        "priceRange": f"{C.PRICE_HOUR_INC} kr/t inkl. mva",
        "knowsAbout": [s["nav"] for s in C.SERVICES],
    }


def package_offers():
    """Fastprispakkene og timeprisen som Offer. Pakker uten pris (etter bilde) tas ikke med."""
    offers = [{"@type": "Offer", "name": f"{p['name']}: {p['for']}", "description": p["time"],
               "price": p["price"], "priceCurrency": "NOK",
               "priceSpecification": {"@type": "PriceSpecification", "price": p["price"], "priceCurrency": "NOK",
                                      "valueAddedTaxIncluded": True}}
              for p in C.PACKAGES["items"] if p["price"]]
    offers.append({"@type": "Offer", "name": "Timepris (introduksjonspris)", "price": C.PRICE_HOUR_INC,
                   "priceCurrency": "NOK", "validThrough": C.PRICE_INTRO_UNTIL,
                   "priceSpecification": {"@type": "UnitPriceSpecification", "price": C.PRICE_HOUR_INC,
                                          "priceCurrency": "NOK", "unitCode": "HUR", "unitText": "time",
                                          "valueAddedTaxIncluded": True, "validThrough": C.PRICE_INTRO_UNTIL}})
    return offers


def nok(n):
    return f"{n:,}".replace(",", " ") + " kr"


def packages_section(slug):
    P = C.PACKAGES
    if slug != P["service"]:
        return ""
    cards = "".join(
        f'<li><h3>{e(p["name"])}</h3><p class="pkg-for">{e(p["for"])}</p>'
        f'<p class="pkg-price">{nok(p["price"]) + " <span>inkl. mva</span>" if p["price"] else "Etter bilde"}</p>'
        f'<p class="pkg-time">{e(p["time"])}</p></li>'
        for p in P["items"])
    return f"""<section class="packages" id="fastpris">
  <div class="wrap">
    <h2>{e(P['title'])}</h2>
    <p class="section-lead">{e(P['lead'])}</p>
    <ul class="pkg-list">{cards}</ul>
    <p class="pkg-note"><strong>{e(P['note'])}</strong></p>
    <a class="btn btn-dark" href="{sms()}" data-goatcounter-click="sms-fastpris">Send bilde på SMS</a>
  </div>
</section>"""


def service_ld(s):
    data = [{
        "@context": "https://schema.org",
        "@type": "Service",
        "name": s["title"],
        "serviceType": s["nav"],
        "description": s["meta_description"],
        "provider": {"@id": abs_url() + "#firma"},
        "areaServed": {"@type": "City", "name": "Oslo"},
        "url": abs_url(s["slug"] + "/"),
        **({"offers": package_offers()} if s["slug"] == C.PACKAGES["service"] else {}),
    }, {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": C.NAME, "item": abs_url()},
            {"@type": "ListItem", "position": 2, "name": s["nav"], "item": abs_url(s["slug"] + "/")},
        ],
    }]
    if s["faq"]:
        data.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faq"]],
        })
    return data


# ---------------------------------------------------------------------------
# Felles deler
# ---------------------------------------------------------------------------
def head(title, desc, path, ld):
    robots = "noindex, nofollow" if C.NOINDEX else "index, follow, max-image-preview:large"
    lds = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    gc = (f'<script data-goatcounter="https://{C.GOATCOUNTER}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
          if C.GOATCOUNTER else "")
    return f"""<!doctype html>
<html lang="nb">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{abs_url(path)}">
<meta name="theme-color" content="#18271F">
<meta property="og:type" content="website">
<meta property="og:locale" content="nb_NO">
<meta property="og:site_name" content="{e(C.NAME)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{abs_url(path)}">
<meta property="og:image" content="{abs_url('img/olsen-pa-jobb-880.jpg')}">
<link rel="icon" href="{url('favicon.ico')}" sizes="48x48">
<link rel="apple-touch-icon" href="{url('img/apple-touch-icon.png')}">
<link rel="preload" href="{url('fonts/barlow-condensed-latin-800-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{url('fonts/barlow-latin-400-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{url('assets/style.css')}?v={ASSET_V}">
{lds}
{gc}
<script src="{url('assets/app.js')}?v={ASSET_V}" defer></script>
</head>
<body>
<a class="skip" href="#innhold">Hopp til innholdet</a>
"""


def header(active=""):
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{url(s["slug"] + "/")}"{cur if active == s["slug"] else ""}>{e(s["nav"])}</a>'
        for s in C.SERVICES if s.get("in_nav", True))
    return f"""<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{url()}" aria-label="{e(C.NAME)}, til forsiden">
      <picture><source type="image/webp" srcset="{url('img/logo.webp')}"><img src="{url('img/logo.png')}" alt="{e(C.NAME)} – {e(C.TAGLINE)}" width="640" height="114"></picture>
    </a>
    <nav class="main-nav" aria-label="Tjenester">{links}<a href="#kontakt">Kontakt</a></nav>
    <a class="header-phone" href="{tel()}" data-goatcounter-click="ring-header">{C.PHONE_DISPLAY}</a>
  </div>
</header>
<main id="innhold">
"""


def trust_band():
    rating = (f'<a href="{e(C.MITTANBUD_URL)}" rel="noopener">{C.MITTANBUD_RATING} av 5 på Mittanbud</a>'
              if C.MITTANBUD_URL else f'{C.MITTANBUD_RATING} av 5 på Mittanbud')
    return f"""<section class="trust" aria-label="Hvorfor velge oss">
  <ul class="wrap trust-list">
    <li><span class="stars" aria-hidden="true">★★★★★</span><strong>{rating}</strong><span>{C.MITTANBUD_COUNT} vurderinger fra kunder</span></li>
    <li><strong>Gratis befaring</strong><span>Vi ser på jobben før du bestemmer deg</span></li>
    <li><strong>{C.PRICE_HOUR_INC} kr/t inkl. mva</strong><span>Introduksjonspris til {C.PRICE_INTRO_UNTIL_TEXT}. Eller fastpris, og hageavfallet kjører vi alltid bort</span></li>
    <li><strong>Registrert foretak</strong><span>Org.nr. {C.ORGNR}, MVA-registrert</span></li>
  </ul>
</section>
"""


def steps():
    items = "".join(f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in C.STEPS)
    return f"""<section class="steps-section">
  <div class="wrap">
    <h2>Slik går det til</h2>
    <ol class="steps">{items}</ol>
  </div>
</section>
"""


def contact(selected="", area=""):
    opts = "".join(
        f'<option{" selected" if selected == s["form_value"] else ""}>{e(s["form_value"])}</option>'
        for s in C.SERVICES) + '<option>Annet</option>'
    placeholder = "" if selected else '<option value="" disabled selected>Velg</option>'
    return f"""<section class="contact" id="kontakt">
  <div class="wrap contact-grid">
    <div class="contact-intro">
      <h2>Be om pris</h2>
      <p>Raskest er å ringe eller sende en SMS med et bilde. Du kan også fylle ut skjemaet, så tar vi kontakt.</p>
      <a class="contact-big" href="{tel()}" data-goatcounter-click="ring-kontakt">{C.PHONE_DISPLAY}</a>
      <p class="contact-alt"><a href="{sms()}" data-goatcounter-click="sms-kontakt">Send SMS</a> eller e-post til <a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
    </div>
    <form class="quote-form" action="https://formsubmit.co/{C.FORM_EMAIL}" method="POST" enctype="multipart/form-data"{f' data-leads="{e(C.LEADS_URL)}"' if C.LEADS_URL else ''}>
      <input type="hidden" name="_subject" value="Ny forespørsel fra nettsiden">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_next" value="{abs_url('takk/')}">
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      {f'<input type="hidden" name="Område" value="{e(area)}">' if area else ''}
      <div class="field">
        <label for="f-tjeneste">Hva gjelder det?</label>
        <select id="f-tjeneste" name="Tjeneste" required>{placeholder}{opts}</select>
      </div>
      <div class="field-row">
        <div class="field"><label for="f-navn">Navn</label><input id="f-navn" name="Navn" autocomplete="name" required></div>
        <div class="field"><label for="f-tlf">Telefon</label><input id="f-tlf" name="Telefon" type="tel" inputmode="tel" autocomplete="tel" required></div>
      </div>
      <div class="field"><label for="f-adr">Adresse eller bydel</label><input id="f-adr" name="Adresse" autocomplete="street-address" required{f' placeholder="F.eks. gate og nummer i {e(area)}"' if area else ''}></div>
      <div class="field"><label for="f-besk">Beskriv jobben</label><textarea id="f-besk" name="Beskrivelse" rows="4" placeholder="Hva skal gjøres, og omtrent hvor stort er området?"></textarea></div>
      <div class="field"><label for="f-bilde">Bilder <span class="opt">(valgfritt)</span></label><input id="f-bilde" name="Bilde" type="file" accept="image/*" multiple></div>
      <button class="btn btn-dark" type="submit">Send forespørsel</button>
      <p class="form-note">Vi bruker opplysningene bare til å svare deg. Skjemaet sendes til oss på e-post via FormSubmit.</p>
    </form>
  </div>
</section>
"""


def footer():
    links = "".join(f'<li><a href="{url(s["slug"] + "/")}">{e(s["nav"])}</a></li>' for s in C.SERVICES)
    links += f'<li><a href="{url("artikler/")}">Råd og priser</a></li>'
    return f"""</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <img class="footer-logo" src="{url('img/logo.png')}" alt="{e(C.NAME)}" width="640" height="114">
      <p>Enkeltpersonforetak fra {C.BASE_AREA}, {C.CITY}.<br>Org.nr. {C.ORGNR} MVA</p>
    </div>
    <div>
      <h2>Tjenester</h2>
      <ul>{links}</ul>
    </div>
    <div>
      <h2>Kontakt</h2>
      <ul>
        <li><a href="{tel()}">{C.PHONE_DISPLAY}</a></li>
        <li><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></li>
        <li>{C.POSTCODE} {C.CITY}</li>
      </ul>
    </div>
  </div>
</footer>
<div class="callbar" aria-label="Kontakt oss">
  <a href="{tel()}" data-goatcounter-click="ring-mobil">Ring {C.PHONE_DISPLAY}</a>
  <a href="{sms()}" data-goatcounter-click="sms-mobil">Send SMS</a>
</div>
</body>
</html>
"""


def stripes():
    return '<div class="reflect" aria-hidden="true"><span></span><span></span></div>'


# ---------------------------------------------------------------------------
# Sider
# ---------------------------------------------------------------------------
def borettslag_band():
    b = next((x for x in C.SERVICES if x["slug"] == "borettslag"), None)
    if not b:
        return ""
    inc = "".join(f"<li>{e(i)}</li>" for i in b["includes"][:4])
    return f"""<section class="band-brl">
  <div class="wrap brl-grid">
    <div>
      <h2>Borettslag og sameier</h2>
      <p class="brl-lead">{e(b['lead'])}</p>
      <a class="btn btn-dark" href="{url(b['slug'] + '/')}">Fast avtale for styret</a>
    </div>
    <ul class="checks">{inc}</ul>
  </div>
</section>"""


def page_index():
    season = next(s for s in C.SERVICES if s["slug"] == C.SEASON["slug"])
    areas = ", ".join(C.NEAR_AREAS[:-1]) + " og " + C.NEAR_AREAS[-1]
    area_links = "".join(f'<li><a href="{url(a["slug"] + "/")}">{e(a["bydel"])}</a></li>' for a in C.AREAS)

    rows = []
    for s in [x for x in C.SERVICES if x.get("in_index", True)]:
        inc = "".join(f"<li>{e(i)}</li>" for i in s["includes"])
        if s["image"]:
            name, alt, widths = s["image"]
            media = picture(name, alt, widths, "(min-width: 900px) 46vw, 100vw", "row-media")
        elif s["slug"] == C.SEASON["slug"]:
            media = f'<div class="row-media row-season"><p>{e(C.SEASON["tag"])}</p><a class="btn btn-dark" href="{url(s["slug"] + "/")}">Se hva som er med</a></div>'
        else:
            media = f'<div class="row-media row-panel"><p>{e(s.get("panel", s["nav"]))}</p><a class="btn btn-line btn-on-dark" href="{url(s["slug"] + "/")}">Se hva vi gjør</a></div>'
        rows.append(f"""<article class="service-row">
  {media}
  <div class="row-text">
    <h3><a href="{url(s['slug'] + '/')}">{e(s['nav'])}</a></h3>
    <p>{e(s['summary'])}</p>
    <ul class="checks">{inc}</ul>
    <a class="text-link" href="{url(s['slug'] + '/')}">Les mer om {e(s['nav'].lower())}</a>
  </div>
</article>""")

    body = f"""<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-text">
      <p class="hero-tag">{e(C.SEASON['tag'])}</p>
      <h1>{e(C.SEASON['title'])}</h1>
      <p class="hero-lead">{e(C.SEASON['lead'])}</p>
      <div class="hero-cta">
        <a class="btn btn-dark" href="{tel()}" data-goatcounter-click="ring-hero">Ring {C.PHONE_DISPLAY}</a>
        <a class="btn btn-line" href="{url(season['slug'] + '/')}">Om løvrydding</a>
      </div>
    </div>
    <figure class="hero-photo">
      {picture('olsen-pa-jobb', 'Olsen på jobb i en hage i Oslo', [880], '(min-width: 900px) 40vw, 90vw', eager=True)}
    </figure>
  </div>
  {stripes()}
</section>
{trust_band()}
<section class="services">
  <div class="wrap">
    <h2>Dette gjør vi</h2>
    <p class="section-lead">Hage og bygg i Oslo, for privatpersoner, borettslag og bedrifter.</p>
    {''.join(rows)}
  </div>
</section>
{borettslag_band()}
{steps()}
<section class="about">
  <div class="wrap about-grid">
    <div>
      <h2>Lokal i Oslo øst</h2>
      <p>{e(C.ABOUT)}</p>
    </div>
    <div>
      <h2>Her jobber vi</h2>
      <p>Hele Oslo. Kortest vei har vi til {e(areas)}.</p>
      <ul class="area-links">{area_links}</ul>
    </div>
  </div>
</section>
{contact()}"""
    title = f"{C.NAME} – løvrydding, hagearbeid og snekker i Oslo"
    desc = ("Løvrydding, hekk, stubbefjerning, snekker og belegningsstein i Oslo og Lørenskog. "
            f"{C.MITTANBUD_RATING} av 5 på Mittanbud. Gratis befaring. Ring {C.PHONE_DISPLAY}.")
    return head(title, desc, "", [business_ld()]) + header() + body + footer()


def page_service(s):
    inc = "".join(f"<li>{e(i)}</li>" for i in s["includes"])
    who = ""
    if s["for_whom"]:
        who = '<div class="who"><h2>For hvem</h2><dl>' + "".join(
            f"<div><dt>{e(t)}</dt><dd>{e(d)}</dd></div>" for t, d in s["for_whom"]) + "</dl></div>"
    secs = "".join(f'<div class="prose-block"><h2>{e(t)}</h2><p>{e(p)}</p></div>' for t, p in s["sections"])
    photos = ""
    if s["photos"]:
        photos = '<div class="gallery">' + "".join(
            f'<figure>{picture(n, a, w, "(min-width: 900px) 45vw, 100vw")}<figcaption>{e(a)}</figcaption></figure>'
            for n, a, w in s["photos"]) + "</div>"
    faq = ""
    if s["faq"]:
        faq = '<section class="faq"><div class="wrap narrow"><h2>Spørsmål og svar</h2>' + "".join(
            f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in s["faq"]) + "</div></section>"

    is_season = s["slug"] == C.SEASON["slug"]
    hero_cls = "hero hero-page" if is_season else "page-hero"
    body = f"""<section class="{hero_cls}">
  <div class="wrap">
    <nav class="crumbs" aria-label="Brødsmuler"><a href="{url()}">Forsiden</a> / <span>{e(s['nav'])}</span></nav>
    <h1>{e(s['title'])}</h1>
    <p class="hero-lead">{e(s['lead'])}</p>
    <div class="hero-cta">
      <a class="btn btn-dark" href="{tel()}" data-goatcounter-click="ring-{s['slug']}">Ring {C.PHONE_DISPLAY}</a>
      <a class="btn btn-line" href="#kontakt">Be om pris</a>
    </div>
  </div>
  {stripes() if is_season else ''}
</section>
{trust_band() if is_season else ''}
<section class="service-detail">
  <div class="wrap detail-grid">
    <div class="includes">
      <h2>Dette er med</h2>
      <ul class="checks">{inc}</ul>
    </div>
    <div class="detail-text">{who}{secs}</div>
  </div>
  {f'<div class="wrap">{photos}</div>' if photos else ''}
</section>
{packages_section(s['slug'])}
{faq}
{related_articles(s['slug'])}
{steps()}
{contact(s['form_value'])}"""
    return head(s["meta_title"], s["meta_description"], s["slug"] + "/",
                [business_ld()] + service_ld(s)) + header(s["slug"]) + body + footer()


def related_articles(slug):
    arts = [a for a in AB.load() if a.get("tjeneste") == slug]
    if not arts:
        return ""
    items = "".join(f'<li><a href="{url("artikler/" + a["slug"] + "/")}"><strong>{e(a["title"])}</strong></a><span>{e(a["description"])}</span></li>' for a in arts)
    return f'<section class="related"><div class="wrap narrow"><h2>Les også</h2><ul class="article-list">{items}</ul></div></section>'


def page_simple(title, h1, text, path):
    body = f"""<section class="page-hero simple">
  <div class="wrap narrow">
    <h1>{e(h1)}</h1>
    <p class="hero-lead">{text}</p>
    <div class="hero-cta"><a class="btn btn-dark" href="{url()}">Til forsiden</a><a class="btn btn-line" href="{tel()}">Ring {C.PHONE_DISPLAY}</a></div>
  </div>
</section>"""
    return head(title, title, path, [business_ld()]) + header() + body + footer()


# ---------------------------------------------------------------------------
# Områdesider
# ---------------------------------------------------------------------------
def nbnum(n):
    return f"{n:,}".replace(",", " ")


def area_ld(a):
    return [{
        "@context": "https://schema.org", "@type": "Service",
        "name": a.get("title", f"Løvrydding og hagearbeid i {a['bydel']}"),
        "serviceType": "Hagearbeid", "provider": {"@id": abs_url() + "#firma"},
        "areaServed": {"@type": "AdministrativeArea", "name": a.get("area_name", f"Bydel {a['bydel']}, Oslo")},
        "url": abs_url(a["slug"] + "/"),
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": C.NAME, "item": abs_url()},
            {"@type": "ListItem", "position": 2, "name": a["bydel"], "item": abs_url(a["slug"] + "/")},
        ],
    }]


def page_area(a):
    st = a["stats"]
    smahus = st["enebolig"] + st["tomannsbolig"] + st["rekkehus"]
    andel = round(smahus / st["totalt"] * 100)
    oslo_andel = round(C.OSLO_SMAHUS["smahus"] / C.OSLO_SMAHUS["boliger"] * 100)
    places = ", ".join(a["places"][:-1]) + " og " + a["places"][-1]
    services = "".join(
        f'<li><a href="{url(s["slug"] + "/")}"><strong>{e(s["nav"])}</strong></a><span>{e(s["summary"])}</span></li>'
        for s in C.SERVICES)
    others = " · ".join(f'<a href="{url(o["slug"] + "/")}">{e(o["bydel"])}</a>' for o in C.AREAS if o is not a)
    rows = [("Eneboliger", st["enebolig"]), ("Tomannsboliger o.l.", st["tomannsbolig"]),
            ("Rekkehus og kjedehus", st["rekkehus"]), ("Blokkleiligheter", st["blokk"])]
    table = "".join(f"<tr><th scope=\"row\">{e(k)}</th><td>{nbnum(v)}</td></tr>" for k, v in rows)
    title = a.get("title", f"Løvrydding og hagearbeid i {a['bydel']}")
    src = a.get("source", C.BOLIG_KILDE)
    note = f" {e(a['stats_note'])}" if a.get("stats_note") else ""
    desc = (f"Løvrydding, hekk, snekker og belegningsstein i {a['bydel']} – {', '.join(a['places'][:3])} m.fl. "
            f"Lokal fra Tveita. Gratis befaring. Ring {C.PHONE_DISPLAY}.")
    body = f"""<section class="page-hero area-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Brødsmuler"><a href="{url()}">Forsiden</a> / <span>{e(a['bydel'])}</span></nav>
    <h1>{e(title)}</h1>
    <p class="hero-lead">{e(a['intro'])}</p>
    <div class="hero-cta">
      <a class="btn btn-dark" href="{tel()}" data-goatcounter-click="ring-{a['slug']}">Ring {C.PHONE_DISPLAY}</a>
      <a class="btn btn-line" href="#kontakt">Be om pris</a>
    </div>
  </div>
</section>
{trust_band()}
<section class="service-detail">
  <div class="wrap detail-grid">
    <div class="area-facts">
      <h2>Boligene i {e(a['bydel'])}</h2>
      <table class="facts">
        <tbody>{table}</tbody>
        <tfoot><tr><th scope="row">Småhus i alt</th><td>{nbnum(smahus)} ({andel}&nbsp;%)</td></tr></tfoot>
      </table>
      <p class="source">{note} Kilde: <a href="{e(src[1])}" rel="noopener">{e(src[0])}</a>. Snittet for Oslo er {oslo_andel}&nbsp;% småhus. <a href="{url('artikler/smahus-i-oslo-per-bydel/')}">Se alle bydelene</a>.</p>
    </div>
    <div class="detail-text">
      <div class="prose-block"><h2>{e(a['angle'][0])}</h2><p>{e(a['angle'][1])}</p></div>
      <div class="prose-block"><h2>Her jobber vi</h2><p>Hele {e(a['bydel']) if a.get('area_name') else 'bydel ' + e(a['bydel'])}, blant annet {e(places)}.</p></div>
      <div class="prose-block"><h2>Dette kan vi hjelpe med</h2><ul class="area-services">{services}</ul></div>
    </div>
  </div>
</section>
{steps()}
{contact('', a['bydel'])}
<section class="other-areas"><div class="wrap"><p>Andre bydeler: {others}</p></div></section>"""
    return head(f"{title} | {C.NAME}", desc, a["slug"] + "/", [business_ld()] + area_ld(a)) + header() + body + footer()


# ---------------------------------------------------------------------------
# Artikler (Råd og priser)
# ---------------------------------------------------------------------------
def fix_links(h):
    """Interne lenker i Markdown skrives som /sti/ og får BASE_PATH her."""
    return re.sub(r'href="/(?!/)', f'href="{B}/', h) if B else h


def article_ld(a):
    data = [{
        "@context": "https://schema.org", "@type": "Article",
        "headline": a["title"], "description": a["description"],
        "datePublished": a["date"], "dateModified": a["updated"], "inLanguage": "nb-NO",
        "author": {"@id": abs_url() + "#firma"}, "publisher": {"@id": abs_url() + "#firma"},
        "mainEntityOfPage": abs_url(f"artikler/{a['slug']}/"),
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": C.NAME, "item": abs_url()},
            {"@type": "ListItem", "position": 2, "name": "Råd og priser", "item": abs_url("artikler/")},
            {"@type": "ListItem", "position": 3, "name": a["title"], "item": abs_url(f"artikler/{a['slug']}/")},
        ],
    }]
    if a["faq"]:
        data.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in a["faq"]]})
    return data


def nbdate(iso):
    m = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"]
    y, mo, d = iso.split("-")
    return f"{int(d)}. {m[int(mo) - 1]} {y}"


def page_article(a, arts):
    svc = next((s for s in C.SERVICES if s["slug"] == a.get("tjeneste")), C.SERVICES[0])
    kontakt = f"""<aside class="cta-box">
  <h2>Vil du heller slippe?</h2>
  <p>Vi tar {e(svc['nav'].lower())} i hele Oslo. Send et bilde, så får du prisen før vi starter.</p>
  <div class="hero-cta"><a class="btn btn-dark" href="{tel()}" data-goatcounter-click="ring-artikkel">Ring {C.PHONE_DISPLAY}</a><a class="btn btn-line" href="{url(svc['slug'] + '/')}#kontakt" data-goatcounter-click="article_cta">Be om pris</a></div>
</aside>"""
    body_html = fix_links(AB.markdown(a["body"], {"kontakt": "<!--KONTAKT-->"})).replace("<!--KONTAKT-->", kontakt)
    faq = ""
    if a["faq"]:
        faq = "<h2>Spørsmål og svar</h2>" + "".join(f"<details><summary>{e(q)}</summary><p>{e(ans)}</p></details>" for q, ans in a["faq"])
    more = "".join(f'<li><a href="{url("artikler/" + o["slug"] + "/")}">{e(o["title"])}</a></li>' for o in arts if o is not a)[:4000]
    upd = f" · Oppdatert {nbdate(a['updated'])}" if a["updated"] != a["date"] else ""
    body = f"""<article class="article">
  <header class="page-hero">
    <div class="wrap narrow">
      <nav class="crumbs" aria-label="Brødsmuler"><a href="{url()}">Forsiden</a> / <a href="{url('artikler/')}">Råd og priser</a></nav>
      <h1>{e(a['title'])}</h1>
      <p class="article-date">Publisert {nbdate(a['date'])}{upd}</p>
    </div>
  </header>
  <div class="wrap narrow article-body">
    {f'<div class="short-answer"><h2>Kort svar</h2><p>{e(a["kort"])}</p></div>' if a.get("kort") else ''}
    {body_html}
    <div class="faq">{faq}</div>
    {f'<nav class="more" aria-label="Flere artikler"><h2>Les også</h2><ul>{more}</ul></nav>' if more else ''}
  </div>
</article>"""
    return head(f"{a['title']} | {C.NAME}", a["description"], f"artikler/{a['slug']}/", [business_ld()] + article_ld(a)) + header() + body + footer()


def page_articles_index(arts):
    items = "".join(
        f'<li><a href="{url("artikler/" + a["slug"] + "/")}"><strong>{e(a["title"])}</strong></a><span>{e(a["description"])}</span></li>'
        for a in arts)
    body = f"""<section class="page-hero">
  <div class="wrap narrow">
    <nav class="crumbs" aria-label="Brødsmuler"><a href="{url()}">Forsiden</a> / <span>Råd og priser</span></nav>
    <h1>Råd og priser</h1>
    <p class="hero-lead">Svar på det folk spør oss om: hva ting koster, hva du kan gjøre selv, og regler i Oslo. Med kilde på alle tall.</p>
  </div>
</section>
<section class="service-detail"><div class="wrap narrow"><ul class="article-list">{items}</ul></div></section>"""
    return head(f"Råd og priser for hage og bygg i Oslo | {C.NAME}",
                "Priser og råd om løvrydding, hagearbeid, terrasse og belegningsstein i Oslo, med kilder.",
                "artikler/", [business_ld()]) + header() + body + footer()


# ---------------------------------------------------------------------------
# Eiersiden /admin/ (skjult for Google, streng sikkerhetsregel)
# ---------------------------------------------------------------------------
def page_admin():
    cfg = json.dumps({"leadsUrl": C.LEADS_URL, "services": [s["form_value"] for s in C.SERVICES]}, ensure_ascii=False)
    csp = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; "
           "connect-src https://script.google.com https://script.googleusercontent.com; form-action 'none'; "
           "base-uri 'none'")
    return f"""<!doctype html>
<html lang="nb">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{csp}">
<meta name="robots" content="noindex, nofollow">
<meta name="referrer" content="no-referrer">
<title>Henvendelser – {e(C.NAME)}</title>
<link rel="icon" href="{url('favicon.ico')}" sizes="48x48">
<link rel="stylesheet" href="{url('assets/style.css')}?v={ASSET_V}">
<script type="application/json" id="admin-cfg">{cfg}</script>
<script src="{url('assets/admin.js')}?v={ASSET_V}" defer></script>
</head>
<body class="admin">
<header class="site-header"><div class="wrap header-inner">
  <a class="brand" href="{url()}"><img src="{url('img/logo.png')}" alt="{e(C.NAME)}" width="640" height="114"></a>
  <div class="admin-actions" id="a-actions" hidden>
    <span id="a-updated" class="admin-updated"></span>
    <button type="button" class="btn btn-sm" id="a-refresh">Oppdater</button>
    <button type="button" class="btn btn-sm btn-ghost" id="a-logout">Logg ut</button>
  </div>
</div></header>
<main class="wrap admin-main">
  <h1>Henvendelser</h1>
  <div id="a-nocal" class="admin-empty" hidden>
    <p>Henvendelsesloggen er ikke satt opp ennå. Følg <strong>henvendelser/README.md</strong> i repoet, og lim inn nettapp-adressen som <code>LEADS_URL</code> i <code>config.py</code>.</p>
  </div>
  <form id="a-login" class="admin-login" hidden>
    <label for="a-key">Passord</label>
    <input id="a-key" type="password" autocomplete="current-password" required>
    <label class="check"><input id="a-remember" type="checkbox"> Husk meg på denne enheten (30 dager)</label>
    <button class="btn btn-dark" type="submit">Logg inn</button>
    <p id="a-login-msg" class="form-msg err" role="alert"></p>
  </form>
  <div id="a-app" hidden>
    <div id="a-stats" class="admin-stats" aria-live="polite"></div>
    <div class="admin-tabs" role="group" aria-label="Vis">
      <button type="button" data-view="aktive" aria-pressed="true">Åpne</button>
      <button type="button" data-view="avsluttet" aria-pressed="false">Avsluttet</button>
      <button type="button" data-view="alle" aria-pressed="false">Alle</button>
    </div>
    <div id="a-list" class="admin-list"></div>
    <div id="a-breakdown" class="admin-breakdown"></div>
    <details class="admin-add">
      <summary>Legg inn henvendelse fra telefon, SMS eller Mittanbud</summary>
      <form id="a-add">
        <div class="field-row">
          <div class="field"><label for="ad-tjeneste">Tjeneste</label><select id="ad-tjeneste"></select></div>
          <div class="field"><label for="ad-kilde">Kom fra</label><select id="ad-kilde"><option>Telefon</option><option>SMS</option><option>Mittanbud</option><option>Anbefaling</option><option>Flyer</option><option>Facebook</option><option>Fast kunde</option><option>Annet</option></select></div>
        </div>
        <div class="field-row">
          <div class="field"><label for="ad-navn">Navn</label><input id="ad-navn"></div>
          <div class="field"><label for="ad-tlf">Telefon</label><input id="ad-tlf" type="tel"></div>
        </div>
        <div class="field"><label for="ad-adresse">Adresse</label><input id="ad-adresse"></div>
        <div class="field"><label for="ad-melding">Hva gjelder det?</label><textarea id="ad-melding" rows="2"></textarea></div>
        <button class="btn btn-dark" type="submit">Lagre</button>
        <p id="a-add-msg" class="form-msg" role="status"></p>
      </form>
    </details>
  </div>
</main>
</body>
</html>
"""


# ---------------------------------------------------------------------------
def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT)

    write("index.html", page_index())
    for s in C.SERVICES:
        write(f"{s['slug']}/index.html", page_service(s))
    write("takk/index.html", page_simple(
        "Takk for forespørselen", "Takk! Vi har fått forespørselen din",
        "Vi tar kontakt på telefon eller SMS. Haster det, kan du ringe oss direkte.", "takk/"))
    for a in C.AREAS:
        write(f"{a['slug']}/index.html", page_area(a))
    arts = AB.load()
    for a in arts:
        write(f"artikler/{a['slug']}/index.html", page_article(a, arts))
    write("artikler/index.html", page_articles_index(arts))
    write("admin/index.html", page_admin())
    shutil.copytree(os.path.join(ROOT, "data"), os.path.join(OUT, "data"))
    write("404.html", page_simple(
        "Fant ikke siden", "Fant ikke siden",
        "Lenken kan være gammel. Gå til forsiden eller ring oss.", "404.html"))

    # robots.txt og sitemap
    if C.NOINDEX:
        robots = "User-agent: *\nDisallow: /\n"
    else:
        robots = f"User-agent: *\nAllow: /\n\nSitemap: {abs_url('sitemap.xml')}\n"
    write("robots.txt", robots)
    today = date.today().isoformat()
    locs = ([""] + [s["slug"] + "/" for s in C.SERVICES] + [a["slug"] + "/" for a in C.AREAS]
            + ["artikler/"] + [f"artikler/{a['slug']}/" for a in arts])
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{abs_url(p)}</loc><lastmod>{today}</lastmod></url>\n" for p in locs) + "</urlset>\n"
    write("sitemap.xml", sm)

    # Faktaark for AI-søk (ChatGPT, Perplexity osv.)
    llms = [f"# {C.NAME} – {C.TAGLINE}", "",
            f"> Enkeltpersonforetak i {C.CITY} (org.nr. {C.ORGNR}). Hage og bygg for privatpersoner, borettslag og bedrifter i Oslo.", "",
            f"- Telefon: {C.PHONE_DISPLAY}", f"- E-post: {C.EMAIL}", f"- Base: {C.BASE_AREA}, {C.POSTCODE} {C.CITY}",
            f"- Vurdering: {C.MITTANBUD_RATING} av 5 på Mittanbud ({C.MITTANBUD_COUNT} vurderinger)",
            f"- Pris: {C.PRICE_TEXT} ({C.PRICE_HOUR_EX} kr eks. mva), {C.PRICE_INTRO_TEXT}, eller fastpris etter befaring. {C.PRICE_REGULAR_TEXT}",
            f"- {C.PACKAGES['title']}: " + "; ".join(
                f"{p['name'].lower()} ({p['for'].lower()}, {p['time'].lower()}) {nok(p['price']).replace(chr(160), ' ')} inkl. mva"
                if p["price"] else f"{p['name'].lower()}: {p['time'][0].lower() + p['time'][1:]}" for p in C.PACKAGES["items"])
            + f". {C.PACKAGES['note']}",
            "- Kjører alltid bort hageavfall", "- Gratis befaring", "", "## Tjenester", ""]
    for s in C.SERVICES:
        llms.append(f"- [{s['nav']}]({abs_url(s['slug'] + '/')}): {s['summary']}")
    llms += ["", "## Områder", ""]
    for a in C.AREAS:
        llms.append(f"- [{a['bydel']}]({abs_url(a['slug'] + '/')})")
    llms += ["", "## Råd og priser", ""]
    for a in arts:
        llms.append(f"- [{a['title']}]({abs_url('artikler/' + a['slug'] + '/')}): {a.get('kort', a['description'])}")
    llms += ["", "## Åpne data", "", f"- [Småhus per bydel i Oslo 2025 (CSV)]({abs_url('data/smahus-per-bydel-oslo-2025.csv')}): summert fra Oslo kommunes statistikkbank, tabell BOL001"]
    write("llms.txt", "\n".join(llms) + "\n")
    print(f"Bygget til {OUT}  (SITE_URL={C.SITE_URL}, BASE_PATH='{B}', NOINDEX={C.NOINDEX})")


if __name__ == "__main__":
    main()
