from flask import Flask, redirect, request, url_for, render_template
import requests
import base64

app = Flask(__name__)

CLIENT_ID = '18806'
CLIENT_SECRET = 'aD4CJslCqTcgYJHpf3GQpOFbA4j5jt1FyBkTj4Zt'
REDIRECT_URI = 'http://localhost:8000/callback'
AUTH_URL = 'https://anilist.co/api/v2/oauth/authorize'
TOKEN_URL = 'https://anilist.co/api/v2/oauth/token'

@app.route('/')
def index():
    auth_url = f"{AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Error: No se recibió el código de autorización"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']
        return f"Access Token: {access_token}"
    else:
        return f"Error: {response.status_code}, {response.text}"

if __name__ == '__main__':
    app.run(debug=True, port=8000)
