## Activity Checker Bot
This is a template for a bot that trucks user activity in Telegram groups and generates a top-list of the most active members. Built with Python (aiogram).

### Features

- Analyze user activity in groups
- Generate a top-list of the most active members
- Built using Python and Aiogram

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kartoshka-ma/activity-checker-bot.git
   cd activity-checker-bot
   ```
2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Create a `.env` file in the root directory and add lines:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   DATABASE_URL=postgresql://user:password@host:port/database_name
   ```
2. Get a bot token from [BotFather](https://t.me/BotFather) on Telegram.

### Usage

Run the bot:

```bash
python main.py
```

### License

This project is licensed under the MIT License.
