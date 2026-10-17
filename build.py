# -*- coding: utf-8 -*-
"""Bygger nettsiden til public/. Kjør: python3 build.py"""
import html
import json
import os
import shutil
from datetime import date

import config as C

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
        "areaServed": {"@type": "City", "name": "Oslo"},
        "knowsAbout": [s["nav"] for s in C.SERVICES],
    }


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
</head>
<body>
<a class="skip" href="#innhold">Hopp til innholdet</a>
"""


def header(active=""):
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{url(s["slug"] + "/")}"{cur if active == s["slug"] else ""}>{e(s["nav"])}</a>'
        for s in C.SERVICES)
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
    <li><strong>Pris før oppstart</strong><span>Du vet hva det koster</span></li>
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


def contact(selected=""):
    opts = "".join(
        f'<option{" selected" if selected == s["form_value"] else ""}>{e(s["form_value"])}</option>'
        for s in C.SERVICES) + '<option>Rens av mur eller fasade</option><option>Annet</option>'
    placeholder = "" if selected else '<option value="" disabled selected>Velg</option>'
    return f"""<section class="contact" id="kontakt">
  <div class="wrap contact-grid">
    <div class="contact-intro">
      <h2>Be om pris</h2>
      <p>Raskest er å ringe eller sende en SMS med et bilde. Du kan også fylle ut skjemaet, så tar vi kontakt.</p>
      <a class="contact-big" href="{tel()}" data-goatcounter-click="ring-kontakt">{C.PHONE_DISPLAY}</a>
      <p class="contact-alt"><a href="{sms()}" data-goatcounter-click="sms-kontakt">Send SMS</a> eller e-post til <a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
    </div>
    <form class="quote-form" action="https://formsubmit.co/{C.FORM_EMAIL}" method="POST" enctype="multipart/form-data">
      <input type="hidden" name="_subject" value="Ny forespørsel fra nettsiden">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_next" value="{abs_url('takk/')}">
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="field">
        <label for="f-tjeneste">Hva gjelder det?</label>
        <select id="f-tjeneste" name="Tjeneste" required>{placeholder}{opts}</select>
      </div>
      <div class="field-row">
        <div class="field"><label for="f-navn">Navn</label><input id="f-navn" name="Navn" autocomplete="name" required></div>
        <div class="field"><label for="f-tlf">Telefon</label><input id="f-tlf" name="Telefon" type="tel" inputmode="tel" autocomplete="tel" required></div>
      </div>
      <div class="field"><label for="f-adr">Adresse eller bydel</label><input id="f-adr" name="Adresse" autocomplete="street-address" required></div>
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
def page_index():
    season = next(s for s in C.SERVICES if s["slug"] == C.SEASON["slug"])
    areas = ", ".join(C.NEAR_AREAS[:-1]) + " og " + C.NEAR_AREAS[-1]

    rows = []
    for s in C.SERVICES:
        inc = "".join(f"<li>{e(i)}</li>" for i in s["includes"])
        if s["image"]:
            name, alt, widths = s["image"]
            media = picture(name, alt, widths, "(min-width: 900px) 46vw, 100vw", "row-media")
        else:
            media = f'<div class="row-media row-season"><p>{e(C.SEASON["tag"])}</p><a class="btn btn-dark" href="{url(s["slug"] + "/")}">Se hva som er med</a></div>'
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
    </div>
  </div>
</section>
{contact()}"""
    title = f"{C.NAME} – hage, løvrydding og snekker i Oslo"
    desc = ("Løvrydding, snekkerarbeid, belegningsstein og hagearbeid i Oslo. "
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
{faq}
{steps()}
{contact(s['form_value'])}"""
    return head(s["meta_title"], s["meta_description"], s["slug"] + "/",
                [business_ld()] + service_ld(s)) + header(s["slug"]) + body + footer()


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
    locs = [""] + [s["slug"] + "/" for s in C.SERVICES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{abs_url(p)}</loc><lastmod>{today}</lastmod></url>\n" for p in locs) + "</urlset>\n"
    write("sitemap.xml", sm)

    # Faktaark for AI-søk (ChatGPT, Perplexity osv.)
    llms = [f"# {C.NAME} – {C.TAGLINE}", "",
            f"> Enkeltpersonforetak i {C.CITY} (org.nr. {C.ORGNR}). Hage og bygg for privatpersoner, borettslag og bedrifter i Oslo.", "",
            f"- Telefon: {C.PHONE_DISPLAY}", f"- E-post: {C.EMAIL}", f"- Base: {C.BASE_AREA}, {C.POSTCODE} {C.CITY}",
            f"- Vurdering: {C.MITTANBUD_RATING} av 5 på Mittanbud ({C.MITTANBUD_COUNT} vurderinger)",
            "- Gratis befaring", "", "## Tjenester", ""]
    for s in C.SERVICES:
        llms.append(f"- [{s['nav']}]({abs_url(s['slug'] + '/')}): {s['summary']}")
    write("llms.txt", "\n".join(llms) + "\n")
    print(f"Bygget til {OUT}  (SITE_URL={C.SITE_URL}, BASE_PATH='{B}', NOINDEX={C.NOINDEX})")


if __name__ == "__main__":
    main()
