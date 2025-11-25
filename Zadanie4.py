import sqlite3
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import Optional


app = FastAPI()
DB_NAME = 'movies_database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

class Movie(BaseModel):
    movieId: int
    title: str
    genres: Optional[str] = None

class Link(BaseModel):
    movieId: int
    imdbId: Optional[str] = None
    tmdbId: Optional[str] = None

class Rating(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int

class Tag(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int


@app.post("/movies/", status_code=201)
def create_movie(movie: Movie):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO movies (movieId, title, genres) VALUES (?, ?, ?)",
            (movie.movieId, movie.title, movie.genres)
        )
        conn.commit()
        return movie
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Movie ID already exists")
    finally:
        conn.close()

@app.get("/movies/{movie_id}")
def read_movie(movie_id: int):
    conn = get_db_connection()
    movie = conn.execute("SELECT * FROM movies WHERE movieId = ?", (movie_id,)).fetchone()
    conn.close()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie: Movie):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE movies SET title = ?, genres = ? WHERE movieId = ?",
        (movie.title, movie.genres, movie_id)
    )
    conn.commit()
    rows = cursor.rowcount
    conn.close()
    if rows == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie updated successfully"}

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE movieId = ?", (movie_id,))
    conn.commit()
    rows = cursor.rowcount
    conn.close()
    if rows == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}


@app.post("/links/", status_code=201)
def create_link(link: Link):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO links (movieId, imdbId, tmdbId) VALUES (?, ?, ?)",
            (link.movieId, link.imdbId, link.tmdbId)
        )
        conn.commit()
        return link
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Link for this Movie ID already exists or Movie ID missing")
    finally:
        conn.close()

@app.get("/links/{movie_id}")
def read_link(movie_id: int):
    conn = get_db_connection()
    link = conn.execute("SELECT * FROM links WHERE movieId = ?", (movie_id,)).fetchone()
    conn.close()
    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return link

@app.put("/links/{movie_id}")
def update_link(movie_id: int, link: Link):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE links SET imdbId = ?, tmdbId = ? WHERE movieId = ?",
        (link.imdbId, link.tmdbId, movie_id)
    )
    conn.commit()
    rows = cursor.rowcount
    conn.close()
    if rows == 0:
        raise HTTPException(status_code=404, detail="Link not found")
    return {"message": "Link updated successfully"}

@app.delete("/links/{movie_id}")
def delete_link(movie_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM links WHERE movieId = ?", (movie_id,))
    conn.commit()
    rows = cursor.rowcount
    conn.close()
    if rows == 0:
        raise HTTPException(status_code=404, detail="Link not found")
    return {"message": "Link deleted successfully"}

@app.post("/ratings/", status_code=201)
def create_rating(rating: Rating):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO ratings (userId, movieId, rating, timestamp) VALUES (?, ?, ?, ?)",
            (rating.userId, rating.movieId, rating.rating, rating.timestamp)
        )
        conn.commit()
        return rating
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Rating already exists")
    finally:
        conn.close()

@app.get("/ratings/{user_id}/{movie_id}")
def read_rating(user_id: int, movie_id: int):
    conn = get_db_connection()
    rating = conn.execute(
        "SELECT * FROM ratings WHERE userId = ? AND movieId = ?",
        (user_id, movie_id)
    ).fetchone()
    conn.close()
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating

@app.put("/ratings/{user_id}/{movie_id}")
def update_rating(user_id: int, movie_id: int, rating: Rating):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE ratings SET rating = ?, timestamp = ? WHERE userId = ? AND movieId = ?",
        (rating.rating, rating.timestamp, user_id, movie_id)
    )
    conn.commit()
    rows = cursor.rowcount
    conn.close()
    if rows == 0:
        raise HTTPException(status_code=404, detail="Rating not found")
    return {"message": "Rating updated successfully"}

@app.delete("/ratings/{user_id}/{movie_id}")
def delete_rating(user_id: int, movie_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ratings WHERE userId = ? AND movieId = ?", (user_id, movie_id))
    conn.commit()
    rows = cursor.rowcount
    conn.close()
    if rows == 0:
        raise HTTPException(status_code=404, detail="Rating not found")
    return {"message": "Rating deleted successfully"}

@app.post("/tags/", status_code=201)
def create_tag(tag: Tag):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO tags (userId, movieId, tag, timestamp) VALUES (?, ?, ?, ?)",
            (tag.userId, tag.movieId, tag.tag, tag.timestamp)
        )
        conn.commit()
        return tag
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Tag already exists")
    finally:
        conn.close()

@app.get("/tags/{user_id}/{movie_id}/{tag_text}")
def read_tag(user_id: int, movie_id: int, tag_text: str):
    conn = get_db_connection()
    tag = conn.execute(
        "SELECT * FROM tags WHERE userId = ? AND movieId = ? AND tag = ?",
        (user_id, movie_id, tag_text)
    ).fetchone()
    conn.close()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@app.put("/tags/{user_id}/{movie_id}/{tag_text}")
def update_tag(user_id: int, movie_id: int, tag_text: str, tag_data: Tag):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tags SET timestamp = ? WHERE userId = ? AND movieId = ? AND tag = ?",
        (tag_data.timestamp, user_id, movie_id, tag_text)
    )
    conn.commit()
    rows = cursor.rowcount
    conn.close()
    if rows == 0:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag updated successfully"}

@app.delete("/tags/{user_id}/{movie_id}/{tag_text}")
def delete_tag(user_id: int, movie_id: int, tag_text: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM tags WHERE userId = ? AND movieId = ? AND tag = ?",
        (user_id, movie_id, tag_text)
    )
    conn.commit()
    rows = cursor.rowcount
    conn.close()
    if rows == 0:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag deleted successfully"}

@app.get("/movies/")
def read_movies(limit: int = 10, offset: int = 0):
    conn = get_db_connection()
    movies = conn.execute("SELECT * FROM movies LIMIT ? OFFSET ?", (limit, offset)).fetchall()
    conn.close()
    return movies

@app.get("/links/")
def read_links(limit: int = 10, offset: int = 0):
    conn = get_db_connection()
    links = conn.execute("SELECT * FROM links LIMIT ? OFFSET ?", (limit, offset)).fetchall()
    conn.close()
    return links

@app.get("/ratings/")
def read_ratings(limit: int = 10, offset: int = 0):
    conn = get_db_connection()
    ratings = conn.execute("SELECT * FROM ratings LIMIT ? OFFSET ?", (limit, offset)).fetchall()
    conn.close()
    return ratings

@app.get("/tags/")
def read_tags(limit: int = 10, offset: int = 0):
    conn = get_db_connection()
    tags = conn.execute("SELECT * FROM tags LIMIT ? OFFSET ?", (limit, offset)).fetchall()
    conn.close()
    return tags