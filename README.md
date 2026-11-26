# Olsen Skogmann – ny nettside (testversjon)

Dette er en rask, statisk nettside for Olsen Skogmann – Hage & Bygg i Oslo. Den er bygget for lokalt søk på Google og for KI-søk som ChatGPT og Perplexity.
Oppsettet er det samme som på follobjorkeved.no: Python-bygg, innholdet i `config.py` og `innhold.json`, artikler i Markdown, FormSubmit, GoatCounter og publisering med GitHub Actions.

**Test:** https://andersmathisen7-design.github.io/olsenskogmann-nettside/
Testsiden er skjult for Google med `noindex` og `robots.txt`, så den ikke konkurrerer med olsenskogmann.no.

- Markedsanalyse og søkeord med tall og kilder: **[ANALYSE.md](ANALYSE.md)**
- Kataloger og lenker: **[LENKEBYGGING.md](LENKEBYGGING.md)**
- Det som må gjøres eller avklares: **[GJOREMAL.md](GJOREMAL.md)**
- Henvendelsesloggen og eiersiden: **[henvendelser/README.md](henvendelser/README.md)**

## Innhold

| Side | Mål i søk |
|---|---|
| `/` | «hagearbeid Oslo», navnet. Generell tekst øverst (`SEASON`), så alle tjenestene som kort, to per rad |
| `/lovrydding/` | «løvrydding Oslo», «løvblåsing», «høstrydding hage». FAQ med strukturerte data |
| `/snekker/` | «snekker Oslo», «bygge terrasse», «utvendig trapp» |
| `/beskjaering-og-trefelling/` | «hekkeklipping Oslo», «beskjæring», «felle tre», «fjerne stubbe», «stubbefresing» |
| `/priser/` | «løvrydding pris», «hagearbeid pris Oslo» og KI-spørsmål om hva det koster. Alle priser på ett sted, med FAQ. Timeprisen bytter av seg selv 1.1.2027 |
| `/borettslag/` | Styrer i borettslag og sameier: fast avtale for uteområdet |
| `/riving/` | «riving Oslo», «rive terrasse», «innvendig riving» |
| `/stein-og-hage/` | «belegningsstein Oslo», «støttemur» |
| `/rens-av-stein/` | «rens av belegningsstein», «spyle stein», «fjerne mose på stein» |
| `/hagearbeid-alna/`, `/hagearbeid-ostensjo/`, `/hagearbeid-nordstrand/`, `/hagearbeid-sondre-nordstrand/`, `/hagearbeid-stovner/`, `/hagearbeid-lorenskog/`, `/hagearbeid-oslo-sentrum/` | «hagearbeid/løvrydding + bydel». Hver side har egne boligtall fra Oslo kommune og egen tekst, og FAQ med pris og borettslag (`area_faq` i `build.py`, egne spørsmål med `faq` i `AREAS`). Skjemaet vet hvilken bydel kunden kom fra |
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
- **Én tydelig sak øverst.** Sesongtilbudet ligger i `SEASON` i `innhold.json`. Bytt det når sesongen skifter, for eksempel til vårrydding.
- **Egne sider per tjeneste og bydel.** Google rangerer én side per tema.
- **Menyen følger med når man ruller**, med en Kontakt-knapp og telefon i menyen. 51,5 % av trafikken i Norge er mobil (StatCounter, september 2026).
- **Vurderingene fra Mittanbud står øverst.** 47 % velger bort en bedrift med under 20 vurderinger (BrightLocal 2026).

## Ønsker fra Olsen som gjelder videre (20.11.2026)

Disse gjelder foran eldre instrukser, også i den ukentlige SEO-oppgaven:
- **Priser står som tall, uten ordene «inkl. mva»** (tallene er med mva, slik loven krever). Ikke legg til «inkl. mva» eller «eks. mva» igjen.
- **Borettslag er ikke fokus.** Siden er tatt bort (videresender til forsiden); lag ikke nytt innhold rettet mot borettslag.
- **Vurderingene fra kunder** (`REVIEWS` i `innhold.json`) er ekte sitater som Olsen har sendt. Ikke endre dem, og ikke legg til nye uten at Olsen har sendt dem.

## Ønsker fra Olsen 26.11.2026 (gjelder videre)

- **Ingen «der du bor» på de seks tjenestene.** Lenkene til bydelssidene står bare på undersiden Løvrydding (`service_areas` i
  `build.py`), fordi bydelssidene handler om løvrydding og hagearbeid.
- **Stripa med vurderinger og gratis befaring står bare på forsiden**, ikke på Hage.
- **Snekker har to lister:** innvendig og utvendig snekkerarbeid (`include_groups` i `innhold.json`). Listene for Snekker,
  Riving og Betong & mur er Olsens egne ord; ikke skriv dem om.
- **Bilder fra Olsen:** Hage (bedet og løvblåseren), Fasadevask (belegningsstein), Sveising (porten) og Betong & mur (armeringen).

