#Invoke-WebRequest -Uri "https://api.jikan.moe/v4/characters?q=Naruto%20Uzumaki" -Method Get

import requests

def search_character(character_name):
    url = f'https://api.jikan.moe/v4/characters?q={character_name}'
    response = requests.get(url)
    data = response.json()
    if data['data']:
        return data['data'][0]
    return None

def get_character_info(character_name):
    character_info = search_character(character_name)
    if character_info:
        return {
            'name': character_info['name'],
            'url': character_info['url'],
            'about': character_info['about'],
            'image_url': character_info['images']['jpg']['image_url']
        }
    return None

if __name__ == "__main__":
    character_name = input("Introduce el nombre del personaje: ")
    character_info = get_character_info(character_name)
    if character_info:
        print(f"Name: {character_info['name']}")
        print(f"URL: {character_info['url']}")
        print(f"About: {character_info['about']}")
        print(f"Image URL: {character_info['image_url']}")
    else:
        print("Personaje no encontrado.")
