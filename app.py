from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/anime', methods=['POST'])
def anime():
    anime_name = request.form['anime']
    anime_url = f'https://api.jikan.moe/v4/anime?q={anime_name}'
    anime_response = requests.get(anime_url)
    anime_data = anime_response.json()['data'][0]

    episodes_url = f'https://api.jikan.moe/v4/anime/{anime_data["mal_id"]}/episodes'
    episodes_response = requests.get(episodes_url)
    episodes_data = episodes_response.json()['data']

    return render_template('anime.html', anime=anime_data, episodes=episodes_data)

@app.route('/character', methods=['POST'])
def character():
    character_name = request.form['character']
    character_url = f'https://api.jikan.moe/v4/characters?q={character_name}'
    character_response = requests.get(character_url)
    character_data = character_response.json()['data'][0]

    return render_template('character.html', character=character_data)

if __name__ == '__main__':
    app.run(debug=True)
    