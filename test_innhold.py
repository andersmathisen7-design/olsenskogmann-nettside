"""Sjekker innhold.json, fila Nettsideferdig endrer når Olsen ber om en endring (se README.md).

Kjør: python3 test_innhold.py. Feiler den, bygges ikke siden (GitHub Actions kjører den før build.py).
"""
import json
import os
import re
import sys

ROT = os.path.dirname(os.path.abspath(__file__))
KJENTE = {"{PRICE_SHORT}", "{PRICE_HOUR_SENTENCE}", "{PRICE_HOUR_INC_TEXT}"}
NOKLER = {"SEASON", "PACKAGES", "NEAR_AREAS", "SERVICES", "STEPS", "ABOUT", "AREAS", "REVIEWS"}


def tekster(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from tekster(x)
    elif isinstance(v, list):
        for x in v:
            yield from tekster(x)


def main():
    with open(os.path.join(ROT, "innhold.json"), encoding="utf-8") as f:
        d = json.load(f)
    feil = []
    if set(d) != NOKLER:
        feil.append(f"nøklene skal være {sorted(NOKLER)}, er {sorted(d)}")
    for t in tekster(d):
        for p in re.findall(r"\{[A-Za-z_]+\}", t):
            if p not in KJENTE:
                feil.append(f"ukjent plassholder {p}")
        if "<" in t or ">" in t:
            feil.append(f"HTML i teksten: {t[:60]}")
    slugs = [s["slug"] for s in d.get("SERVICES", [])] + [a["slug"] for a in d.get("AREAS", [])]
    if len(slugs) != len(set(slugs)):
        feil.append("samme adresse (slug) to ganger")
    for s in slugs:
        if not re.fullmatch(r"[a-z0-9-]+", s):
            feil.append(f"ugyldig adresse: {s}")
    sys.path.insert(0, ROT)
    import config  # noqa: F401  plassholderne fylles, og fila må kunne leses av config.py
    if feil:
        print("\n".join(feil))
        sys.exit(1)
    print("innhold.json er i orden")


if __name__ == "__main__":
    main()
