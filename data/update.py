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
def board():
    """Scoreboard in 30-day chunks (one big range can time out), merged into a single file."""
    start = dt.datetime.strptime(SEASON_START, "%Y%m%d")
    stop = dt.datetime.utcnow() + dt.timedelta(days=120)
    events, seen, d = [], set(), start
    while d <= stop:
        e = min(d + dt.timedelta(days=29), stop)
        rng = f"{d:%Y%m%d}-{e:%Y%m%d}"
        part = None
        for host in HOSTS:
            for q in (f"dates={rng}&limit=500", f"dates={rng}", f"limit=500&dates={rng.replace('-', '-')}"):
                try:
                    part = get(f"{host}/site/v2/sports/{LEAGUE}/scoreboard?{q}")
                    break
                except Exception as ex:
                    print("::warning title=scoreboard failed::", str(ex)[:300])
            if part is not None:
                break
        if part is None:
            return None
        for ev in part.get("events", []):
            if ev.get("id") not in seen:
                seen.add(ev.get("id")); events.append(ev)
        d = e + dt.timedelta(days=1)
    return {"events": events}
saved = 0
b = board()
if b and b["events"]:
    json.dump(b, open("data/scoreboard.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("saved scoreboard.json:", len(b["events"]), "events"); saved += 1
for host in HOSTS:
    try:
        data = get(host + f"/v2/sports/{LEAGUE}/standings")
        json.dump(data, open("data/standings.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
        print("saved standings.json from", host); saved += 1
        break
    except Exception as e:
        print("::warning title=standings failed::", str(e)[:300])
# never fail the workflow just because the feed is down: the page keeps its previous data
print(f"{saved}/2 files refreshed")
