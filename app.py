from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

API_BASE_URL = "https://graphql.anilist.co"
ACCESS_TOKEN = 'tu_access_token'  # Reemplaza esto con el token obtenido

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query') if request.method == 'POST' else request.args.get('query')
    search_type = request.form.get('search_type') if request.method == 'POST' else request.args.get('search_type')
    filter_type = request.form.get('filter_type') if request.method == 'POST' else request.args.get('filter_type')
    page = int(request.args.get('page', 1))
    per_page = 10

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    if search_type == 'anime':
        sort = {
            'popularidad': 'POPULARITY_DESC',
            'mejores valorados': 'SCORE_DESC',
            'fecha de salida': 'START_DATE_DESC',
            'trending': 'TRENDING_DESC'
        }.get(filter_type, 'POPULARITY_DESC')

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

    if 'data' in data and 'Media' in data['data']:
        item = data['data']['Media']
        return render_template('details.html', item=item)
    else:
        return "Detalles no encontrados", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
