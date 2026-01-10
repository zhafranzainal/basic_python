import os
import re
import pandas as pd
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient

# Load credentials
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
password = os.getenv("API_PASSWORD")  # optional, for 2FA

channels = [
    'OrangePropertylisting',
    'rumahlelongmnproperty',
    'lelonglistishaq',
    'adlinamn'
]

price_regex = re.compile(r'RM\s?([\d,]+)')
bedroom_regex = re.compile(r'(\d+)\s*(?:bedroom|bilik tidur|bilik)')
bathroom_regex = re.compile(r'(\d+)\s*(?:bathroom|bilik mandi|bilik)')
area_regex = re.compile(r'([\d,]+)\s*(?:sq\.?ft|sqft|sqm|m2)')

data = []


async def main(client):
    for channel in channels:
        print(f"\nFetching messages from: {channel}...")
        count = 0
        async for msg in client.iter_messages(channel, limit=None):
            if msg.text:
                message_text = msg.text
                price_match = price_regex.search(message_text)
                bedroom_match = bedroom_regex.search(message_text)
                bathroom_match = bathroom_regex.search(message_text)
                area_match = area_regex.search(message_text)

                price = price_match.group(1).replace(',', '') if price_match else ''
                bedrooms = bedroom_match.group(1) if bedroom_match else ''
                bathrooms = bathroom_match.group(1) if bathroom_match else ''
                area = area_match.group(1).replace(',', '') if area_match else ''

                data.append({
                    'channel': channel,
                    'date': msg.date.replace(tzinfo=None),
                    'message': message_text,
                    'link': f"https://t.me/{channel}/{msg.id}",
                    'price_RM': price,
                    'bedrooms': bedrooms,
                    'bathrooms': bathrooms,
                    'area_sqft': area
                })

            count += 1
            if count % 500 == 0:
                print(f"{count} messages fetched from {channel}...")
                await asyncio.sleep(0.5)

        print(f"Done fetching {channel}, {len(data)} messages collected so far")

    os.makedirs('output', exist_ok=True)
    df = pd.DataFrame(data)
    df.to_excel('output/telegram_property_listings.xlsx', index=False)
    print("\nAll data saved to output/telegram_property_listings.xlsx")


# Run
async def run():
    client = TelegramClient('session', api_id, api_hash)
    await client.start(password=password)  # login handled automatically
    await main(client)
    await client.disconnect()  # cleanly disconnect


if __name__ == "__main__":
    asyncio.run(run())
