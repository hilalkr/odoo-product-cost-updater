# Odoo Product Cost Updater

Simple FastAPI app that connects to Odoo 16 Community Edition via XML-RPC to list products and update their cost prices.

## Features

- Fetch products (ID, name, SKU/internal reference, cost) with `search_read`.
- Update cost using `write` on `product.product`.
- Basic validation: blocks negative costs on both frontend and backend.
- Minimal UI via Jinja2 template + Bootstrap.

## Tech Stack

- Python 3.10+
- FastAPI + Uvicorn
- XML-RPC (stdlib `xmlrpc.client`)
- Docker Compose (Odoo + PostgreSQL)
- HTML/Bootstrap/JS (Fetch API)

## Project Structure

- `main.py` - FastAPI app, routes, template rendering.
- `services.py` - Odoo XML-RPC helpers (auth, fetch, update).
- `schemas.py` - Pydantic models for request validation.
- `config.py` - Loads environment variables from `.env`.
- `templates/` - HTML frontend.

## Setup

### 1) Clone

```bash
git clone <repository-url>
cd odoo-app
```

### 2) Start Odoo via Docker

```bash
docker-compose up -d
```

Then:

1. Wait for Odoo to initialize.
2. Open `http://localhost:8069` and create the database with:
   - Master Password: use the value shown (default is often `admin`)
   - Database Name: `odoo_test` (must match `.env`)
   - Email: `admin`
   - Password: `admin`
   - Demo Data: check this box to get sample products
3. Click **Create Database**.
4. After login, go to **Apps** and install the **Sales** module so products exist to test.

### 3) Python environment

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

### 4) Environment variables

Create `.env` in the project root:

```
ODOO_URL=http://localhost:8069
ODOO_DB=odoo_test
ODOO_USER=admin
ODOO_PASSWORD=admin
```

Adjust values to match your Odoo setup.

## Run the app

```bash
uvicorn main:app --reload
```

- UI: `http://127.0.0.1:8000`
- Docs: `http://127.0.0.1:8000/docs`

## Run tests

```bash
pytest
```

## Notes

- Cost is variant-level in Odoo, so updates target `product.product`.
- Internal Reference/SKU maps to `default_code`.
- Uses stdlib XML-RPC; no extra client dependency needed.
