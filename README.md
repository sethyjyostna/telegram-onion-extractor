# telegram-onion-extractor
# 🧅 Telegram .onion Link Extractor

This Python script connects to a public Telegram channel using the **Telethon** library and extracts any `.onion` links from recent messages. The extracted links are saved in a structured JSON file. This tool is useful for OSINT researchers, cybersecurity analysts, and ethical hacking learners.

## 📦 Features

- Connects securely to Telegram using your credentials
- Extracts `.onion` URLs using regex
- Saves results in JSON format (1 object per line)
- Tracks last processed message (to avoid duplicate results)
- Uses asynchronous Python (`async/await`)
- Handles Telegram API/network errors gracefully

## ⚙️ Requirements

- Python 3.8 or later
- A Telegram account
- API credentials from Telegram
## 🚀 Setup Instructions

### 1. Clone or Download the Project

```bash
git clone https://github.com/your-username/telegram-onion-extractor.git
cd telegram-onion-extractor
