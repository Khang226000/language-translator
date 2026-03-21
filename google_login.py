import requests
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email']

def login_google():

    flow = InstalledAppFlow.from_client_secrets_file(
    "language-translator/client_secret.json",
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid"]
)

    creds = flow.run_local_server(port=0)
    

    return creds
def get_user_info(creds):

    headers = {
        "Authorization": f"Bearer {creds.token}"
    }

    r = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers=headers
    )

    return r.json()