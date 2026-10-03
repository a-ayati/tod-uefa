"""Daily refresh of the Champions League data used by the page (run by GitHub Actions).
Saves raw ESPN scoreboard + standings JSON; the page reads them when the live feed is not reachable from the browser."""
import json, urllib.request, urllib.error, datetime as dt, sys, time
HOSTS = ["https://site.api.espn.com/apis", "https://site.web.api.espn.com/apis"]
LEAGUE = "soccer/uefa.champions"
SEASON_START = "20260901"
HEAD = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
        "Accept": "application/json", "Referer": "https://www.espn.com/"}
def get(url):
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEAD), timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code} {e.reason}"
            if e.code in (403, 404): break
        except Exception as e:
            last = repr(e)
        time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"{last} <- {url}")
end = (dt.datetime.utcnow() + dt.timedelta(days=120)).strftime("%Y%m%d")
jobs = {
    "scoreboard.json": f"/site/v2/sports/{LEAGUE}/scoreboard?dates={SEASON_START}-{end}&limit=500",
    "standings.json": f"/v2/sports/{LEAGUE}/standings",
}
saved = 0
for name, path in jobs.items():
    for host in HOSTS:
        try:
            data = get(host + path)
            with open(f"data/{name}", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
            print("saved", name, "from", host)
            saved += 1
            break
        except Exception as e:
            print("FAILED", name, e, file=sys.stderr)
# never fail the workflow just because the feed is down: the page keeps its previous data
print(f"{saved}/{len(jobs)} files refreshed")
