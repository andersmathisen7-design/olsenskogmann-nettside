# -*- coding: utf-8 -*-
"""
Alt innhold på nettsiden ligger her. Endre tekst, telefon eller tjenester her,
og kjør `python3 build.py` (eller push til main, så bygges siden automatisk).

Ting merket MÅ SJEKKES er antakelser som Olsen må bekrefte før siden går live.
Se GJOREMAL.md.
"""
import os

# ---------------------------------------------------------------------------
# Adresse og publisering
# ---------------------------------------------------------------------------
# SITE_URL og BASE_PATH settes av GitHub Actions (se .github/workflows/pages.yml).
# Testdomene: https://andersmathisen7-design.github.io/olsenskogmann-nettside
# Når siden går live: SITE_URL=https://olsenskogmann.no og BASE_PATH="" og NOINDEX=0.
SITE_URL = os.environ.get("SITE_URL", "http://localhost:8000").rstrip("/")
BASE_PATH = os.environ.get("BASE_PATH", "").rstrip("/")
# Testsiden skal ikke dukke opp i Google (den ville konkurrert med den ekte siden).
NOINDEX = os.environ.get("NOINDEX", "1") == "1"

# ---------------------------------------------------------------------------
# Firma
# ---------------------------------------------------------------------------
NAME = "Olsen Skogmann"
TAGLINE = "Hage & Bygg"
PHONE = "45502162"
PHONE_DISPLAY = "455 02 162"
EMAIL = "olsenskogmann@gmail.com"
ORGNR = "835 391 752"           # Enkeltpersonforetak, MVA-registrert (Brønnøysund)
BASE_AREA = "Tveita"
POSTCODE = "0669"
CITY = "Oslo"

# Mittanbud: sjekket på profilen 24.10.2026 (org.nr. 835 391 752, 0669 Oslo): 42 vurderinger, 5,0.
MITTANBUD_RATING = "5,0"
MITTANBUD_COUNT = 42
MITTANBUD_URL = "https://mittanbud.no/bedrift/9242603"

# Skjemaet sendes til e-post via FormSubmit (gratis, ingen server).
# Første innsending gir en aktiverings-e-post til adressen. Se README.md.
FORM_EMAIL = EMAIL

# Besøksstatistikk. Lag konto på goatcounter.com og skriv inn navnet, f.eks. "olsenskogmann".
# Tom = ingen telling. Hendelsene er beskrevet øverst i src/assets/app.js.
GOATCOUNTER = ""

# Henvendelsesloggen (Google-ark + Apps Script). Nettapp-adressen som slutter på /exec.
# Tom = skjemaet sender bare e-post, og eiersiden /admin/ viser hvordan den settes opp.
# Se henvendelser/README.md.
LEADS_URL = ""

# Pris (bekreftet av Olsen 17.10.2026: timepris eller fastpris, introduksjonspris 600 kr eks. mva).
# Priser til forbrukere skal vises med mva (prisopplysningsforskriften), derfor står inkl. mva først.
PRICE_HOUR_EX = 600
PRICE_HOUR_INC = 750
PRICE_TEXT = f"{PRICE_HOUR_INC} kr i timen inkl. mva"
# Introduksjonsprisen gjelder til og med 31.12.2026 (Olsen 23.10.2026).
# «795 eks.» er ikke avklart (se GJOREMAL.md), så den står ikke på siden.
PRICE_INTRO_UNTIL = "2026-12-31"       # brukes i strukturerte data (validThrough)
PRICE_INTRO_UNTIL_TEXT = "31.12.2026"
PRICE_INTRO_TEXT = f"introduksjonspris til {PRICE_INTRO_UNTIL_TEXT}"

# Fastpris på løvrydding (Olsen 23.10.2026). Vises på /lovrydding/ og nevnes på forsiden.
# MÅ SJEKKES: Olsen må godkjenne prisene før siden går live.
# price=None betyr pris etter bilde.
PACKAGES = {
    "service": "lovrydding",
    "title": "Fastpris på løvrydding",
    "lead": "Du vet hva det koster før vi starter.",
    "items": [
        {"name": "Liten hage", "for": "Rekkehus eller liten tomt", "time": "Opptil ca. 2 timer", "price": 1490},
        {"name": "Vanlig hage", "for": "Enebolig eller tomannsbolig", "time": "Opptil ca. 4 timer", "price": 2790},
        {"name": "Stor hage", "for": "Større tomter", "time": "Fast pris på forhånd etter bilde på SMS", "price": None},
    ],
    "note": "Alt avfall kjøres bort. Ingen startpris eller kjøregebyr.",
}

