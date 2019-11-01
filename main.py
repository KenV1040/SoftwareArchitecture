#imports
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def analyseEmotion(headline):
	print("yo")

def newsAPI():
	url = "https://newsapi.org/v2/top-headlines?country=gb"
	response = requests.get(
	url,
	headers={
		"Authorization":"b31dbb029fbc45c693c90dfad3065ee0"
	}
	)
	res = response.json()
	print("Total results: ", res['totalResults'])
	for articles in res['articles']:
		print(articles)

def spotifyAuth():
	clientID = "75c5a1900edd49d19af217ca24cb6c97"
	secret = "8d9eebd3551b4df68d8f1cdb3ea7b970" 
	client_credentials_manager = SpotifyClientCredentials(
	client_id=clientID, client_secret=secret
	)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def main():
	newsAPI()

if __name__ == "__main__":
	main()

