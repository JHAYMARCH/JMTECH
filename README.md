# BUORO OLUWATOBI JOSHUA - Portfolio

Personal portfolio website with a FastAPI backend for contact form submissions.

## Features

- Responsive portfolio UI
- Rotating role labels in hero section
- Contact form connected to backend API
- Message storage in MySQL
- Email notifications via SMTP (Gmail supported)

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: FastAPI (Python)
- Database: MySQL
- Email: SMTP

## Project Structure

- `index.html` - portfolio page
- `styles.css` - styling and animations
- `app.py` - FastAPI server and API routes
- `schema.sql` - MySQL table schema
- `requirements.txt` - Python dependencies
- `.env.example` - environment variable template

## Setup

1. Create virtual environment and install dependencies.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Create a `.env` file from `.env.example` and fill your values.

3. Create database and table.

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS portfolio;"
mysql -u root -p portfolio < schema.sql
```

4. Run the server.

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

5. Open in browser.

- `http://localhost:8000`

## Contact

- Email: `joshuaoluwatobby@gmail.com`
- LinkedIn: `https://linkedin.com/in/oluwatobi-buoro`
- GitHub: `https://github.com/JHAYMARCH`
