import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("SCOPUS_API_KEY")

query = 'TITLE-ABS-KEY("malicious URL detection" AND "machine learning" AND ("browser extension" OR "web application" OR "deployment"))'

url = "https://api.elsevier.com/content/search/scopus"

all_results = []
start = 0
count = 25

while True:
    params = {
        "query": query,
        "apiKey": API_KEY,
        "start": start,
        "count": count,
        "view": "STANDARD"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(data)
        break

    results = data.get("search-results", {}).get("entry", [])
    total = int(data.get("search-results", {}).get("opensearch:totalResults", 0))

    print(f"Fetched {start + len(results)} / {total}")

    all_results.extend(results)
    start += count

    if start >= total:
        break

df = pd.json_normalize(all_results)
df.to_csv("scopus_export.csv", index=False)
print(f"\nExported {len(df)} documents")
