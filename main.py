import json
from flask import Flask, request, redirect, g, render_template
import requests
from urllib.parse import quote

# Authentication Steps, paramaters, and responses are defined at https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.
""" 
# Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    # Get user playlist data
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)

    # Combine profile and playlist data to display
    display_arr = [profile_data] + playlist_data["items"] """


app = Flask(__name__)

#  Client Keys
CLIENT_ID = "75c5a1900edd49d19af217ca24cb6c97"
CLIENT_SECRET = "8d9eebd3551b4df68d8f1cdb3ea7b970"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}


@app.route("/")
def index():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]
    #print("News response, articles")
    #print(newsResponse['articles'])
    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    
    newsResponse = getNewsAPI()

    return render_template("index.html", news=newsResponse['articles'])


# Retrieves the top headlines from the news api
def getNewsAPI():
    apiKey = "b31dbb029fbc45c693c90dfad3065ee0"
    country = "gb"
    url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={apiKey}"
    #print("Getting news api from " + url)
    response = requests.get(
        url
    )
    newsResponse = json.loads(response.text)
    analyzeNewsArticles("I am angry")
    for articles in newsResponse['articles']:
        tone = analyzeNewsArticles(articles['title'])
        print(newsResponse[articles])
    return newsResponse

def analyzeNewsArticles(description):
    baseUrl = "https://gateway-lon.watsonplatform.net/tone-analyzer/api"
    date = "2019-10-30"
    #url = f"{baseUrl}/v3/tone?text={description}&version={date}"
    url = f"{baseUrl}/v3/tone"
    ibmKey = "u_PrmzhBiR3WJ19oHXwFS526m71E1T8dcCCXcfdmmhtB"
    #print(url)
    response = requests.get(
        url,
        auth=('apiKey', ibmKey),
        params={
            "text":description,
            "version":date
        }
    )
    toneOfArticle = json.loads(response.text)
    #print(f"response world {toneOfArticle}")
    try:
        print("description " + description + " " + toneOfArticle['document_tone']['tones'][0]['tone_name'])
        return toneOfArticle['document_tone']['tones'][0]['tone_name']
    except:
        return "Failed"

if __name__ == "__main__":
    app.run(debug=True, port=PORT)