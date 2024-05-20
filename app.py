from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

API_BASE_URL = "https://graphql.anilist.co"
ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImFlZjQ1Y2NmYmE1NjUzOGQ4MjMwOWVhYTJmNWM0YjY5MmIwNmJmYzhmZWFkMjI2ZGM4MGZmMTdkNmUzYzc0Mzg5ZjBjNWE0OGIzMGM5YmM3In0.eyJhdWQiOiIxODgwNiIsImp0aSI6ImFlZjQ1Y2NmYmE1NjUzOGQ4MjMwOWVhYTJmNWM0YjY5MmIwNmJmYzhmZWFkMjI2ZGM4MGZmMTdkNmUzYzc0Mzg5ZjBjNWE0OGIzMGM5YmM3IiwiaWF0IjoxNzE2MTkwNzUwLCJuYmYiOjE3MTYxOTA3NTAsImV4cCI6MTc0NzcyNjc1MCwic3ViIjoiNjI0NjM0NCIsInNjb3BlcyI6W119.CxFqUzgRqg1OEVTO_HKs8O6XUYw6FIeMqV9X262x8_5_A5zD3pTKimbRwru_lfUHwPusGyDfsVkYE1Dlv-xIXCtTFMV2A-1vKwOW1uvMIJLelsIQI0JA8dJGKPFNeq-8rkpr0YQHm2EHyImbHDTN8Pu16Mim0y6k9zWFLJfFOL1suoqghEHU2oDlLeYBfY0-I_bCSWBaP--3hlMtv59YKMZJft7-WJ727Otevbx9FerXqZ5ErjKX5twWfBmReDYLe1_4UCgAaEiHB7QD1yyAW5HHC5LymfjOUyp06GyIyvc2MRCDGztl0y7FUBtnrWwAkl-av1ZWVpyGr6OId8YFY33tBEYMFSdBVO985YOINEr-HkL70QRM2K6llGoKHtq-Ml2--RZ-mqDoLNxL76u_7obt4BsMYOlfRUmIG4og-fEcsGdCpc9npzgN704mSoi1BW0w9azg6niYeKIB9ASA2jMcuaLoXDslMCO3MNzM7mq2zXTfy_kSC8Jt3sII9E9MMbIiP1H_9C6Lmmnprm4ztMsujovRGQNLwTj_JNaDWR7p1T05dyxjmNv7faaBaHIcBbSvRFFrVLZg4yfqp-jn-lTVL0yvSG56CBUziSwxpbS1bioVcszUC8ZErSETX81j6LdODIDLjo7YEvwH2aflLkrlPo87tDTBwnFLZpjrWaE'  # Reemplaza esto con el token obtenido

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query') if request.method == 'POST' else request.args.get('query')
    search_type = request.form.get('search_type') if request.method == 'POST' else request.args.get('search_type')
    page = int(request.args.get('page', 1))
    per_page = 3

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

    if 'data' in data:
        results = data['data']['Page']
        return render_template('results.html', results=results, search_type=search_type, query=query, page=page)
    else:
        return render_template('results.html', results=None, search_type=search_type, query=query)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
