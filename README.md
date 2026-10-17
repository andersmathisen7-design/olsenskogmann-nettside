# Olsen Skogmann – ny nettside (testversjon)

Dette er en rask, statisk nettside for Olsen Skogmann – Hage & Bygg i Oslo. Den skal gi henvendelser fra Google og fra mobil.
Akkurat nå er **løvrydding** sesongtilbudet øverst på forsiden. Snekker og Stein & hage er faste tjenester.

**Test:** https://andersmathisen7-design.github.io/olsenskogmann-nettside/
Testsiden er skjult for Google med `noindex` og `robots.txt`, så den ikke konkurrerer med olsenskogmann.no.

Det som må avklares med Olsen før siden går live, står i **[GJOREMAL.md](GJOREMAL.md)**.

## Innhold

| Side | Mål i søk |
|---|---|
| `/` | «hagearbeid Oslo», «løvrydding Oslo», navnet |
| `/lovrydding/` | «løvrydding Oslo», «løvblåsing», «høstrydding hage». Har FAQ med strukturerte data |
| `/snekker/` | «snekker Oslo», «bygge terrasse», «utvendig trapp» |
| `/stein-og-hage/` | «belegningsstein Oslo», «støttemur», «beskjæring» |
| `/takk/` | Takkeside etter skjema. Kan brukes til å måle konverteringer i Google Ads |
| `/llms.txt` | Faktaark for AI-søk (ChatGPT, Perplexity) |

Valgene bak siden:
- **Én tydelig sak øverst.** Sesongtilbudet ligger i `SEASON` i `config.py` og byttes når sesongen skifter, for eksempel til vårrydding.
- **Tjenestene har egne sider.** Google rangerer én side per tema. Én side med alt rangerer dårlig på alt.
- **Ring og SMS er alltid synlige på mobil.** Over halvparten av trafikken i Norge er mobil (StatCounter, september 2026: 51,5 %).
- **Vurderingene fra Mittanbud står helt øverst.** 47 % velger bort en bedrift med under 20 vurderinger (BrightLocal 2026). Olsen har 32 med snitt 5,0.
- **Bildene har ikke GPS-data.** Originalbildene på dagens side har posisjonen der bildet ble tatt, ofte hos kunden. Den er fjernet her.
- Siden er ren HTML og CSS uten JavaScript og uten WordPress. Fontene ligger lokalt, og ingenting lastes fra Google, så det trengs ikke samtykkebanner.
- Strukturerte data (JSON-LD) med `HomeAndConstructionBusiness`, `Service`, `BreadcrumbList` og `FAQPage`.

## Endre tekst

Alt innhold ligger i **`config.py`**: telefon, tjenester, punktlister, FAQ og sesongtilbud. Design ligger i `src/assets/style.css`.

```bash
python3 build.py                                   # bygger til public/
cd public && python3 -m http.server 8000           # se siden på http://localhost:8000
```

Hver push til `main` bygger siden og publiserer den på `gh-pages`-branchen med GitHub Actions.

### Første gang: slå på GitHub Pages
1. Push til `main`, og vent til workflowen «Publiser nettsiden» er grønn under **Actions**.
2. Gå til **Settings → Pages**. Velg **Deploy from a branch**, branch `gh-pages` og mappe `/ (root)`.
3. Etter et minutt er siden på adressen over.

## Skjema på e-post

Skjemaet sender til `FORM_EMAIL` i `config.py` gjennom [FormSubmit](https://formsubmit.co). Det er gratis og trenger ingen server. Kunden kan legge ved bilder.
1. Send én testforespørsel fra siden.
2. FormSubmit sender en aktiverings-e-post til olsenskogmann@gmail.com. Klikk **Activate**.
3. Etter det kommer hver forespørsel som en e-post med tabell og eventuelle bilder.
4. Anbefalt: bytt e-postadressen i `FORM_EMAIL` med koden fra aktiverings-e-posten. Da vises ikke adressen i kildekoden.

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
4. Legg siden inn i Google Search Console og send inn `sitemap.xml`.
5. Sett nettadressen i Google-bedriftsprofilen til den aktuelle tjenestesiden, for eksempel `/lovrydding/` i sesongen.

E-posten (Gmail) påvirkes ikke av DNS-endringen.