# Bydeler og områder nær Tveita. Brukes i teksten om hvor vi jobber.
NEAR_AREAS = ["Tveita", "Hellerud", "Bryn", "Østensjø", "Oppsal", "Manglerud",
              "Haugerud", "Furuset", "Alna", "Lørenskog", "Nordstrand", "Lambertseter"]

# ---------------------------------------------------------------------------
# Sesongtilbud på forsiden. Bytt ut når sesongen skifter (f.eks. vårrydding).
# ---------------------------------------------------------------------------
SEASON = {
    "slug": "lovrydding",
    "tag": "Høstsesong i Oslo",
    "title": "Løvrydding før snøen kommer",
    "lead": "Vi blåser løvet fra plen, bed, terrasse og innkjørsel, og kjører bort alt hageavfallet. "
            "Hekken og buskene kan vi ta i samme runde. Fastpris fra 1 490 kr inkl. mva, "
            "eller 750 kr i timen inkl. mva (introduksjonspris til 31.12.2026).",
}

# ---------------------------------------------------------------------------
# Tjenester. Hver tjeneste får sin egen side på /<slug>/.
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "lovrydding",
        "nav": "Løvrydding",
        "form_value": "Løvrydding",
        "title": "Løvrydding i Oslo",
        "meta_title": "Løvrydding i Oslo | Olsen Skogmann",
        "meta_description": "Løvrydding og høstrydding i Oslo. Vi blåser og raker løv fra plen, bed, terrasse og innkjørsel og tar det med oss. Gratis befaring. Ring 455 02 162.",
        "lead": "Vi blåser og raker løvet fra plen, bed, terrasse, trapper og innkjørsel, og tar det med oss. "
                "For villa, rekkehus, borettslag og bedrifter i hele Oslo.",
        "summary": "Løvblåsing, raking og bortkjøring av løv. For villa, rekkehus, borettslag og bedrifter.",
        "image": None,
        # Bekreftet av Olsen 17.10.2026: kjører alltid bort hageavfall, tar hekk og beskjæring i samme runde.
        "includes": [
            "Løvblåsing av plen, bed og under busker",
            "Terrasse, trapper, gangveier og innkjørsel",
            "Raking og samling av løv",
            "Bortkjøring av alt hageavfall, alltid",
            "Hekkeklipping og beskjæring i samme runde",
            "Felling av mindre trær og fjerning av stubber",
        ],
        "for_whom": [
            ("Villa og rekkehus", "Hele hagen, eller bare plenen og innkjørselen."),
            ("Borettslag og sameier", "Fellesarealer, gangveier og lekeplasser. Én gang eller flere runder gjennom høsten."),
            ("Bedrifter", "Uteområder, parkering og inngangsparti."),
        ],
        "sections": [
            ("Hvorfor fjerne løvet før vinteren?",
             "Løv som blir liggende på plenen under snøen stenger ute lyset og holder på fuktigheten. "
             "Til våren får du ofte døde flekker, mose og snømugg. Vått løv på trapper og gangveier blir også glatt."),
            ("Når er det best?",
             "Når det meste av løvet har falt. I Oslo er det vanligvis fra midten av oktober og fram til snøen kommer. "
             "Har du mange trær, kan det lønne seg med to runder: én nå og én rett før snøen."),
            ("Hva koster det?",
             "Fastpris fra 1 490 kr inkl. mva for en liten hage, se prisene under. Eller 750 kr i timen inkl. mva "
             "(600 kr eks. mva), som er introduksjonspris til 31.12.2026. Send et bilde av hagen på SMS, "
             "så får du en pris. Befaringen er gratis, og du får prisen før vi starter."),
        ],
        "faq": [
            ("Hva koster løvrydding hos dere?",
             "Liten hage (rekkehus eller liten tomt) koster 1 490 kr og vanlig hage (enebolig eller tomannsbolig) 2 790 kr, "
             "inkl. mva. Stor hage får fast pris på forhånd etter bilde på SMS. Alt avfall kjøres bort, og det er ingen startpris "
             "eller kjøregebyr. Du kan også betale per time: 750 kr inkl. mva, introduksjonspris til 31.12.2026."),
            ("Må jeg være hjemme mens dere jobber?",
             "Nei. Vi avtaler dag på forhånd og gir beskjed når vi er ferdige."),
            ("Tar dere med løvet?",
             "Ja, alltid. Vi kjører bort alt hageavfallet, så du slipper sekker i hagen og turer til gjenvinningsstasjonen."),
            ("Kan dere klippe hekken samtidig?",
             "Ja. Hekkeklipping, beskjæring av busker og felling av mindre trær kan vi ta i samme runde."),
            ("Kan dere komme flere ganger i løpet av høsten?",
             "Ja. Mange med store trær tar to runder. Vi avtaler det når vi er der første gang."),
            ("Tar dere oppdrag for borettslag?",
             "Ja. Vi har fast avtale med et borettslag i Oslo i dag og kommer dit to ganger i måneden. Det kan ditt borettslag også få."),
        ],
        "photos": [],
    },
    {
        "slug": "beskjaering-og-trefelling",
        "nav": "Hekk & trær",
        "form_value": "Hekk, beskjæring og trær",
        "title": "Hekkeklipping, beskjæring og trefelling i Oslo",
        "meta_title": "Hekkeklipping, beskjæring og stubbefjerning i Oslo | Olsen Skogmann",
        "meta_description": "Hekkeklipping, beskjæring av busker og frukttrær, felling av mindre trær og fjerning av stubber i Oslo og Lørenskog. Vi kjører bort alt. 750 kr/t inkl. mva.",
        "lead": "Vi klipper hekken, beskjærer busker og frukttrær, feller mindre trær og fjerner stubber, enten med hele roten eller med fres. "
                "Alt kvist og hageavfall kjører vi bort.",
        "summary": "Hekkeklipping, beskjæring, felling av mindre trær og fjerning av stubber.",
        "image": None,
        "panel": "Hekk, busker, små trær og stubber",
        "includes": [
            "Hekkeklipping",
            "Beskjæring av busker og frukttrær",
            "Felling av mindre trær",
            "Stubbefjerning: graving med hele roten, eller fresing",
            "Bortkjøring av alt kvist og hageavfall",
        ],
        "for_whom": [],
        "sections": [
            ("Stubben: grave eller frese?",
             "Skal du plante, legge plen eller stein der stubben sto, er det best å fjerne hele roten. "
             "Skal området bare se ryddig ut, holder det ofte å frese stubben ned under bakken. Vi gjør begge deler."),
            ("Store trær?",
             "Vi feller mindre trær. Store trær nær hus, ledninger eller vei bør felles av en arborist med klatreutstyr eller lift. "
             "Send et bilde, så sier vi ærlig fra om det er en jobb for oss."),
            ("Må du søke?",
             "I Oslo kan større trær være vernet i reguleringsplanen, ofte trær med stammeomkrets over 90 cm målt én meter over bakken. "
             "Det gjelder blant annet i småhusplanen. Vi hjelper deg å sjekke før vi feller noe."),
        ],
        "faq": [
            ("Må jeg søke om å felle et tre i Oslo?",
             "Vanligvis ikke. Men trær kan være vernet i reguleringsplanen, ofte de med stammeomkrets over 90 cm målt én meter over bakken. Da må du søke om dispensasjon. Sjekk eiendommen i Planinnsyn hos Oslo kommune."),
            ("Tar dere med kvisten og stammen?",
             "Ja. Vi kjører alltid bort alt hageavfall."),
            ("Når er det best å beskjære frukttrær?",
             "Epler og pærer beskjæres vanligvis på senvinteren, før knoppene sprekker. Kirsebær og plomme beskjæres helst om sommeren, rett etter høsting."),
            ("Kan dere ta hekken samtidig med løvryddingen?",
             "Ja, og da sparer du en tur."),
        ],
        "photos": [],
    },
    {
        "slug": "borettslag",
        "nav": "Borettslag",
        "form_value": "Fast avtale for borettslag/sameie",
        "title": "Fast avtale for borettslag og sameier",
        "meta_title": "Fast uteavtale for borettslag og sameier i Oslo | Olsen Skogmann",
        "meta_description": "Fast avtale om løvrydding, hekk, rydding og rens av stein for borettslag og sameier i Oslo og Lørenskog. Én kontaktperson og faste besøk. Gratis befaring.",
        "lead": "Vi har i dag fast avtale med et borettslag i Oslo og kommer dit to ganger i måneden. "
                "Det samme kan styret i ditt borettslag eller sameie få: én kontaktperson og faste besøk hele året.",
        "summary": "Faste besøk for uteområdet: løv, hekk, rydding og rens av stein.",
        "image": ("plantekasse-terrasse-oslo", "Plantekasse på felles terrasse, plantet med hortensia og lavendel", [1600, 800]),
        "in_index": False,
        "includes": [
            "Løvrydding høst og vår",
            "Hekkeklipping og beskjæring",
            "Rydding av gangveier, bed og lekeplasser",
            "Rens av belegningsstein, trapper og murer",
            "Benker, plantekasser og små reparasjoner",
            "Bortkjøring av alt hageavfall",
        ],
        "for_whom": [
            ("Borettslag og sameier", "Fellesarealer, gangveier, lekeplasser og bed."),
            ("Bakgårder i indre by", "Plantekasser, bed og steinbelegg som skal holdes i stand."),
            ("Næringseiendom", "Inngangsparti, parkering og grøntarealer."),
        ],
        "sections": [
            ("Hvorfor fast avtale?",
             "Styret slipper å bestille hver jobb for seg og hente nye tilbud. Vi kjenner uteområdet, ser hva som trengs, "
             "og gir beskjed før noe blir et problem."),
            ("Slik kommer vi i gang",
             "Vi tar en gratis befaring med styret, lager en enkel plan for året og gir pris før vi starter."),
        ],
        "faq": [
            ("Hvor ofte kommer dere?",
             "Det avtaler vi med styret. Hos borettslaget vi har i dag, kommer vi to ganger i måneden."),
            ("Kjører dere bort hageavfallet?",
             "Ja, alltid. Styret trenger ikke ordne container eller levering."),
        ],
        "photos": [
            ("plantekasse-terrasse-oslo", "Plantekasse på felles terrasse", [1600, 800]),
        ],
    },
    {
        "slug": "snekker",
        "nav": "Snekker",
        "form_value": "Snekker",
        "title": "Snekker i Oslo",
        "meta_title": "Snekker i Oslo – terrasse, trapp og plantekasser | Olsen Skogmann",
        "meta_description": "Snekkeroppdrag i Oslo: terrasser, utvendige trapper, plantekasser, innvendige løsninger og vedlikehold. Ingen jobb er for liten. Gratis befaring.",
        "lead": "Små og store snekkeroppdrag for privatpersoner, borettslag og bedrifter. "
                "Ingen jobb er for liten.",
        "summary": "Terrasser, utvendige trapper, plantekasser, innvendige løsninger og vedlikehold.",
        "image": ("utvendig-trapp-tre", "Ny utvendig trapp i trykkimpregnert tre ved inngangsparti", [1203, 800]),
        "includes": [
            "Ny terrasse eller utbedring av gammel",
            "Utvendige trapper",
            "Plantekasser og benker",
            "Innvendige løsninger",
            "Vedlikehold og reparasjoner",
        ],
        "for_whom": [],
        "sections": [
            ("Slik jobber vi",
             "Vi ser på jobben sammen med deg, foreslår en løsning og gir deg prisen før vi starter. "
             "Du snakker med den som gjør jobben, hele veien."),
        ],
        "faq": [],
        "photos": [
            ("utvendig-trapp-tre", "Ny utvendig trapp i tre", [1203, 800]),
            ("plantekasse-terrasse-oslo", "Plantekasse i tre på terrasse i borettslag, plantet med hortensia og lavendel", [1600, 800]),
        ],
    },
    {
        "slug": "stein-og-hage",
        "nav": "Stein & hage",
        "form_value": "Stein & hage",
        "title": "Stein og hage i Oslo",
        "meta_title": "Belegningsstein, støttemur og hagearbeid i Oslo | Olsen Skogmann",
        "meta_description": "Belegningsstein, skifer, støttemurer, plantekasser og hagearbeid i Oslo. Gratis befaring. Ring 455 02 162.",
        "lead": "Uteområder som er praktiske og fine å se på. Fra belegningsstein og støttemurer "
                "til beplantning og beskjæring.",
        "summary": "Belegningsstein, skifer, støttemurer, beplantning, beskjæring og rens av mur.",
        "image": ("plantekasse-terrasse-oslo", "Plantekasse i tre på terrasse, plantet med hortensia og lavendel", [1600, 800]),
        "includes": [
            "Belegningsstein og skifer",
            "Støttemurer",
            "Plantekasser og beplantning",
            "Beskjæring og hagearbeid",
            "Rens av stein og mur (egen side)",
        ],
        "for_whom": [],
        "sections": [
            ("Gammel stein som ser ny ut",
             "Ofte trenger ikke steinen å legges om. Alger, mose og skitt kan spyles bort, og mur og belegningsstein blir som nye. Se siden om rens av stein og mur."),
        ],
        "faq": [],
        "photos": [
            ("rens-av-mur-for-etter", "Støttemur i betong: renset til venstre, urenset til høyre", [1600, 800]),
            ("plantekasse-terrasse-oslo", "Plantekasse med hortensia og lavendel", [1600, 800]),
        ],
    },
    {
        "slug": "rens-av-stein",
        "nav": "Rens av stein",
        "form_value": "Rens av stein og mur",
        "title": "Rens av belegningsstein og mur i Oslo",
        "meta_title": "Rens av belegningsstein, mur og trapp i Oslo | Olsen Skogmann",
        "meta_description": "Høytrykkspyling av belegningsstein, skifer, trapper, støttemurer og nedre del av fasaden i Oslo. Fjerner alger, mose og skitt. Gratis befaring.",
        "lead": "Vi spyler bort alger, mose og skitt fra belegningsstein, skifer, trapper, murer og nedre del av fasaden. "
                "Ofte trenger ikke steinen å legges om for å se ny ut.",
        "summary": "Høytrykkspyling av stein, trapper, murer og nedre del av fasaden.",
        "image": ("rens-av-mur-for-etter", "Støttemur i betong: renset til venstre, urenset til høyre", [1600, 800]),
        "in_nav": False,
        "includes": [
            "Belegningsstein og skifer",
            "Trapper og gangveier",
            "Støttemurer og grunnmur",
            "Nedre del av fasaden",
            "Gårdsplass og bakgård",
        ],
        "for_whom": [],
        "sections": [
            ("Før og etter",
             "Bildet viser en støttemur i betong. Venstre del er spylt, høyre del er ikke det."),
            ("Hvorfor rense?",
             "Alger og mose gjør stein og trapper glatte når det er vått, og holder på fuktighet i fugene. Det ser også slitent ut, selv om steinen er hel."),
        ],
        "faq": [
            ("Kan dere vaske hele fasaden?",
             "Vi tar nedre del av fasaden og grunnmuren fra bakken. Hele fasader i høyden tar vi ikke."),
        ],
        "photos": [
            ("rens-av-mur-for-etter", "Støttemur i betong: renset til venstre, urenset til høyre", [1600, 800]),
        ],
    },
]

