# Myntra Discovery Copilot - Foundation

This is the foundational backend for the Myntra Discovery Copilot.

## Architecture
- FastAPI
- SQLite (via aiosqlite for async support)
- SQLAlchemy 2.0 (async)
- Alembic for migrations

## Setup Locally

1. **Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

2. **Database**
   - We are using SQLite for local development. The database will be created in `data/myntra_copilot.db`.
   - Copy `.env.example` to `.env`. Ensure you provide your `YOUTUBE_API_KEY`.

3. **Migrations**
   ```bash
   alembic upgrade head
   ```

4. **Run Server**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Testing**
   ```bash
   pytest
   ```

## YouTube Data Collection

You can run the modular YouTube data collector via the CLI. The collector searches for videos and fetches comments based on configured discovery queries.

**Setup**:
Ensure `YOUTUBE_API_KEY` is configured in your `.env` file. Do not commit this file.

**Features**:
- **Pagination & Quota Limits**: The collector uses configurable limits (`--max-videos`, `--max-comments`, `--max-total`) to stop gracefully before exhausting your API quota.
- **Deduplication**: We rely on the `(source_id, external_id)` database constraint. The same comment may appear across multiple queries; it is handled safely (ignored) during insertion.

**Example Command**:
```bash
python -m app.collectors.youtube --queries "Myntra clothes review" "Myntra wishlist" --max-videos 2 --max-comments 50 --max-total 100
```

**Dry Run**:
You can use `--dry-run` to fetch data from the YouTube API without writing it to the local database:
```bash
python -m app.collectors.youtube --dry-run
```

## Google Play Store Data Collection

The Play Store collector uses an unofficial public endpoint parser to pull raw reviews for the Myntra Android App.

**Example Command**:
```bash
python -m app.collectors.playstore --app-id "com.myntra.android" --max-reviews 1000
```

## Apple App Store Data Collection

The App Store collector fetches reviews for the Myntra iOS app using the internal public amp-api, surpassing the 500 review limit of traditional RSS feeds.

**Example Command**:
```bash
python -m app.collectors.appstore --app-id 907394059 --max-reviews 1000
```
