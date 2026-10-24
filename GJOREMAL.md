# Gjøremål

## Anders – nå
1. **Opprett repoet** `olsenskogmann-nettside` (tomt, offentlig) på andersmathisen7-design. Claude pusher koden.
2. **Settings → Pages:** branch `gh-pages`, mappe `/ (root)`, når første publisering er ferdig.
3. [x] **GoatCounter** er på (24.10.2026): https://olsenskogmann.goatcounter.com. Gjenstår: bekreft e-posten fra GoatCounter, og lag en API-nøkkel med lesetilgang (Settings → API). Legg den inn som `OLSEN_GOATCOUNTER_TOKEN` i miljøet til den ukentlige rutinen, ikke i repoet.
4. **Henvendelsesloggen:** følg [henvendelser/README.md](henvendelser/README.md) (ca. 5 min). Lim nettapp-adressen inn som `LEADS_URL`, og gi passordet til Olsen.
5. **FormSubmit:** send én testforespørsel fra testsiden, og be Olsen klikke **Activate** i e-posten.

## Svar fra Olsen (17.10.2026) – lagt inn på siden
- [x] Kjører alltid bort alt hageavfall.
- [x] Timepris eller fastpris. Introduksjonspris 600 kr eks. mva, vist som **750 kr/t inkl. mva** (prisopplysningsforskriften krever pris med mva til forbrukere).
- [x] Hekkeklipping og beskjæring i samme runde, feller mindre trær, fjerner stubber med hele roten eller fres. Ny side: `/beskjaering-og-trefelling/`.
- [x] Fast avtale med et borettslag (to besøk i måneden). Ny side: `/borettslag/`.
- [x] Kunden trenger ikke være hjemme.
- [x] Lørenskog og hele Oslo sentrum. Nye sider: `/hagearbeid-lorenskog/` og `/hagearbeid-oslo-sentrum/`.
- [x] Høytrykkspyling av stein og nedre del av fasaden. Ny side: `/rens-av-stein/`.

## Svar fra Olsen (23.10.2026)
- [x] **Introduksjonsprisen** (750 kr/t inkl. mva, 600 eks.) gjelder til 31.12.2026. Står nå på forsiden, `/lovrydding/`, i pris-FAQ, artikkelen om pris og `llms.txt`. Strukturerte data har `validThrough: 2026-12-31`.
- [x] **Fastpris er greit.** Pakker for løvrydding står på `/lovrydding/` (`PACKAGES` i `config.py`) og «fra 1 490 kr» på forsiden: liten hage 1 490 kr, vanlig hage 2 790 kr, stor hage etter bilde. Alt avfall kjøres bort, ingen startpris eller kjøregebyr.
- [x] **Mittanbud:** profilen er https://mittanbud.no/bedrift/9242603 (sjekket 24.10.2026: org.nr. og 0669 Oslo stemmer). 42 vurderinger, 5,0. Lagt inn.
- [x] **795 kr eks. mva** er vanlig timepris fra 1.1.2027 (993,75 kr inkl. mva). Står i pris-FAQ, på `/lovrydding/` og i `llms.txt`.
- [x] **Pakkeprisene** (1 490 og 2 790 kr inkl. mva) er godkjent.
- [x] **Google-bedriftsprofil:** han har allerede en.
- [x] **Borettslaget:** Olsen foreslo å finne på et navn og et sitat. Det gjør vi ikke. Oppdiktede kundeuttalelser er ulovlig etter markedsføringsloven. Siden sier bare det som er sant: fast avtale med et borettslag i Oslo, besøk to ganger i måneden.
- [ ] **Terrassebilde** (IMG_20260616_150237_825.jpg) kom på e-post, men kunne ikke lastes ned med verktøyene her. Lagre det i `/tmp/olsen-img/`, så fjerner Claude GPS-data og legger det på `/snekker/`.

