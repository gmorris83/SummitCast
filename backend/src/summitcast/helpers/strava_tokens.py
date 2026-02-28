import requests
import json
import time
from pathlib import Path

STRAVA_CLIENT_ID = "204849"
STRAVA_CLIENT_SECRET = "04d37eba70e5eeb6eed897ae62860b2b507f1d43"
REFRESH_TOKEN = 'a70e5990314338a6518cfb5d4a1ba2710e9d03ca'
TOKEN_FILE = Path(__file__).parent / "strava_tokens.json"

def refresh_strava_token():
    url = "https://www.strava.com/oauth/token"

    payload = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        raise Exception(f"Token refresh failed: {response.text}")

    token_data = response.json()

    # Store token data locally
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=4)

    return token_data


def get_valid_access_token():
    try:
        with open(TOKEN_FILE, "r") as f:
            token_data = json.load(f)
    except FileNotFoundError:
        print(f'No token data found.')
        #print(f"No token file found, creating new one...")
        # save_tokens(token_data)
        token_data = refresh_strava_token()

    expires_at = token_data.get("expires_at", 0)

    # Refresh if expired
    if time.time() > expires_at:
        token_data = refresh_strava_token()

    return token_data["access_token"], token_data["refresh_token"]

def save_tokens(token_data):
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)


def load_tokens():
    try:
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def main():
    t = load_tokens()
    print(t)
    access_token, refresh_token = get_valid_access_token()
    print(f'New Strava access token generated: {access_token}\n')
    print(f'New REFRESH_TOKEN: {refresh_token}')

# main()
