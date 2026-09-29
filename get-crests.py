#!/usr/bin/env python3
"""Download the club crests used by the "Champions League by the numbers" section.

Source: https://football-logos.cc (logo library for informational / non-commercial design work).
Each logo is a trademark of its club. Keep the "not an official TOD page" note on the site
and use the official assets from the TOD / UEFA pack for anything real.

Usage (from the repo root, next to index.html):
    python3 get-crests.py            # download the missing crests
    python3 get-crests.py --force    # download everything again

Files are saved as assets/crests/<CODE>.png (PSG.png, BMU.png, ...).
"""
import os, re, sys, time, urllib.request, urllib.error
from urllib.parse import urljoin

BASE = os.environ.get("CRESTS_BASE", "https://football-logos.cc").rstrip("/")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "crests")
HEADERS = {"User-Agent": "Mozilla/5.0 (personal design test; downloads each logo once)"}

# code used by the site -> team page on football-logos.cc
TEAMS = {
    "PSG": "france/paris-saint-germain", "BMU": "germany/bayern-munchen", "RMA": "spain/real-madrid",
    "LFC": "england/liverpool", "INT": "italy/inter", "MCI": "england/manchester-city",
    "ARS": "england/arsenal", "BAR": "spain/barcelona", "ATM": "spain/atletico-madrid",
    "BVB": "germany/borussia-dortmund", "ROM": "italy/roma", "SPO": "portugal/sporting-cp",
    "AVL": "england/aston-villa", "FCP": "portugal/fc-porto", "MUN": "england/manchester-united",
    "BRU": "belgium/club-brugge", "RBB": "spain/real-betis", "PSV": "netherlands/psv",
    "FEY": "netherlands/feyenoord", "LIL": "france/lille", "BOG": "norway/bodo-glimt",
    "NAP": "italy/napoli", "RBL": "germany/rb-leipzig", "VIL": "spain/villarreal",
    "FEN": "turkey/fenerbahce", "SHA": "ukraine/shakhtar", "GAL": "turkey/galatasaray",
    "SLA": "czech-republic/slavia-praha", "SLO": "slovakia/s-bratislava", "VFB": "germany/vfb-stuttgart",
    "AEK": "greece/aek-athens", "ASK": "austria/lask", "COM": "italy/como-1907",
    "RCL": "france/rc-lens", "VIK": "norway/viking", "SBH": "azerbaijan/sabah",
}

def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def find_image(html, page_url):
    m = (re.search(r'<meta[^>]+property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', html)
         or re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']', html)
         or re.search(r'https://assets\.football-logos\.cc/logos/[^"\'\s>]+/700x700/[^"\'\s>]+\.png', html))
    if not m:
        return None
    return urljoin(page_url, m.group(1) if m.groups() else m.group(0))

def main():
    force = "--force" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    failed = []
    for i, (code, path) in enumerate(TEAMS.items(), 1):
        dest = os.path.join(OUT, code + ".png")
        if os.path.exists(dest) and not force:
            print(f"[{i:2}/{len(TEAMS)}] {code}: already there")
            continue
        page = f"{BASE}/{path}/"
        try:
            img = find_image(fetch(page).decode("utf-8", "ignore"), page)
            if not img:
                raise RuntimeError("no image found on the page")
            data = fetch(img)
            if not data.startswith(b"\x89PNG"):
                raise RuntimeError("downloaded file is not a PNG")
            with open(dest, "wb") as f:
                f.write(data)
            print(f"[{i:2}/{len(TEAMS)}] {code}: saved ({len(data)//1024} KB)")
        except (urllib.error.URLError, RuntimeError, OSError) as e:
            print(f"[{i:2}/{len(TEAMS)}] {code}: FAILED - {e}")
            failed.append(code)
        time.sleep(1)  # be polite to the site
    print()
    if failed:
        print("Not downloaded:", ", ".join(failed), "- add them by hand as assets/crests/<CODE>.png")
    else:
        print("Done. All crests are in assets/crests/")

if __name__ == "__main__":
    main()
