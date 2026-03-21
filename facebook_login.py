import webbrowser
import requests

APP_ID = "1981923649420266"
REDIRECT_URI = "https://www.facebook.com/connect/login_success.html"


def login_facebook():

    url = (
        f"https://www.facebook.com/v18.0/dialog/oauth"
        f"?client_id={APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=email,public_profile"
        f"&response_type=token"
    )

    webbrowser.open(url)


def get_user_info(access_token):

    url = f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}"

    r = requests.get(url)

    return r.json()