## Ønsker fra Olsen 24.11.2026 (gjelder videre)

- **Bare seks tjenester** i menyen, på forsiden, i skjemaet og nederst, i denne rekkefølgen: Snekker, Betong & mur, Sveising,
  Riving, Hage, Fasadevask (`MAIN_SERVICES` i `config.py`). Fasadevask er siden `/rens-av-stein/`. Løvrydding og Hekk & trær
  står videre som undersider av Hage (`"main": false`), fordi artiklene og fastprisen peker dit. Stein og hage er tatt bort.
- **Ett bilde per tjeneste.** Snekker: den nye terrassen; Hage: plantekassen; Fasadevask: skiferterrassen; Riving: Olsen som
  pigger betong.
- **Forsiden:** Olsens bilde av grunnarbeid i full bredde som bakgrunn som toner over i hvitt. «Vi rydder etter oss» er tatt bort.

## Ønsker fra Olsen 23.11.2026 (gjelder videre)
- **Snømåking og drenering er tatt helt bort.** Ikke legg dem til igjen, verken som side, i skjemaet, i menyen, i bunnen eller i artikler. `/snomaking/` og `/drenering/` videresender til tjenestene på forsiden (`REMOVED_PAGES` i `config.py`).
- **Riving** er en egen tjeneste (`/riving/`).
- Menyen er Hage, Snekker, Betong & mur, Sveising, Riving og Kontakt. Menyen er sticky. Det er ingen fast Ring/SMS-stripe nederst på mobil.
- Ingen sesongtilbud øverst og ingen «Lokal i Oslo øst»/«Her jobber vi» på forsiden. Toppen er hvit med gule detaljer og en generell tekst: «Vi utfører tjenester innen … i Oslo og omegn».
- Forsiden viser alle tjenestene i `SERVICES` som kort med lite bilde og kort tekst, to per rad. Samme liste står i skjemaet og nederst på siden.

## Sesong og bredde (Anders 23.11.2026, gjelder videre)
- **Forsiden viser alltid alle tjenestene.** En kunde lurte på om Olsen bare levde av løvblåsing, fordi toppen handlet om løvrydding. Én sterk side per tjeneste, aldri ett nettsted per tjeneste.
- **Rekkefølgen på kortene følger sesongen** (`SEASONS` og `by_season` i `config.py`): i sesong først, så det som går hele året, så resten. Ingen sesongtilbud øverst (Olsens ønske 23.11.2026). Workflowen bygger siden på nytt den 1. hver måned, så rekkefølgen bytter av seg selv.
- **Innhold kommer før sesongen.** Google bruker uker på å rangere nytt innhold: den ukentlige SEO-økta skriver artikler om tjenesten som har sesong om 1–2 måneder (desember–januar: trefelling og beskjæring; februar–mars: vårrydding, hekk og stein; august: løvrydding), ikke om den som er over.

## Endre tekst

Tekstene på siden (teksten øverst på forsiden, fastpris på løvrydding, tjenester med FAQ, stegene, «om oss» og bydelssidene) ligger i **`innhold.json`**. Telefon, e-post, org.nr., timepris og alt annet ligger i **`config.py`**.

**Endringer Olsen ber om på e-post** gjør Nettsideferdig i `innhold.json`, og ingen andre filer: koden sjekker at bare tekst endres (aldri tall, adresser eller bilder), Olsen ser hva som endres og publiserer selv med lenken i e-posten, og koden lagrer fila her på `main`. `{PRICE_SHORT}`, `{PRICE_HOUR_SENTENCE}` og `{PRICE_HOUR_INC_TEXT}` i teksten byttes med timeprisen fra `config.py`. `python3 test_innhold.py` sjekker fila. Design ligger i `src/assets/style.css`.

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

### Tall agentene kan lese (fra 19.11.2026)

Siden laster også `t.js` fra Nettsideferdig-workeren (`STATS_URL` og `STATS_SITE` i `config.py`). Den teller
visninger per side og kilde (Google, Bing, Facebook, AI-chatene som `ai:chatgpt`, annonser) og klikk på
telefon (`tel`), SMS (`sms`), e-post (`mailto`), sendt skjema (`skjema`) og skjema nettleseren stoppet
(`skjema_stopp`). Bare summer per døgn, ingen cookies. Den ukentlige jobben og alle andre agenter henter tallene slik:

```
curl -s -H "Authorization: Bearer $AGENT_TOKEN" "https://sidefabrikken.nettsideferdig.workers.dev/agent/besok?site=olsenskogmann&dager=28"
```

GoatCounter står på som før og har de detaljerte hendelsene (hvor på siden det ble trykket).

## Ukentlig overvåking

En planlagt jobb kjører hver mandag morgen. Den sjekker at alle sider svarer, at lenker og JSON-LD er gyldige og at skjemaet virker (med falsk FormSubmit). Den henter besøkstall fra workeren (`/agent/besok`, se over) og fra GoatCounter når nøkkelen er satt opp, og ser hvor siden står i søk.
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
