from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

# File path for storing movie data
MOVIE_DATA_FILE = 'movies.json'

def load_movie_data():
    try:
        with open(MOVIE_DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_movie_data(data):
    with open(MOVIE_DATA_FILE, 'w') as file:
        json.dump(data, file)

@app.route('/')
def index():
    movies = load_movie_data()
    return render_template('index.html', movies=movies)

@app.route('/stared')
def stared():
    movies = load_movie_data()
    return render_template('stared.html', movies=movies)

@app.route('/add', methods=['POST'])
def add_movie():
    name = request.form['name']
    year = request.form['year']
    movie = {'name': name, 'year': year, 'watched': False, 'flagged': False, 'priority': '0', }
    movies = load_movie_data()
    movies.append(movie)
    save_movie_data(movies)
    return redirect('/')

@app.route('/delete/<int:index>')
def delete_movie(index):
    movies = load_movie_data()
    del movies[index]
    save_movie_data(movies)
    return redirect('/')

@app.route('/update/<int:index>/<string:status>')
def update_movie(index, status):
    movies = load_movie_data()
    movie = movies[index]
    if status == 'watched':
        movie['watched'] = True
        movie['flagged'] = False
    elif status == 'unwatched':
        movie['watched'] = False
        movie['flagged'] = False
    save_movie_data(movies)
    return redirect('/')

@app.route('/flag/<int:index>/<string:status>')
def flag_movie(index, status):
    movies = load_movie_data()
    movie = movies[index]
    if status == 'flagged':
        movie['flagged'] = True
    elif status == 'unflagged':
        movie['flagged'] = False
    save_movie_data(movies)
    return redirect('/')

@app.route('/prioritize/<int:index>')
def prioritize_movie(index):
    movies = load_movie_data()
    movie = movies[index]
    if movie.get('priority', 0) < 3:
        movie['priority'] = movie.get('priority', 0) + 1;
    else:
        movie['priority'] = 0;
    save_movie_data(movies)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)