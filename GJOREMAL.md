# Gjøremål

## Må sjekkes med Olsen før siden går live
Dette står på siden, men er antakelser. Rett i `config.py` hvis noe er feil.

- [ ] **Tar han med seg løvet?** Siden lover «bortkjøring av løv og hageavfall».
- [ ] **Beskjæring og nedklipping av stauder i samme runde som løvrydding?**
- [ ] **«Du får prisen før vi starter»** står flere steder. Stemmer det, eller tar han timepris?
- [ ] **«Må jeg være hjemme? Nei»**, i FAQ på løvryddingssiden.
- [ ] **Faste runder for borettslag** gjennom høsten.
- [ ] **Mittanbud:** oppdater antall vurderinger (32 fra mai 2026), og lim inn lenken til profilen i `MITTANBUD_URL`.
- [ ] **Områdene** i `NEAR_AREAS`. Er det bydeler han ikke vil kjøre til, eller områder utenfor Oslo han vil ha med?
- [ ] **Fasadevask:** ligger nå bare som «Rens av mur, stein og fasade» under Stein & hage. Er det greit, eller skal det bort?

## Bilder (det som løfter siden mest)
- [ ] **Bilder fra løvjobber nå i høst**, før og etter fra samme vinkel. Løvryddingssiden har ingen bilder i dag.
- [ ] Bilde av ham med løvblåser, til toppen av forsiden. Dagens bilde er fra en sommerjobb.
- [ ] Bilder av terrasser og belegningsstein han har laget.
- Send bildene rett fra telefonen. Byggeskriptet tar ikke bort GPS, så kjør dem gjennom samme behandling som de første (se `src/img/`).

## Utenfor nettsiden (gir mest kunder)
- [ ] **Google-bedriftsprofil**, hvis han ikke har det. Primærkategori er den viktigste faktoren for kartresultatene (Whitespark 2026). Forslag: «Hagearbeider» (Gardener) som primær, med «Snekker» og «Anleggsgartner» som sekundære.
- [ ] Be faste kunder fra Mittanbud om en Google-anmeldelse også. Google viser ikke Mittanbud-vurderingene.
- [ ] Flyers i postkasser i villa- og rekkehusstrøk nær Tveita med teksten «Løvrydding før snøen kommer» og telefonnummeret.

## Senere
- [ ] Domene (vent til siden har vært ute en stund).
- [ ] Besøksstatistikk med GoatCounter (`GOATCOUNTER` i `config.py`). Knappene for ring og SMS er allerede merket.
- [ ] Vårsesong: bytt `SEASON` til vårrydding og lag en egen side for det.
