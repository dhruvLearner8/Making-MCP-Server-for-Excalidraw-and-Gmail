from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
from email.mime.text import MIMEText
import json

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def get_gmail_service():
    """Return an authorized Gmail API service."""
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("gmail", "v1", credentials=creds)
    return service

def create_message(to: str, subject: str, body: str) -> dict:
    """Create a Gmail message dict."""
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw}
