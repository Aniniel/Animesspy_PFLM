from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

API_BASE_URL = "https://graphql.anilist.co"
ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImFlZjQ1Y2NmYmE1NjUzOGQ4MjMwOWVhYTJmNWM0YjY5MmIwNmJmYzhmZWFkMjI2ZGM4MGZmMTdkNmUzYzc0Mzg5ZjBjNWE0OGIzMGM5YmM3In0.eyJhdWQiOiIxODgwNiIsImp0aSI6ImFlZjQ1Y2NmYmE1NjUzOGQ4MjMwOWVhYTJmNWM0YjY5MmIwNmJmYzhmZWFkMjI2ZGM4MGZmMTdkNmUzYzc0Mzg5ZjBjNWE0OGIzMGM5YmM3IiwiaWF0IjoxNzE2MTkwNzUwLCJuYmYiOjE3MTYxOTA3NTAsImV4cCI6MTc0NzcyNjc1MCwic3ViIjoiNjI0NjM0NCIsInNjb3BlcyI6W119.CxFqUzgRqg1OEVTO_HKs8O6XUYw6FIeMqV9X262x8_5_A5zD3pTKimbRwru_lfUHwPusGyDfsVkYE1Dlv-xIXCtTFMV2A-1vKwOW1uvMIJLelsIQI0JA8dJGKPFNeq-8rkpr0YQHm2EHyImbHDTN8Pu16Mim0y6k9zWFLJfFOL1suoqghEHU2oDlLeYBfY0-I_bCSWBaP--3hlMtv59YKMZJft7-WJ727Otevbx9FerXqZ5ErjKX5twWfBmReDYLe1_4UCgAaEiHB7QD1yyAW5HHC5LymfjOUyp06GyIyvc2MRCDGztl0y7FUBtnrWwAkl-av1ZWVpyGr6OId8YFY33tBEYMFSdBVO985YOINEr-HkL70QRM2K6llGoKHtq-Ml2--RZ-mqDoLNxL76u_7obt4BsMYOlfRUmIG4og-fEcsGdCpc9npzgN704mSoi1BW0w9azg6niYeKIB9ASA2jMcuaLoXDslMCO3MNzM7mq2zXTfy_kSC8Jt3sII9E9MMbIiP1H_9C6Lmmnprm4ztMsujovRGQNLwTj_JNaDWR7p1T05dyxjmNv7faaBaHIcBbSvRFFrVLZg4yfqp-jn-lTVL0yvSG56CBUziSwxpbS1bioVcszUC8ZErSETX81j6LdODIDLjo7YEvwH2aflLkrlPo87tDTBwnFLZpjrWaE'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query') if request.method == 'POST' else request.args.get('query')
    search_type = request.form.get('search_type') if request.method == 'POST' else request.args.get('search_type')
    page = int(request.args.get('page', 1))
    per_page = 10

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    if search_type == 'anime':
        graphql_query = '''
        query ($query: String, $page: Int, $perPage: Int) {
            Page(page: $page, perPage: $perPage) {
                media(search: $query, type: ANIME) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    coverImage {
                        medium
                    }
                    description
                }
            }
        }
        '''
    elif search_type == 'characters':
        graphql_query = '''
        query ($query: String, $page: Int, $perPage: Int) {
            Page(page: $page, perPage: $perPage) {
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
    else:
        return render_template('results.html', results=None, search_type=search_type, query=query)

    variables = {
        'query': query,
        'page': page,
        'perPage': per_page
    }

    response = requests.post(API_BASE_URL, headers=headers, json={'query': graphql_query, 'variables': variables})
    data = response.json()
    print(data)  # Para depuración

    if 'data' in data:
        results = data['data']['Page']
        return render_template('results.html', results=results, search_type=search_type, query=query, page=page)
    else:
        return render_template('results.html', results=None, search_type=search_type, query=query)

@app.route('/filter', methods=['GET'])
def filter_results():
    query = request.args.get('query')
    search_type = request.args.get('search_type')
    filter_type = request.args.get('filter_type', 'POPULARITY_DESC')
    page = int(request.args.get('page', 1))
    per_page = 10

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    sort = {
        'title': 'TITLE_ROMAJI',
        'popularity': 'POPULARITY_DESC',
        'average score': 'SCORE_DESC',
        'trending': 'TRENDING_DESC',
        'favorites': 'FAVOURITES_DESC',
        'date added': 'ID_DESC',
        'release date': 'START_DATE_DESC'
    }.get(filter_type, 'POPULARITY_DESC')

    if search_type == 'anime':
        graphql_query = '''
        query ($query: String, $page: Int, $perPage: Int, $sort: [MediaSort]) {
            Page(page: $page, perPage: $perPage) {
                media(search: $query, type: ANIME, sort: $sort) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    coverImage {
                        medium
                    }
                    description
                }
            }
        }
        '''
    elif search_type == 'characters':
        graphql_query = '''
        query ($query: String, $page: Int, $perPage: Int) {
            Page(page: $page, perPage: $perPage) {
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
    else:
        return render_template('results.html', results=None, search_type=search_type, query=query)

    variables = {
        'query': query,
        'page': page,
        'perPage': per_page,
        'sort': sort if search_type == 'anime' else None
    }

    response = requests.post(API_BASE_URL, headers=headers, json={'query': graphql_query, 'variables': variables})
    data = response.json()
    print(data)  # Para depuración

    if 'data' in data:
        results = data['data']['Page']
        return render_template('results.html', results=results, search_type=search_type, query=query, page=page, filter_type=filter_type)
    else:
        return render_template('results.html', results=None, search_type=search_type, query=query)

@app.route('/details/<int:item_id>')
def details(item_id):
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    graphql_query = '''
    query ($id: Int) {
        Media(id: $id, type: ANIME) {
            id
            title {
                romaji
                english
                native
            }
            coverImage {
                large
            }
            description
            episodes
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            averageScore
            popularity
        }
    }
    '''

    variables = {
        'id': item_id
    }

    response = requests.post(API_BASE_URL, headers=headers, json={'query': graphql_query, 'variables': variables})
    data = response.json()
    print(data)  # Para depuración

    if 'data' in data and 'Media' in data['data']:
        item = data['data']['Media']
        return render_template('details.html', item=item)
    else:
        return "Detalles no encontrados", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
