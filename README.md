# 🎮 CS:GO Code Extractor Bot

An automated bot that monitors social media platforms (Instagram, Facebook (no implemented), Discord) to automatically extract CS:GO promo codes and send them via Discord.

## 🚀 Features

- **Multi-platform monitoring** : Instagram, Facebook and Discord
- **Automatic code extraction** : Uses OCR (Tesseract) to detect promo codes
- **Automatic sending** : Sends new codes via Discord
- **Duplicate detection** : Avoids sending the same code multiple times
- **Continuous monitoring** : Runs in a loop with hourly checks
- **Multi-site support** : Monitors multiple accounts simultaneously

## 📋 Prerequisites

- Python 3.7+
- Tesseract OCR
- Instagram and Discord accounts
- Internet connection

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/cs-free-code-getter.git
cd cs-free-code-getter
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR

**Windows:**
- Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
- Install in `C:\Program Files\Tesseract-OCR\`
- Make sure the path is correct in `src/extraire_code.py`

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

### 4. Configuration

Create a `.env` file in the project root:

```env
# Instagram Credentials
INSTAGRAM_USERNAME=your_email@gmail.com
INSTAGRAM_PASSWORD=your_password

# Discord Bot Token (Selfbot)
DISCORD_TOKEN=your_discord_token
DISCORD_OUTPUT_CHANNEL_ID=output_channel_id
```

### 5. Configure monitored sites

Modify `setup.json` according to your needs:

```json
[
    {
        "site": "csgoskins",
        "username_instagram": "csgoskins_official",
        "username_facebook": "csgoskinscom",
        "discord_channel_id": "1202603456825790534"
    },
    {
        "site": "csgocases",
        "username_instagram": "csgocasescom",
        "username_facebook": "csgocasescom",
        "discord_channel_id": "1279122419994595361"
    }
]
```

## 🎯 Usage

### Launch the main bot
```bash
python main.py
```

The bot will:
1. Connect to configured platforms
2. Download latest images
3. Extract promo codes with OCR
4. Send new codes via Discord
5. Wait 1 hour before next check

### Individual scripts

**Images download only:**
```bash
python src/download_image.py
```

**Code extraction only:**
```bash
python src/extraire_code.py image_path
```

## 📁 Project Structure

```
cs-free-code-getter/
├── main.py                 # Main script
├── setup.json             # Monitored sites configuration
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (to create)
├── src/
│   ├── download_image.py # Multi-platform image download
│   ├── extraire_code.py  # Code extraction with OCR
│   └── selfbot.py        # Discord interface
├── downloaded_images/    # Downloaded images
├── last_code.json       # Sent codes history
└── session_instagram.json # Instagram session
```

## 🔧 Advanced Configuration

### Add a new site

1. Add an entry in `setup.json`:
```json
{
    "site": "new_site",
    "username_instagram": "instagram_account",
    "username_facebook": "facebook_account",
    "discord_channel_id": "discord_channel_id"
}
```

### Modify check interval

In `main.py`, modify the line:
```python
time.sleep(3600)  # 3600 seconds = 1 hour
```

### Banned codes

In `src/extraire_code.py`, modify the `banned_codes` list:
```python
banned_codes = {'FREECDE', 'XYZ789', 'OTHER_CODE'}
```

## 🔒 Security

⚠️ **Important:**
- Never share your `.env` file
- The `.env` file is automatically ignored by Git
- Use dedicated accounts for this bot
- Respect platform terms of service


## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Add new features

## ⚠️ Disclaimer

This bot is intended for educational and personal use. Make sure to respect:
- Platform terms of service
- Local laws on automation
- Copyright and intellectual property rights

---
