import re
import json
import asyncio
from datetime import datetime, timezone
from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel

# Replace with your API credentials
API_ID = '21084117'
API_HASH = '81aef5eaf2633b028ac4480db53a3f53'

# Channel username
CHANNEL_USERNAME = 'toronionlinks'
OUTPUT_FILE = 'onion_links.json'
LAST_MSG_FILE = 'last_message_id.txt'

# Regex to find .onion links
ONION_REGEX = r'(http[s]?://[a-zA-Z0-9]{16,56}\.onion)'

# Load last message ID
def load_last_msg_id():
    try:
        with open(LAST_MSG_FILE, 'r') as f:
            content = f.read().strip()
            return int(content) if content else 0
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0


# Save last message ID
def save_last_msg_id(msg_id):
    with open(LAST_MSG_FILE, 'w') as f:
        f.write(str(msg_id))

# Save results to JSON file (one object per line)
def save_results(onion_links):
    with open(OUTPUT_FILE, 'a') as f:
        for item in onion_links:
            json.dump(item, f)
            f.write('\n')

# Parse message text for .onion links
def extract_onion_links(text):
    return re.findall(ONION_REGEX, text)

# Main async function
async def main():
    last_msg_id = load_last_msg_id()

    async with TelegramClient('anon', API_ID, API_HASH) as client:
        try:
            entity = await client.get_entity(CHANNEL_USERNAME)
            messages = await client.get_messages(entity, limit=100)

            new_last_id = last_msg_id
            found_links = []

            for message in reversed(messages):  # process old to new
                if message.id <= last_msg_id:
                    continue

                if message.message:
                    links = extract_onion_links(message.message)
                    for link in links:
                        found_links.append({
                            "source": "telegram",
                            "url": link,
                            "discovered_at": datetime.now(timezone.utc).isoformat(),
                            "context": f"Found in Telegram channel @{CHANNEL_USERNAME}",
                            "status": "pending"
                        })

                new_last_id = max(new_last_id, message.id)

            if found_links:
                save_results(found_links)
                print(f"Saved {len(found_links)} .onion links to {OUTPUT_FILE}")
            else:
                print("No new .onion links found.")

            save_last_msg_id(new_last_id)

        except Exception as e:
            print(f"Error occurred: {e}")


# Run the script
if __name__ == '__main__':
    asyncio.run(main())
