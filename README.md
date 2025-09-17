# NFL Eliminator 2025

Modern Flask-based NFL Eliminator game with SMS authentication and picks via text.

## Features

- 📱 **SMS Authentication** - Login with phone number verification codes
- 🏈 **Pick Teams** - Via web interface or SMS replies  
- 📲 **SMS Reminders** - Get pick reminders with available teams
- 🏆 **League Management** - Create and join multiple leagues
- 💾 **SQLite Database** - Simple, local database storage

## Tech Stack

- **Flask 3.x** with SQLAlchemy 2.x
- **uv** for modern Python package management
- **Twilio** for SMS integration
- **Bootstrap 5** for responsive UI
- **SQLite** for simple deployment

## Quick Start

1. **Setup Environment**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your settings (Twilio credentials optional for development)
   ```

2. **Install Dependencies**
   ```bash
   uv sync
   ```

3. **Initialize Database**
   ```bash
   uv run flask --app run.py db upgrade
   ```

4. **Run Development Server**
   ```bash
   uv run python run.py
   ```

5. **Open in Browser**
   ```
   http://localhost:8000
   ```

## SMS Setup (Optional for Development)

To enable SMS features, sign up for Twilio and add to `.env`:

```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token  
TWILIO_PHONE_NUMBER=+1234567890
```

## Deployment

The app is designed for easy deployment to:
- **Railway** - `railway up`
- **Fly.io** - `fly deploy`
- **Any VPS** - Simple SQLite + Flask setup

## Old Django Version

The previous Django version (2024 season) is archived in the `old/` directory.
