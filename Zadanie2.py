import csv
from flask import Flask, jsonify

app = Flask(__name__)


class Movie:
    def __init__(self, movie_id, title, genres):
        self.movie_id = movie_id
        self.title = title
        self.genres = genres

    def __dict__(self):
        return {
            'movie_id': self.movie_id,
            'title': self.title,
            'genres': self.genres
        }


@app.route('/movies')
def get_movies():
    movies = []

    with open('movies.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            genres = row['genres'].split('|')
            movie = Movie(row['movieId'], row['title'], genres)
            movies.append(movie)

    return jsonify([movie.__dict__() for movie in movies])


class Link:
    def __init__(self, movie_id, imdb_id, tmdb_id):
        self.movie_id = movie_id
        self.imdb_id = imdb_id
        self.tmdb_id = tmdb_id

    def __dict__(self):
        return {
            'movie_id': self.movie_id,
            'imdb_id': self.imdb_id,
            'tmdb_id': self.tmdb_id
        }

class Rating:
    def __init__(self, user_id, movie_id, rating, timestamp):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating
        self.timestamp = timestamp

    def __dict__(self):
        return {
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'rating': self.rating,
            'timestamp': self.timestamp
        }

class Tag:
    def __init__(self, user_id, movie_id, tag, timestamp):
        self.user_id = user_id
        self.movie_id = movie_id
        self.tag = tag
        self.timestamp = timestamp

    def __dict__(self):
        return {
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'tag': self.tag,
            'timestamp': self.timestamp
        }


@app.route('/links')
def get_links():
    links = []

    with open('links.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            link = Link(row['movieId'], row['imdbId'], row['tmdbId'])
            links.append(link)

    return jsonify([link.__dict__() for link in links])


@app.route('/ratings')
def get_ratings():
    ratings = []

    with open('ratings.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            rating = Rating(row['userId'], row['movieId'], row['rating'], row['timestamp'])
            ratings.append(rating)

    return jsonify([rating.__dict__() for rating in ratings])


@app.route('/tags')
def get_tags():
    tags = []

    with open('tags.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            tag = Tag(row['userId'], row['movieId'], row['tag'], row['timestamp'])
            tags.append(tag)

    return jsonify([tag.__dict__() for tag in tags])


if __name__ == '__main__':
    app.run(debug=True)
