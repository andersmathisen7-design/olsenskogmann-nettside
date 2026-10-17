# Olsen Skogmann – ny nettside (testversjon)

Dette er en rask, statisk nettside for Olsen Skogmann – Hage & Bygg i Oslo. Den er bygget for lokalt søk på Google og for KI-søk som ChatGPT og Perplexity.
Oppsettet er det samme som på follobjorkeved.no: Python-bygg, innholdet i `config.py`, artikler i Markdown, FormSubmit, GoatCounter og publisering med GitHub Actions.

**Test:** https://andersmathisen7-design.github.io/olsenskogmann-nettside/
Testsiden er skjult for Google med `noindex` og `robots.txt`, så den ikke konkurrerer med olsenskogmann.no.

- Markedsanalyse og søkeord med tall og kilder: **[ANALYSE.md](ANALYSE.md)**
- Kataloger og lenker: **[LENKEBYGGING.md](LENKEBYGGING.md)**
- Det som må gjøres eller avklares: **[GJOREMAL.md](GJOREMAL.md)**
- Henvendelsesloggen og eiersiden: **[henvendelser/README.md](henvendelser/README.md)**

## Innhold

| Side | Mål i søk |
|---|---|
| `/` | «hagearbeid Oslo», «løvrydding Oslo», navnet. Sesongtilbudet (løvrydding) står øverst |
| `/lovrydding/` | «løvrydding Oslo», «løvblåsing», «høstrydding hage». FAQ med strukturerte data |
| `/snekker/` | «snekker Oslo», «bygge terrasse», «utvendig trapp» |
| `/beskjaering-og-trefelling/` | «hekkeklipping Oslo», «beskjæring», «felle tre», «fjerne stubbe», «stubbefresing» |
| `/borettslag/` | Styrer i borettslag og sameier: fast avtale for uteområdet |
| `/stein-og-hage/` | «belegningsstein Oslo», «støttemur» |
| `/rens-av-stein/` | «rens av belegningsstein», «spyle stein», «fjerne mose på stein» |
| `/hagearbeid-alna/`, `/hagearbeid-ostensjo/`, `/hagearbeid-nordstrand/`, `/hagearbeid-sondre-nordstrand/`, `/hagearbeid-stovner/`, `/hagearbeid-lorenskog/`, `/hagearbeid-oslo-sentrum/` | «hagearbeid/løvrydding + bydel». Hver side har egne boligtall fra Oslo kommune og egen tekst. Skjemaet vet hvilken bydel kunden kom fra |
| `/artikler/` | Råd og priser. Markdown i `artikler/`, formatet står øverst i `artikler_build.py` |
| `/artikler/smahus-i-oslo-per-bydel/` + `/data/…csv` | Egne tall (småhus per bydel 2025). Laget for å få lenker (se LENKEBYGGING.md) |
| `/admin/` | Ikke i søk. Eiersiden med henvendelser, status og tall (krever passord) |
| `/takk/` | Takkeside etter skjema. Brukes til å måle konverteringer |
| `/llms.txt` | Faktaark for KI-søk |
| `sitemap.xml`, `robots.txt` | Lages automatisk |

Andre SEO-grep:
- Strukturerte data (JSON-LD): `HomeAndConstructionBusiness`, `Service`, `Article`, `FAQPage` og `BreadcrumbList`.
- Ingen WordPress. Ren HTML og CSS med ca. 3 KB JavaScript. Fontene ligger lokalt, så ingenting lastes fra Google og det trengs ikke samtykkebanner.
- Bildene er i WebP med JPG som reserve, har flere størrelser og er uten GPS-data. Originalene på dagens side viser hvor bildet ble tatt, ofte hjemme hos kunden.
- Canonical, Open Graph og norsk språkkode på alle sider.
- IndexNow varsler Bing om alle sider ved hver publisering, men bare når siden er live (`NOINDEX=0`).

Valgene bak siden:
- **Én tydelig sak øverst.** Sesongtilbudet ligger i `SEASON` i `config.py`. Bytt det når sesongen skifter, for eksempel til vårrydding.
- **Egne sider per tjeneste og bydel.** Google rangerer én side per tema.
- **Ring og SMS er alltid synlige på mobil.** 51,5 % av trafikken i Norge er mobil (StatCounter, september 2026).
- **Vurderingene fra Mittanbud står øverst.** 47 % velger bort en bedrift med under 20 vurderinger (BrightLocal 2026).