# Stegene er en ekte rekkefølge, derfor nummerert på siden.
STEPS = [
    ("Send et bilde", "Ring eller send SMS med et bilde av det som skal gjøres. Du kan også bruke skjemaet."),
    ("Gratis befaring", "Vi kommer og ser på jobben, eller gir pris ut fra bildet hvis det holder."),
    ("Pris før oppstart", "Du får prisen før vi begynner, så du vet hva det koster."),
    ("Jobben blir gjort", "Vi gjør jobben og rydder etter oss."),
]

ABOUT = (
    "Olsen Skogmann er et enkeltpersonforetak fra Tveita i Oslo. Du snakker med den som gjør jobben, "
    "fra første telefon til siste rake. Vi tar både små og store oppdrag i hage og bygg, "
    "og ingen jobb er for liten."
)

# ---------------------------------------------------------------------------
# Områdesider: én side per bydel nær Tveita. Tallene er boliger etter bygningstype per 1.1.2025,
# summert fra grunnkretser i Oslo kommunes statistikkbank (tabell BOL001) med SSBs
# grunnkrets→bydel-kobling (Klass 1→103). Rådata: data/smahus-per-bydel-oslo-2025.csv.
# Hver side skal ha egen tekst (ikke bare byttet navn), ellers ser Google den som tynn.
# ---------------------------------------------------------------------------
BOLIG_KILDE = ("Oslo kommune, statistikkbanken, tabell BOL001 (boliger etter bygningstype, 2025)",
               "https://statistikkbanken.oslo.kommune.no/statbank/pxweb/no/db1/db1__Boliger%20og%20byggevirksomhet__Boligmengden/OK-BOL001.px/")
