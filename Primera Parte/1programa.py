#Invoke-WebRequest -Uri "https://api.jikan.moe/v4/anime?q=Naruto" -Method Get

import requests

def search_anime(anime_name):
    url = f'https://api.jikan.moe/v4/anime?q={anime_name}'
    response = requests.get(url)
    data = response.json()
    if data['data']:
        return data['data'][0]
    return None

def get_anime_info(anime_name):
    anime_info = search_anime(anime_name)
    if anime_info:
        return {
            'title': anime_info['title'],
            'url': anime_info['url'],
            'synopsis': anime_info['synopsis'],
            'image_url': anime_info['images']['jpg']['image_url']
        }
    return None

if __name__ == "__main__":
    anime_name = input("Introduce el nombre del anime: ")
    anime_info = get_anime_info(anime_name)
    if anime_info:
        print(f"Title: {anime_info['title']}")
        print(f"URL: {anime_info['url']}")
        print(f"Synopsis: {anime_info['synopsis']}")
        print(f"Image URL: {anime_info['image_url']}")
    else:
        print("Anime no encontrado.")