## Endre tekst

Alt innhold ligger i **`config.py`**: telefon, tjenester, bydeler, FAQ og sesongtilbud. Design ligger i `src/assets/style.css`.

```bash
python3 build.py                                               # bygger til public/
python3 -m http.server 8000 --directory public                 # se siden på http://localhost:8000
```

Hver push til `main` bygger siden og publiserer den på `gh-pages`-branchen med GitHub Actions.

### Første gang: slå på GitHub Pages
1. Push til `main`, og vent til workflowen «Publiser nettsiden» er grønn under **Actions**.
2. Gå til **Settings → Pages**. Velg **Deploy from a branch**, branch `gh-pages` og mappe `/ (root)`.
3. Etter et minutt er siden på adressen over.

## Henvendelser: e-post og logg

Skjemaet sender til `FORM_EMAIL` gjennom [FormSubmit](https://formsubmit.co). Kunden kan legge ved bilder.
1. Send én testforespørsel. FormSubmit sender en aktiverings-e-post til olsenskogmann@gmail.com. Klikk **Activate**.
2. Anbefalt: bytt adressen i `FORM_EMAIL` med koden fra aktiverings-e-posten, så adressen ikke står i kildekoden.

Er `LEADS_URL` satt, lagres hver henvendelse også i et Google-ark. Olsen følger dem opp på `/admin/` (ny → kontaktet → befaring → tilbud → vunnet/tapt). Se [henvendelser/README.md](henvendelser/README.md).

## Besøksstatistikk (GoatCounter)

Sett `GOATCOUNTER` i `config.py` til navnet på GoatCounter-siden, for eksempel `olsenskogmann`. GoatCounter bruker ingen cookies, så siden trenger ikke samtykkebanner.

Hendelser som telles:
- **ring-\*** og **sms-\***: trykk på telefon eller SMS. Navnet sier hvor på siden, for eksempel `ring-hero`, `ring-mobil` eller `ring-hagearbeid-ostensjo`.
- **begin_form**: begynte på skjemaet.
- **form_invalid:\<felt\>**: trykket Send, men et felt manglet.
- **generate_lead** og **lead_tjeneste:\<tjeneste\>**: sendte skjemaet.
- **article_cta**: klikk fra en artikkel til «Be om pris».
- **/takk/**: fullført forespørsel.

For hendelser viser kilden (referrer) siden hendelsen skjedde på.

## Ukentlig overvåking

En planlagt jobb kjører hver mandag morgen. Den sjekker at alle sider svarer, at lenker og JSON-LD er gyldige og at skjemaet virker (med falsk FormSubmit). Den henter besøkstall fra GoatCounter når det er satt opp, og ser hvor siden står i søk.
I sesongen skriver den også én ny artikkel i uka med kilder. Funn og forbedringer kommer som en pull request med `ukesrapporter/<dato>.md`. Godkjenn de du er enig i.

## Gå live på olsenskogmann.no

Gjør dette når Olsen har godkjent teksten og punktene i GJOREMAL.md er avklart.
1. Endre i `.github/workflows/pages.yml`:
   `SITE_URL=https://olsenskogmann.no`, `BASE_PATH=` (tom) og `NOINDEX=0`.
   Legg til `cname: olsenskogmann.no` under `peaceiris/actions-gh-pages`.
2. Endre DNS hos domeneleverandøren (der WordPress-siden ligger i dag):
   - `A` @ → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `AAAA` @ → `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
   - `CNAME` www → `andersmathisen7-design.github.io`
3. Gå til **Settings → Pages → Custom domain**, skriv `olsenskogmann.no` og kryss av for **Enforce HTTPS**.
4. Legg siden inn i Google Search Console og send inn `sitemap.xml`. Importer så til Bing Webmaster Tools.
5. Sett nettadressen i Google-bedriftsprofilen til forsiden.

E-posten (Gmail) påvirkes ikke av DNS-endringen.
