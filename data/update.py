"""Daily refresh of the Champions League data used by the page (run by GitHub Actions).
Saves raw ESPN scoreboard + standings JSON; the page reads them when the live feed is not reachable from the browser."""
import json, urllib.request, datetime as dt, sys
BASE = "https://site.api.espn.com/apis"
LEAGUE = "soccer/uefa.champions"
SEASON_START = "20260901"
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)
today = dt.datetime.utcnow()
end = (today + dt.timedelta(days=120)).strftime("%Y%m%d")
ok = True
for name, url in (
    ("scoreboard.json", f"{BASE}/site/v2/sports/{LEAGUE}/scoreboard?dates={SEASON_START}-{end}&limit=500"),
    ("standings.json", f"{BASE}/v2/sports/{LEAGUE}/standings"),
):
    try:
        data = get(url)
        with open(f"data/{name}", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        print("saved", name)
    except Exception as e:  # keep the previous file if the feed is down
        ok = False
        print("failed", name, e, file=sys.stderr)
sys.exit(0 if ok else 1)
