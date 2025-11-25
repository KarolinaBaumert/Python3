import sqlite3

def get_db_connection():
    conn = sqlite3.connect('movies_database.db')
    conn.row_factory = sqlite3.Row  # Umożliwia dostęp do kolumn po nazwach
    return conn

def get_movies():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies')
    movies = cursor.fetchall()
    conn.close()
    return movies

def get_links():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM links')
    links = cursor.fetchall()
    conn.close()
    return links

def get_ratings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ratings')
    ratings = cursor.fetchall()
    conn.close()
    return ratings

def get_tags():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tags')
    tags = cursor.fetchall()
    conn.close()
    return tags

movies = get_movies()
for movie in movies:
    print(f"Movie ID: {movie['movieId']}, Title: {movie['title']}, Genres: {movie['genres']}")

links = get_links()
for link in links:
    print(f"Movie ID: {link['movieId']}, IMDB ID: {link['imdbId']}, TMDB ID: {link['tmdbId']}")

ratings = get_ratings()
for rating in ratings:
    print(f"User ID: {rating['userId']}, Movie ID: {rating['movieId']}, Rating: {rating['rating']}, Timestamp: {rating['timestamp']}")

tags = get_tags()
for tag in tags:
    print(f"User ID: {tag['userId']}, Movie ID: {tag['movieId']}, Tag: {tag['tag']}, Timestamp: {tag['timestamp']}")
