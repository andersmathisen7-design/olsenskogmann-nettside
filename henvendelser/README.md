# Henvendelsesloggen og eiersiden /admin/

Hver forespørsel fra skjemaet på nettsiden kommer som før på e-post via FormSubmit, med bilder.
I tillegg kan den lagres som en rad i et Google-regneark. På eiersiden `/admin/` ser Olsen alle henvendelsene og følger dem opp:

**Ny → Kontaktet → Befaring → Tilbud sendt → Vunnet / Tapt**

- **Tall øverst:** nye henvendelser (gul hvis noen har ventet mer enn ett døgn), henvendelser under arbeid, henvendelser siste 30 dager, andel vunnet og vunnet verdi siste 90 dager.
- **Per tjeneste og per kilde:** for eksempel Google, direkte, Mittanbud eller telefon. Da ser dere hva som gir jobber, ikke bare besøk.
- **Per henvendelse:** ring, SMS eller kart med ett trykk, notat («befaring tirsdag kl. 16») og verdi i kroner.
- **Legg inn henvendelser fra telefon, SMS og Mittanbud,** så alt ligger ett sted.

Dette er samme oppsett som leveringskalenderen til Follo Bjørkeved, med samme sikkerhet.

## Sett opp (ca. 5 min, gratis)

1. Lag et nytt Google-regneark med Google-kontoen som skal eie dataene, for eksempel «Olsen Skogmann – henvendelser». Ikke del det med andre enn de som skal se kundedataene.
2. Velg **Utvidelser → Apps Script**. Slett det som står der, lim inn alt fra `henvendelser/henvendelser.gs`, og trykk **lagre**.
3. Velg **Implementer → Ny implementering → tannhjulet → Nettapp**.
   - Kjør som: **Meg**
   - Hvem har tilgang: **Alle**. Det må til for at skjemaet på nettsiden kan legge inn rader. Uten innlogging kan man bare legge til en henvendelse, aldri lese noe.
4. Trykk **Implementer** og godkjenn med Google-kontoen. Google sier at appen «ikke er bekreftet». Det er vanlig for egne skript: velg **Avansert → Gå til … (usikkert)**.
5. Kopier nettapp-adressen (slutter på `/exec`). Lim den inn som `LEADS_URL` i `config.py`, eller send den til Claude.
6. Last regnearket på nytt. Velg **Henvendelser → Lag nytt passord til eiersiden**. Passordet vises **én gang**. Gi det til Olsen og lagre det i en passordbehandler.
7. Olsen åpner `/admin/` på telefonen, logger inn og krysser av for «Husk meg».

## Sikkerhet

- Passordet lagres bare som en saltet SHA-256-sjekksum i skriptets innstillinger, aldri i koden eller GitHub.
- Innlogging gir en tilfeldig billett som varer 12 timer, eller 30 dager med «Husk meg». **Henvendelser → Logg ut alle enheter** gjør alle billetter ugyldige.
- Etter 10 feil passord på 15 minutter stenges innloggingen i 15 minutter.
- Tekst fra skjemaet lagres som ren tekst, så den aldri kan bli en formel i arket.
- Maks 30 nettforespørsler i timen, som vern mot søppel.
- Eiersiden er skjult for Google og har en streng sikkerhetsregel (Content Security Policy).

## Daglig bruk

- **Ny henvendelse:** ring kunden og trykk **Kontaktet**. Henvendelser som har ventet mer enn ett døgn, blir merket gult.
- **Etter befaring eller tilbud:** trykk på status, skriv et notat og legg inn verdien når tilbudet er sendt.
- **Vunnet eller tapt:** trykk på status. Da blir tallene for vunnet riktige.
- **Endre skriptet:** velg **Implementer → Administrer implementeringer → Rediger → Ny versjon**, ellers brukes den gamle koden.

Svarer ikke arket, går henvendelsen likevel fram på e-post.
