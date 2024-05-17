from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_BASE_URL = "https://api.jikan.moe/v4"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query') if request.method == 'POST' else request.args.get('query')
    search_type = request.form.get('search_type') if request.method == 'POST' else request.args.get('search_type')
    page = int(request.args.get('page', 1))
    limit = 3
    offset = (page - 1) * limit
    url = f"{API_BASE_URL}/{search_type}?q={query}&page={offset // 25 + 1}"
    response = requests.get(url)
    data = response.json()
    if 'data' in data and len(data['data']) > 0:
        paginated_data = data['data'][offset % 25: offset % 25 + limit]
        return render_template('results.html', results=paginated_data, search_type=search_type, query=query, page=page)
    else:
        return render_template('results.html', results=None, search_type=search_type, query=query)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
