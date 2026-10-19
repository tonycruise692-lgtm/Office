# brain.py - The office intelligence
import requests

def get_crypto_prices():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true", timeout=10)
        data = r.json()
        out = []
        for coin in ["bitcoin", "ethereum"]:
            if coin in data:
                d = data[coin]
                out.append(f"{coin.capitalize()}: ${d['usd']:,} ({round(d['usd_24h_change'], 1)}% 24h)")
        return " | ".join(out) if out else "No data right now"
    except Exception as e:
        return f"Price feed error: {e}"

def get_news():
    try:
        r = requests.get("https://api.rss2json.com/v1/api.json?rss_url=https%3A%2F%2Fcointelegraph.com%2Frss", timeout=10)
        items = r.json().get("items", [])[:5]
        return [i["title"] for i in items] if items else ["No news loaded"]
    except Exception:
        return ["News feed error"]

def reddit_buzz(coin="pepe"):
    try:
        r = requests.get(f"https://www.reddit.com/search.json?q={coin}&sort=new&limit=5", timeout=10,
                         headers={"User-Agent": "office-agent/1.0"})
        posts = r.json().get("data", {}).get("children", [])
        return [p["data"]["title"] for p in posts] if posts else ["No posts found"]
    except Exception:
        return ["Reddit feed error"]

def market_verdict():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/global", timeout=10)
        change = r.json()["data"]["market_cap_change_percentage_24h_usd"]
        if change > 2:
            return f"Market is UP {round(change,1)}% - green across the board"
        elif change < -2:
            return f"Market is DOWN {round(change,1)}% - be careful"
        else:
            return f"Market is flat ({round(change,1)}%) - sideways day"
    except Exception:
        return "Verdict unavailable (feed error)"

def run_agent(name, task):
    if name == "news":
        return get_news()
    elif name == "market":
        return [get_crypto_prices()]
    elif name == "reddit":
        return reddit_buzz()
    elif name == "security":
        return ["Educational tool only - NOT financial advice. Verify everything yourself."]
    return ["Nothing to report"]

AGENT_TASKS = {
    "manager": "coordinate the team",
    "news": "scan the latest crypto headlines",
    "market": "check live coin prices",
    "reddit": "scan community buzz",
    "security": "keep everyone safe and honest",
}
def handle(message):
    msg = message.lower()
    details = "ok"

    if "verdict" in msg:
        reply = market_verdict()
    elif "market" in msg:
        reply = get_crypto_prices()
    elif "news" in msg:
        headlines = get_news()
        reply = " | ".join(headlines)
    elif "reddit" in msg or "buzz" in msg:
        posts = reddit_buzz()
        reply = " | ".join(posts)
    elif "security" in msg or "safe" in msg:
        reply = "Educational tool only - NOT financial advice."
    else:
        reply = "Manager: Try one of these - 'market update', 'latest news', 'reddit buzz', or 'market verdict'"
        details = "help"

    return reply, details
