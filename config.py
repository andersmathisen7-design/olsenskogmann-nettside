# -*- coding: utf-8 -*-
"""
Alt innhold på nettsiden ligger her. Endre tekst, telefon eller tjenester her,
og kjør `python3 build.py` (eller push til main, så bygges siden automatisk).

Ting merket MÅ SJEKKES er antakelser som Olsen må bekrefte før siden går live.
Se GJOREMAL.md.
"""
import json
import os
from datetime import date, datetime
from zoneinfo import ZoneInfo

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

# Mittanbud: sjekket på profilen 24.10.2026 (org.nr. 835 391 752, 0669 Oslo): 42 vurderinger. Snitt 4,9 (Olsen 20.11.2026).
# Google: 5 av 5 (Olsen 20.11.2026).
GOOGLE_RATING = "5"
MITTANBUD_RATING = "4,9"
MITTANBUD_COUNT = 42
MITTANBUD_URL = "https://mittanbud.no/bedrift/9242603"

# Profiler på andre nettsteder. Brukes i sameAs og i llms.txt, så Google og KI-søk ser at det er samme firma.
# Legg til lenken til Google-bedriftsprofilen (Del → Kopier lenke i Google Maps), Gule Sider, 1881 osv.
# når de er på plass. Bare profiler med samme navn, telefon og org.nr. som her.
PROFILES = [
    ("Mittanbud", MITTANBUD_URL),
    ("Brønnøysundregistrene", "https://virksomhet.brreg.no/nb/oppslag/enheter/835391752"),
    # ("Google Maps", "https://maps.app.goo.gl/..."),
    # ("Gule Sider", "https://www.gulesider.no/..."),
]

# Skjemaet sendes til e-post via FormSubmit (gratis, ingen server).
# Første innsending gir en aktiverings-e-post til adressen. Se README.md.
FORM_EMAIL = EMAIL

# Besøksstatistikk. Lag konto på goatcounter.com og skriv inn navnet, f.eks. "olsenskogmann".
# Tom = ingen telling. Hendelsene er beskrevet øverst i src/assets/app.js.
GOATCOUNTER = "olsenskogmann"

# Besøkstall agentene kan lese (Nettsideferdig-workeren, nettsidebyra: worker/src/statistikk.ts).
# Siden laster {STATS_URL}/t.js med data-site="{STATS_SITE}". Ingen cookies og ingenting lagres på enheten,
# bare summer per døgn: visninger per side og kilde (Google, Bing, Facebook, AI-chatene, annonser),
# og klikk på telefon, SMS, e-post og skjema. Leses med
#   curl -H "Authorization: Bearer $AGENT_TOKEN" "{STATS_URL}/agent/besok?site=olsenskogmann&dager=28"
# Siden må stå med "statistikk": true i nettsidebyra/drift/apper.json. Tom STATS_URL = av.
STATS_URL = "https://sidefabrikken.nettsideferdig.workers.dev"
STATS_SITE = "olsenskogmann"

# Henvendelsesloggen (Google-ark + Apps Script). Nettapp-adressen som slutter på /exec.
# Tom = skjemaet sender bare e-post, og eiersiden /admin/ viser hvordan den settes opp.
# Se henvendelser/README.md.
LEADS_URL = ""

# Pris (bekreftet av Olsen 17.10.2026: timepris eller fastpris, introduksjonspris 600 kr eks. mva).
# Priser til forbrukere skal vises med mva (prisopplysningsforskriften): tallene på siden er med mva.
# Olsen 20.11.2026: «fjerne all pris inkl. mva og gjør om til bare pris med tall», så ordene «inkl. mva» står ikke lenger.
# Introduksjonsprisen gjelder til og med 31.12.2026 (Olsen 23.10.2026).
# Fra 1.1.2027 er vanlig timepris 795 kr eks. mva (Olsen 23.10.2026, bekreftet av Anders 24.10.2026).
# Siden bytter pris av seg selv: workflowen bygger siden rett etter midnatt 1.1.2027 (se pages.yml).
# Se siden slik den blir etter nyttår: PRICE_DATE=2027-01-01 python3 build.py
TODAY = (date.fromisoformat(os.environ["PRICE_DATE"]) if os.environ.get("PRICE_DATE")
         else datetime.now(ZoneInfo("Europe/Oslo")).date())
