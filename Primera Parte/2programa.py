import requests

ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImFlZjQ1Y2NmYmE1NjUzOGQ4MjMwOWVhYTJmNWM0YjY5MmIwNmJmYzhmZWFkMjI2ZGM4MGZmMTdkNmUzYzc0Mzg5ZjBjNWE0OGIzMGM5YmM3In0.eyJhdWQiOiIxODgwNiIsImp0aSI6ImFlZjQ1Y2NmYmE1NjUzOGQ4MjMwOWVhYTJmNWM0YjY5MmIwNmJmYzhmZWFkMjI2ZGM4MGZmMTdkNmUzYzc0Mzg5ZjBjNWE0OGIzMGM5YmM3IiwiaWF0IjoxNzE2MTkwNzUwLCJuYmYiOjE3MTYxOTA3NTAsImV4cCI6MTc0NzcyNjc1MCwic3ViIjoiNjI0NjM0NCIsInNjb3BlcyI6W119.CxFqUzgRqg1OEVTO_HKs8O6XUYw6FIeMqV9X262x8_5_A5zD3pTKimbRwru_lfUHwPusGyDfsVkYE1Dlv-xIXCtTFMV2A-1vKwOW1uvMIJLelsIQI0JA8dJGKPFNeq-8rkpr0YQHm2EHyImbHDTN8Pu16Mim0y6k9zWFLJfFOL1suoqghEHU2oDlLeYBfY0-I_bCSWBaP--3hlMtv59YKMZJft7-WJ727Otevbx9FerXqZ5ErjKX5twWfBmReDYLe1_4UCgAaEiHB7QD1yyAW5HHC5LymfjOUyp06GyIyvc2MRCDGztl0y7FUBtnrWwAkl-av1ZWVpyGr6OId8YFY33tBEYMFSdBVO985YOINEr-HkL70QRM2K6llGoKHtq-Ml2--RZ-mqDoLNxL76u_7obt4BsMYOlfRUmIG4og-fEcsGdCpc9npzgN704mSoi1BW0w9azg6niYeKIB9ASA2jMcuaLoXDslMCO3MNzM7mq2zXTfy_kSC8Jt3sII9E9MMbIiP1H_9C6Lmmnprm4ztMsujovRGQNLwTj_JNaDWR7p1T05dyxjmNv7faaBaHIcBbSvRFFrVLZg4yfqp-jn-lTVL0yvSG56CBUziSwxpbS1bioVcszUC8ZErSETX81j6LdODIDLjo7YEvwH2aflLkrlPo87tDTBwnFLZpjrWaE'  # Reemplaza esto con el token obtenido

def search_character(query):
    url = "https://graphql.anilist.co"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    graphql_query = '''
    query ($query: String) {
        Page(page: 1, perPage: 1) {
            characters(search: $query) {
                id
                name {
                    full
                }
                image {
                    medium
                }
                description
            }
        }
    }
    '''
    variables = {
        'query': query
    }

    response = requests.post(url, headers=headers, json={'query': graphql_query, 'variables': variables})
    print("Response status code:", response.status_code)
    print("Response content:", response.content.decode('utf-8'))
    return response.json()

if __name__ == '__main__':
    character_name = input("Introduce el nombre del personaje: ")
    result = search_character(character_name)
    if result and 'data' in result and result['data']['Page']['characters']:
        character = result['data']['Page']['characters'][0]
        print(f"Nombre: {character['name']['full']}")
        print(f"Descripción: {character['description']}")
        print(f"Imagen: {character['image']['medium']}")
    else:
        print("Personaje no encontrado.")
