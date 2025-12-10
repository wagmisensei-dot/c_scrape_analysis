import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def save_snapshot_to_supabase(data):
    url = f"{SUPABASE_URL}/rest/v1/cron_snapshots"
    headers = {
        "apikey": SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
        "Content-Type": "application/json"
    }
    r = requests.post(url, headers=headers, data=json.dumps(data))
    print("Supabase response:", r.text)

def scrape_chrono24():
    url = "https://www.chrono24.com/rolex/index.htm"
    print("Scraping:", url)

    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    listings = soup.select(".article-item-container")
    results = []

    for item in listings[:10]:  # just first 10 to keep it small
        title = item.select_one(".article-title").text.strip() if item.select_one(".article-title") else None
        price = item.select_one(".article-price").text.strip() if item.select_one(".article-price") else None

        results.append({
            "title": title,
            "price": price
        })

    return results

if __name__ == "__main__":
    data = scrape_chrono24()

    print("Scraped:", data)

    # Save simple snapshot
    save_snapshot_to_supabase({
        "run_time": datetime.utcnow().isoformat(),
        "data": data
    })
