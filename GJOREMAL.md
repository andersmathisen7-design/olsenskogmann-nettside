# Gjøremål

## Anders – nå
1. **Opprett repoet** `olsenskogmann-nettside` (tomt, offentlig) på andersmathisen7-design. Claude pusher koden.
2. **Settings → Pages:** branch `gh-pages`, mappe `/ (root)`, når første publisering er ferdig.
3. **GoatCounter:** lag siden `olsenskogmann` på [goatcounter.com](https://www.goatcounter.com), og sett `GOATCOUNTER = "olsenskogmann"` i `config.py`. Lag en API-nøkkel med lesetilgang til den ukentlige jobben.
4. **Henvendelsesloggen:** følg [henvendelser/README.md](henvendelser/README.md) (ca. 5 min). Lim nettapp-adressen inn som `LEADS_URL`, og gi passordet til Olsen.
5. **FormSubmit:** send én testforespørsel fra testsiden, og be Olsen klikke **Activate** i e-posten.

## Må sjekkes med Olsen før siden går live
Dette står på siden, men er antakelser. Rett i `config.py` hvis noe er feil.

- [ ] **Tar han med seg løvet?** Siden lover «bortkjøring av løv og hageavfall».
- [ ] **Beskjæring og nedklipping av stauder i samme runde som løvrydding?**
- [ ] **«Du får prisen før vi starter»** står flere steder. Stemmer det, eller tar han timepris?
- [ ] **«Må jeg være hjemme? Nei»** i FAQ på løvryddingssiden.
- [ ] **Faste runder for borettslag** gjennom høsten.
- [ ] **Bydelene:** tar han gjerne oppdrag i Alna, Østensjø, Nordstrand, Søndre Nordstrand og Stovner? Andre han vil ha med (Lørenskog, Rælingen)?
- [ ] **Mittanbud:** oppdater antall vurderinger (32 fra mai 2026), og lim inn lenken til profilen i `MITTANBUD_URL`.
- [ ] **Fasadevask:** står nå bare som «Rens av mur, stein og fasade» under Stein & hage. Er det greit?
- [ ] **Hans egne priser.** Artikkelen om pris på løvrydding bruker markedspriser. Har han en timepris eller fra-pris han vil vise? En pris på siden gir ofte flere henvendelser.

## Bilder (det som løfter siden mest)
- [ ] **Før- og etterbilder fra løvjobber i høst**, tatt fra samme vinkel. Løvryddingssiden har ingen bilder i dag.
- [ ] Et bilde av ham med løvblåser, til toppen av forsiden. Dagens bilde er fra en sommerjobb.
- [ ] Bilder av terrasser og belegningsstein han har laget.
- Bildene må få fjernet GPS-data før de legges ut (se hvordan i `src/img/`). Claude gjør det hvis bildene sendes hit.

## Utenfor nettsiden (gir mest kunder)
1. **Google-bedriftsprofil** (ca. 20 min + bekreftelse). Den avgjør om han vises i kartet når noen søker «løvrydding» eller «hagearbeid» i nærheten.
   - Gå til https://business.google.com og logg inn med Olsens Google-konto.
   - **Navn:** «Olsen Skogmann», som i Brønnøysund. Ikke legg til søkeord i navnet.
   - **Primærkategori:** «Hagearbeider» (Gardener). **Tilleggskategorier:** «Snekker» og «Anleggsgartner». Primærkategorien er den viktigste faktoren for kartresultatene (Whitespark 2026).
   - **Adresse:** legg inn adressen, men velg å **skjule** den. Han kjører ut og har ikke butikk.
   - **Tjenesteområde:** Alna, Østensjø, Nordstrand, Søndre Nordstrand, Stovner og resten av Oslo.
   - **Telefon:** 455 02 162. **Nettside:** olsenskogmann.no.
   - **Etterpå:** 10+ bilder av jobber, tjenestene med kort tekst, ett innlegg i uka i sesongen («Ledig for løvrydding neste uke»), og svar på alle anmeldelser.
2. **Google-anmeldelser:** send en SMS med lenke til alle som har vært fornøyd. Mittanbud-vurderingene vises ikke på Google. Mål: 20 før jul.
3. **Flyers** i småhusstrøk nær Tveita (Østensjø, Hellerud, Haugerud). Tekst: «Løvrydding før snøen kommer», telefonnummer og «Send et bilde på SMS». Bruk `?utm_source=flyer` på en QR-kode, så ser vi i GoatCounter og på eiersiden hvor mange som kom fra flyeren.
4. **Borettslag:** e-post til styrene i rekkehusborettslag i Østensjø og Søndre Nordstrand med pris på løvrydding av fellesarealer.
5. **Kataloger og lenker:** se [LENKEBYGGING.md](LENKEBYGGING.md).

## Senere
- [ ] Gå live på olsenskogmann.no (README.md, «Gå live»). Deretter Search Console og Bing Webmaster Tools.
- [ ] Vårsesong (mars): bytt `SEASON` til vårrydding og lag en side for det. Skriv artikler om terrasse og belegningsstein før byggesesongen.
- [ ] Flere bydelssider (Lørenskog, Rælingen, Grorud) hvis Olsen vil kjøre dit.

## Hver mandag
- Les rapporten fra den ukentlige jobben, og godkjenn forslagene (PR) du er enig i.
