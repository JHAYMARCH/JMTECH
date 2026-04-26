from __future__ import annotations

import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")


class ContactPayload(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
    )


def send_email(payload: ContactPayload) -> None:
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    smtp_from = os.getenv("SMTP_FROM")
    smtp_to = os.getenv("SMTP_TO")

    if not all([smtp_host, smtp_user, smtp_pass, smtp_from, smtp_to]):
        raise RuntimeError("SMTP configuration is incomplete.")

    msg = EmailMessage()
    msg["Subject"] = f"Portfolio Contact: {payload.subject}"
    msg["From"] = smtp_from
    msg["To"] = smtp_to
    msg.set_content(
        """
New contact form submission:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
""".format(
            name=payload.name,
            email=payload.email,
            subject=payload.subject,
            message=payload.message,
        )
    )

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls(context=context)
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)


@app.get("/")
async def home():
    return FileResponse(BASE_DIR / "index.html")


@app.post("/api/contact")
async def submit_contact(payload: ContactPayload):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO contact_messages (name, email, subject, message)
            VALUES (%s, %s, %s, %s)
            """,
            (payload.name, payload.email, payload.subject, payload.message),
        )
        connection.commit()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}")
    finally:
        try:
            cursor.close()
            connection.close()
        except Exception:
            pass

    try:
        send_email(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Email error: {exc}")

    return {"ok": True}


@app.get("/health")
async def health():
    return {"status": "ok"}