PRICE_INTRO_UNTIL = "2026-12-31"       # brukes i strukturerte data (validThrough)
PRICE_INTRO_UNTIL_TEXT = "31.12.2026"
PRICE_REGULAR_FROM = "2027-01-01"
PRICE_REGULAR_FROM_TEXT = "1.1.2027"
INTRO = TODAY <= date.fromisoformat(PRICE_INTRO_UNTIL)
PRICE_REGULAR_EX = 795
PRICE_REGULAR_INC = 993.75             # 795 * 1,25
PRICE_REGULAR_INC_TEXT = "993,75"
if INTRO:
    PRICE_HOUR_EX, PRICE_HOUR_INC, PRICE_HOUR_INC_TEXT = 600, 750, "750"
else:
    PRICE_HOUR_EX, PRICE_HOUR_INC, PRICE_HOUR_INC_TEXT = PRICE_REGULAR_EX, PRICE_REGULAR_INC, PRICE_REGULAR_INC_TEXT
PRICE_TEXT = f"{PRICE_HOUR_INC_TEXT} kr i timen"
# Kort: brukes i ingresser. Lang: hele setningen om timepris, brukt i FAQ, artikler og llms.txt.
PRICE_SHORT = f"{PRICE_TEXT} (introduksjonspris til {PRICE_INTRO_UNTIL_TEXT})" if INTRO else PRICE_TEXT
PRICE_HOUR_SENTENCE = (
    f"{PRICE_TEXT}, introduksjonspris til {PRICE_INTRO_UNTIL_TEXT}. "
    f"Fra {PRICE_REGULAR_FROM_TEXT} er timeprisen {PRICE_REGULAR_INC_TEXT} kr."
    if INTRO else f"{PRICE_TEXT}.")

# ---------------------------------------------------------------------------
# Tekstene på siden: sesongtilbud, fastpris på løvrydding, områder, tjenester,
# stegene, «om oss» og bydelssidene ligger i innhold.json.
# Endringer kunden ber om på e-post gjør Nettsideferdig i den fila (kode sjekker
# dem: bare tekst endres, aldri tall, adresser (slug) eller bilder), og kunden
# publiserer med lenken i e-posten. Endre teksten der, ikke her.
# {PRICE_SHORT}, {PRICE_HOUR_SENTENCE} og {PRICE_HOUR_INC_TEXT} byttes med
# timeprisen over, så den bytter av seg selv 1.1.2027.
# SEASON: sesongtilbudet øverst på forsiden. Bytt det når sesongen skifter.
# PACKAGES: fastpris på løvrydding (Olsen 23.10.2026, godkjent 24.10.2026); price null = pris etter bilde.
# ---------------------------------------------------------------------------
_VERDIER = {
    "{PRICE_SHORT}": PRICE_SHORT,
    "{PRICE_HOUR_SENTENCE}": PRICE_HOUR_SENTENCE,
    "{PRICE_HOUR_INC_TEXT}": PRICE_HOUR_INC_TEXT,
}


def _fyll(v):
    if isinstance(v, str):
        for k, x in _VERDIER.items():
            v = v.replace(k, x)
        return v
    if isinstance(v, dict):
        return {k: _fyll(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_fyll(x) for x in v]
    return v


with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "innhold.json"), encoding="utf-8") as _f:
    _INNHOLD = _fyll(json.load(_f))

PACKAGES = _INNHOLD["PACKAGES"]
NEAR_AREAS = _INNHOLD["NEAR_AREAS"]
SEASON = _INNHOLD["SEASON"]
SERVICES = _INNHOLD["SERVICES"]
STEPS = _INNHOLD["STEPS"]
ABOUT = _INNHOLD["ABOUT"]
AREAS = _INNHOLD["AREAS"]
REVIEWS = _INNHOLD["REVIEWS"]

# Sider som er tatt bort, med videresending til forsiden (build.py: page_redirect).
REMOVED_PAGES = ["borettslag"]


# ---------------------------------------------------------------------------
# Områdesider: én side per bydel nær Tveita. Tallene er boliger etter bygningstype per 1.1.2025,
# summert fra grunnkretser i Oslo kommunes statistikkbank (tabell BOL001) med SSBs
# grunnkrets→bydel-kobling (Klass 1→103). Rådata: data/smahus-per-bydel-oslo-2025.csv.
# Hver side skal ha egen tekst (ikke bare byttet navn), ellers ser Google den som tynn.
# ---------------------------------------------------------------------------
BOLIG_KILDE = ("Oslo kommune, statistikkbanken, tabell BOL001 (boliger etter bygningstype, 2025)",
               "https://statistikkbanken.oslo.kommune.no/statbank/pxweb/no/db1/db1__Boliger%20og%20byggevirksomhet__Boligmengden/OK-BOL001.px/")
OSLO_SMAHUS = {"boliger": 355915, "smahus": 84186}
