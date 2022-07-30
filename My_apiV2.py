import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
from flask import Flask, jsonify, request

app = Flask(__name__)
CORS(app)


def get_films(url):
    films = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    T_films = soup.find_all('a', class_='movie')
    for film in T_films:
        films.append({
            'name':film.text,
            'url':film.get('href'),
            'img':film.img['src'],
        })
    return films

@app.route('/film', methods=["GET","POST"])
def home():
    if request.method == "POST":
        search_url = 'https://ww.egybest.bid/explore/?q='
        keyword = request.args.get('keyword')
        search_url += keyword
        return jsonify(get_films(search_url))
    else:
        return jsonify(get_films('https://ww.egybest.bid/movies/action'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000,debug=True)