## Fortsatt åpent
- [ ] **31.12.2026: bytt til vanlig timepris.** Introduksjonsprisen står mange steder (config.py, FAQ, `priceRange`, `llms.txt`). Siden bygges bare ved push, så prisen må endres i `config.py` og pushes før 1.1.2027. Ellers viser Google og KI-søk feil pris.
- [ ] **Lenken til Google-profilen:** be Olsen om den (Google Maps → Del → Kopier lenke), og legg den inn i `PROFILES` i `config.py`.
- [ ] **«Om Olsen»-side:** KI-søk og Google stoler mer på en bedrift når det står hvem som gjør jobben. Spør Olsen om fornavn, hvor lenge han har drevet med hage og bygg, hva han gjorde før, og om vi kan bruke et bilde av ham. Bare det han bekrefter kommer på siden.
- [ ] **Før- og etterbilder fra løvjobber** (se under).
- [ ] **Google-profilen:** Olsen gjør alt selv (vi ber ikke om admin-tilgang). Sjekkliste sendt på e-post 24.10.2026: kategori, tjenesteområde, beskrivelse, tjenester, bilder, innlegg, anmeldelser og ny timepris 1.1.2027.

## Bilder (det som løfter siden mest)
- [ ] **Før- og etterbilder fra løvjobber i høst**, tatt fra samme vinkel. Løvryddingssiden har ingen bilder i dag.
- [ ] Et bilde av ham med løvblåser, til toppen av forsiden. Dagens bilde er fra en sommerjobb.
- [ ] Bilder av terrasser og belegningsstein han har laget.
- Bildene må få fjernet GPS-data før de legges ut (se hvordan i `src/img/`). Claude gjør det hvis bildene sendes hit.

## Utenfor nettsiden (gir mest kunder)
1. **Google-bedriftsprofil.** Olsen har allerede en (svar 23.10.2026) og gjør endringene selv. Den bør være satt opp slik:
   - **Navn:** «Olsen Skogmann», som i Brønnøysund. Ikke legg til søkeord i navnet.
   - **Primærkategori:** «Hagearbeider» (Gardener). **Tilleggskategorier:** «Snekker» og «Anleggsgartner». Primærkategorien er den viktigste faktoren for kartresultatene (Whitespark 2026).
   - **Adresse:** skjult. Han kjører ut og har ikke butikk.
   - **Tjenesteområde:** Alna, Østensjø, Nordstrand, Søndre Nordstrand, Stovner, Oslo sentrum og Lørenskog.
   - **Telefon:** 455 02 162. **Nettside:** olsenskogmann.no.
   - **Etterpå:** 10+ bilder av jobber, tjenestene med kort tekst, ett innlegg i uka i sesongen («Ledig for løvrydding neste uke»), og svar på alle anmeldelser. Tekstene står i UTKAST.md.
2. **Google-anmeldelser:** send en SMS med lenke til alle som har vært fornøyd. Mittanbud-vurderingene vises ikke på Google. Mål: 20 før jul.
3. **Flyers** i småhusstrøk nær Tveita (Østensjø, Hellerud, Haugerud). Tekst: «Løvrydding før snøen kommer», telefonnummer og «Send et bilde på SMS». Bruk `?utm_source=flyer` på en QR-kode, så ser vi i GoatCounter og på eiersiden hvor mange som kom fra flyeren.
4. **Borettslag:** e-post til styrene i rekkehusborettslag i Østensjø og Søndre Nordstrand med pris på løvrydding av fellesarealer.
5. **Kataloger og lenker:** se [LENKEBYGGING.md](LENKEBYGGING.md).

## Senere
- [x] Live på olsenskogmann.no 24.10.2026. DNS hos Proisp peker til GitHub Pages, HTTPS er på. Search Console (andersmathisen7-kontoen) er bekreftet med HTML-fil, sitemap er sendt inn (19 sider), og forsiden og `/lovrydding/` er sendt til indeksering.
- [ ] **Bing Webmaster Tools:** importer fra Search Console (5 min). ChatGPT-søk og Copilot bygger på Bing, så dette er det viktigste for KI-søk.
- [ ] **Apple Business Connect:** gjør krav på firmaet i Apple Maps (gratis, se LENKEBYGGING.md).
- [ ] Legg olsenskogmann.no inn som nettside i Google-bedriftsprofilen.
- [ ] Si opp webhotellet hos Proisp når alt har virket en stund (domenet må beholdes).
- [ ] Vårsesong (mars): bytt `SEASON` til vårrydding og lag en side for det. Skriv artikler om terrasse og belegningsstein før byggesesongen.
- [ ] Flere bydelssider (Lørenskog, Rælingen, Grorud) hvis Olsen vil kjøre dit.

## Hver mandag
- Les rapporten fra den ukentlige jobben, og godkjenn forslagene (PR) du er enig i.
