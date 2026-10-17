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

# Mittanbud: tallene er hentet fra skjermbildet på dagens nettside (mai 2026).
# MÅ SJEKKES: oppdater tallene og lim inn lenken til profilen.
MITTANBUD_RATING = "5,0"
MITTANBUD_COUNT = 32
MITTANBUD_URL = ""  # f.eks. "https://mittanbud.no/profil/....."

# Skjemaet sendes til e-post via FormSubmit (gratis, ingen server).
# Første innsending gir en aktiverings-e-post til adressen. Se README.md.
FORM_EMAIL = EMAIL

# Besøksstatistikk (valgfritt). Lag konto på goatcounter.com og skriv inn navnet, f.eks. "olsenskogmann".
GOATCOUNTER = ""

# Bydeler og områder nær Tveita. Brukes i teksten om hvor vi jobber.
NEAR_AREAS = ["Tveita", "Hellerud", "Bryn", "Østensjø", "Oppsal", "Manglerud",
              "Haugerud", "Furuset", "Alna", "Groruddalen", "Nordstrand", "Lambertseter"]

# ---------------------------------------------------------------------------
# Sesongtilbud på forsiden. Bytt ut når sesongen skifter (f.eks. vårrydding).
# ---------------------------------------------------------------------------
SEASON = {
    "slug": "lovrydding",
    "tag": "Høstsesong i Oslo",
    "title": "Løvrydding før snøen kommer",
    "lead": "Vi blåser løvet fra plen, bed, terrasse og innkjørsel, samler det og tar det med oss. "
            "Du får prisen før vi starter.",
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
        # MÅ SJEKKES: at Olsen tar med seg løvet, og at han kan ta beskjæring/nedklipping i samme runde.
        "includes": [
            "Løvblåsing av plen, bed og under busker",
            "Terrasse, trapper, gangveier og innkjørsel",
            "Raking og samling av løv",
            "Bortkjøring av løv og hageavfall",
            "Nedklipping av stauder og beskjæring av busker, hvis du vil",
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
             "Det kommer an på hvor stort området er og hvor mye løv det er. Send et bilde av hagen på SMS, "
             "så får du en pris. Befaringen er gratis, og du får prisen før vi starter."),
        ],
        "faq": [
            ("Må jeg være hjemme mens dere jobber?",
             "Nei, ikke hvis vi kommer til hagen. Vi avtaler dag og tid på forhånd og gir beskjed når vi er ferdige."),
            ("Tar dere med løvet?",
             "Ja. Vi samler løvet og kjører det bort, så du slipper sekker i hagen."),
            ("Kan dere komme flere ganger i løpet av høsten?",
             "Ja. Mange med store trær tar to runder. Vi avtaler det når vi er der første gang."),
            ("Tar dere oppdrag for borettslag?",
             "Ja. Vi gir pris på fellesarealer og kan komme fast gjennom høsten."),
        ],
        "photos": [],
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
        "meta_description": "Belegningsstein, skifer, støttemurer, plantekasser, beskjæring og hagearbeid i Oslo. Også rens av mur og stein. Gratis befaring.",
        "lead": "Uteområder som er praktiske og fine å se på. Fra belegningsstein og støttemurer "
                "til beplantning og beskjæring.",
        "summary": "Belegningsstein, skifer, støttemurer, beplantning, beskjæring og rens av mur.",
        "image": ("plantekasse-terrasse-oslo", "Plantekasse i tre på terrasse, plantet med hortensia og lavendel", [1600, 800]),
        "includes": [
            "Belegningsstein og skifer",
            "Støttemurer",
            "Plantekasser og beplantning",
            "Beskjæring og hagearbeid",
            "Rens av mur, stein og fasade",
        ],
        "for_whom": [],
        "sections": [
            ("Rens av mur og stein",
             "Alger og skitt gjør mur og stein grå og glatt. Bildet viser en støttemur der venstre del er renset og høyre del ikke er det."),
        ],
        "faq": [],
        "photos": [
            ("rens-av-mur-for-etter", "Støttemur i betong: renset til venstre, urenset til høyre", [1600, 800]),
            ("plantekasse-terrasse-oslo", "Plantekasse med hortensia og lavendel", [1600, 800]),
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