OSLO_SMAHUS = {"boliger": 355915, "smahus": 84186}

AREAS = [
    {
        "slug": "hagearbeid-alna", "bydel": "Alna",
        "stats": {"enebolig": 1008, "tomannsbolig": 917, "rekkehus": 2527, "blokk": 16107, "totalt": 21112},
        "places": ["Tveita", "Hellerud", "Haugerud", "Trosterud", "Teisen", "Bryn", "Furuset", "Ellingsrud", "Lindeberg", "Alfaset"],
        "intro": "Alna er hjemmebydelen vår. Vi holder til på Tveita, så her er kjøreveien kortest og det er lettest å få til en rask befaring.",
        "angle": ("Mest blokk, men mange borettslag med fellesarealer",
                  "Nesten åtte av ti boliger i Alna er i blokk. Det betyr mange borettslag og sameier med plener, gangveier og lekeplasser som skal ryddes for løv hver høst. "
                  "Samtidig er det over 4 400 småhus i bydelen, de fleste rekkehus og kjedehus med små hager."),
    },
    {
        "slug": "hagearbeid-ostensjo", "bydel": "Østensjø",
        "stats": {"enebolig": 2112, "tomannsbolig": 2194, "rekkehus": 4362, "blokk": 13859, "totalt": 23062},
        "places": ["Oppsal", "Manglerud", "Bøler", "Ulsrud", "Godlia", "Bogerud", "Skullerud", "Abildsø", "Rustad", "Trasop"],
        "intro": "Østensjø ligger rett sør for Tveita. Vi tar oppdrag i hele bydelen, fra Godlia og Oppsal til Bøler, Bogerud og Skullerud.",
        "angle": ("Rekkehus og små hager",
                  "Østensjø har 4 362 rekkehus og kjedehus, nesten dobbelt så mange som eneboliger. Mange hager er små, men har hekk, busker og trær som slipper løv på plenen og terrassen. "
                  "Der går en løvrydding fort, og prisen blir deretter."),
    },
    {
        "slug": "hagearbeid-nordstrand", "bydel": "Nordstrand",
        "stats": {"enebolig": 5602, "tomannsbolig": 3505, "rekkehus": 4626, "blokk": 8810, "totalt": 23007},
        "places": ["Nordstrand", "Ljan", "Bekkelaget", "Lambertseter", "Simensbråten", "Ekeberg", "Munkerud", "Ryen", "Karlsrud", "Ormsund"],
        "intro": "Nordstrand er bydelen med flest småhus i Oslo. Vi tar oppdrag fra Ekeberg og Simensbråten til Lambertseter, Bekkelaget og Ljan.",
        "angle": ("Flest småhus i Oslo",
                  "Nordstrand har 13 733 småhus, flere enn noen annen bydel i Oslo, og 5 602 av dem er eneboliger. Det betyr mange store hager. "
                  "Er det mye løv, kan det lønne seg med to runder i høst: én nå og én rett før snøen."),
    },
    {
        "slug": "hagearbeid-sondre-nordstrand", "bydel": "Søndre Nordstrand",
        "stats": {"enebolig": 2271, "tomannsbolig": 697, "rekkehus": 4672, "blokk": 6032, "totalt": 13787},
        "places": ["Holmlia", "Hauketo", "Mortensrud", "Prinsdal", "Bjørndal", "Rosenholm", "Lofsrud", "Bjørnerud", "Gjersrud", "Sloreåsen"],
        "intro": "Vi tar oppdrag i hele Søndre Nordstrand, fra Hauketo og Holmlia til Prinsdal, Mortensrud og Bjørndal.",
        "angle": ("Flest rekkehus i Oslo",
                  "Søndre Nordstrand har 4 672 rekkehus og kjedehus, flere enn noen annen bydel. Over halvparten av boligene i bydelen er småhus. "
                  "Mange bor i rekkehusborettslag der løvryddingen gjøres på fellesarealene. Vi gir pris både til borettslag og til hver enkelt."),
    },
    {
        "slug": "hagearbeid-stovner", "bydel": "Stovner",
        "stats": {"enebolig": 1567, "tomannsbolig": 689, "rekkehus": 2385, "blokk": 7494, "totalt": 12193},
        "places": ["Stovner", "Høybråten", "Vestli", "Rommen", "Fossum", "Tangerud", "Karihaugen", "Stig"],
        "intro": "Vi tar oppdrag i hele Stovner, fra Høybråten og Fossum til Rommen og Vestli.",
        "angle": ("Villaer på Høybråten, rekkehus og blokk lenger nord",
                  "Stovner har 1 567 eneboliger og 2 385 rekkehus og kjedehus. Til sammen er nesten fire av ti boliger i bydelen småhus. "
                  "Vi rydder løv for villaer, rekkehus og borettslag, og gir pris før vi starter."),
    },
    {
        "slug": "hagearbeid-lorenskog", "bydel": "Lørenskog",
        "area_name": "Lørenskog kommune",
        "source": ("SSB, tabell 06265 (boliger etter bygningstype, 2026)", "https://www.ssb.no/statbank/table/06265"),
        "stats": {"enebolig": 5240, "tomannsbolig": 1620, "rekkehus": 3230, "blokk": 11569, "totalt": 22044},
        "places": ["Fjellhamar", "Finstad", "Kurland", "Skårer", "Rasta", "Lørenskog sentrum", "Solheim", "Rolvsrud"],
        "intro": "Lørenskog ligger rett øst for Furuset og Groruddalen, kort vei fra oss på Tveita. Vi tar oppdrag i hele kommunen.",
        "angle": ("Nesten halvparten er småhus",
                  "Lørenskog har 10 090 småhus, 46 prosent av boligene. 5 240 av dem er eneboliger, nesten like mange som i Nordstrand. "
                  "Det betyr mange hager med plen, hekk og trær som skal ryddes hver høst."),
    },
    {
        "slug": "hagearbeid-oslo-sentrum", "bydel": "Oslo sentrum",
        "title": "Bakgård, uteområder og hagearbeid i Oslo sentrum",
        "area_name": "Indre by, Oslo",
        "stats_note": "Frogner, Gamle Oslo, Grünerløkka, St. Hanshaugen, Sagene og Sentrum til sammen.",
        "stats": {"enebolig": 1557, "tomannsbolig": 3729, "rekkehus": 1534, "blokk": 152214, "totalt": 168105},
        "places": ["Frogner", "Majorstuen", "St. Hanshaugen", "Bislett", "Grünerløkka", "Torshov", "Sagene", "Tøyen", "Gamle Oslo", "Sentrum"],
        "intro": "Vi tar oppdrag i hele indre by, for sameier, borettslag og gårdeiere. Mest bakgårder og fellesarealer, men også småhus med hage, for eksempel på Kampen, Vålerenga og Frogner.",
        "angle": ("Bakgårder og sameier",
                  "Bare 4 prosent av boligene i indre by er småhus. Til gjengjeld er det over 150 000 leiligheter i blokk og bygård, "
                  "og mange sameier har bakgård med bed, plantekasser, trær og steinbelegg som skal holdes i stand. "
                  "Vi rydder løv, klipper, spyler stein og bygger plantekasser, og kjører bort alt avfallet."),
    },
]
