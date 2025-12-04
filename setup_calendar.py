#!/usr/bin/env python3
"""
Run this locally (not in Docker) to authenticate Google Calendar.
The token will be saved to data/google_token.pickle for Docker to use.
"""

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_FILE = 'data/google_credentials.json'
TOKEN_FILE = 'data/google_token.pickle'

def main():
    creds = None

    # Check for existing token
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # If no valid creds, do the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"ERROR: Missing {CREDENTIALS_FILE}")
                print("\nTo get this file:")
                print("1. Go to https://console.cloud.google.com")
                print("2. Create/select a project")
                print("3. Enable 'Google Calendar API'")
                print("4. Go to Credentials → Create Credentials → OAuth client ID")
                print("5. Choose 'Desktop app'")
                print("6. Download JSON and save as data/google_credentials.json")
                return

            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)

        # Save the token
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

        print(f"\nSuccess! Token saved to {TOKEN_FILE}")
        print("Restart the Docker container to use it:")
        print("  docker-compose restart dan-brain")

if __name__ == '__main__':
    main()
