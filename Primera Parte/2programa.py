#Invoke-WebRequest -Uri "https://api.jikan.moe/v4/anime/20/episodes" -Method Get

import requests

def get_anime_episodes(anime_id):
    url = f'https://api.jikan.moe/v4/anime/{anime_id}/episodes'
    response = requests.get(url)
    data = response.json()
    if 'data' in data:
        return data['data']
    return []

def print_anime_episodes(anime_id):
    episodes = get_anime_episodes(anime_id)
    if episodes:
        print(f"Episodes of Anime ID {anime_id}:")
        for episode in episodes:
            print(f"Episode {episode['mal_id']}: {episode['title']} (Aired: {episode['aired']})")
    else:
        print("No episodes found.")

if __name__ == "__main__":
    anime_id = int(input("Introduce el ID del anime: "))
    print_anime_episodes(anime_id)
