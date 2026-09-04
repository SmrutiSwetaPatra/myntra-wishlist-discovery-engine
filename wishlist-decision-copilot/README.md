# Myntra Wishlist Decision Copilot - Backend

This is the standalone MVP backend for the Myntra Wishlist Decision Copilot.

## Overview
This backend provides the deterministic decision engine, product catalogue, and analytics tracking for the Copilot feature. It is built using FastAPI and SQLite.

## Setup Instructions

1. **Create Virtual Environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/Scripts/activate  # Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   ```

4. **Run the Application**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000/api`.
   Swagger documentation will be available at `http://localhost:8000/docs`.
   The application will automatically seed 10 demo products and a sample wishlist into SQLite on startup.

## Testing
Run the automated test suite with:
```bash
pytest
```
