import pytest
import sqlite3
import os
from fastapi.testclient import TestClient
from Zadanie4 import app, get_db_connection
import httpx

TEST_DB = "test_movies_database.db"



def override_get_db():
    conn = sqlite3.connect(TEST_DB)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

app.dependency_overrides[get_db_connection] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS movies (movieId INTEGER PRIMARY KEY, title TEXT NOT NULL, genres TEXT)''')
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS links (movieId INTEGER PRIMARY KEY, imdbId TEXT, tmdbId TEXT, FOREIGN KEY (movieId) REFERENCES movies(movieId))''')
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS ratings (userId INTEGER, movieId INTEGER, rating INTEGER, timestamp INTEGER, PRIMARY KEY (userId, movieId), FOREIGN KEY (movieId) REFERENCES movies(movieId))''')
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS tags (userId INTEGER, movieId INTEGER, tag TEXT, timestamp INTEGER, PRIMARY KEY (userId, movieId, tag), FOREIGN KEY (movieId) REFERENCES movies(movieId))''')


    cursor.execute("INSERT INTO movies (movieId, title, genres) VALUES (1, 'Test Movie 1', 'Comedy')")
    cursor.execute("INSERT INTO movies (movieId, title, genres) VALUES (2, 'Test Movie 2', 'Drama')")
    cursor.execute("INSERT INTO links (movieId, imdbId, tmdbId) VALUES (1, 'tt001', 'tm001')")
    cursor.execute("INSERT INTO ratings (userId, movieId, rating, timestamp) VALUES (1, 1, 5, 100000)")
    cursor.execute("INSERT INTO tags (userId, movieId, tag, timestamp) VALUES (1, 1, 'funny', 100000)")

    conn.commit()
    conn.close()

    yield

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_read_movies_list():
    response = client.get("/movies/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_read_movie_by_id():
    response = client.get("/movies/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Toy Story (1995)"


def test_read_movie_not_found():
    response = client.get("/movies/9999")
    assert response.status_code == 404


def test_create_movie():
    payload = {"movieId": 193610, "title": "New Movie", "genres": "Action"}
    response = client.post("/movies/", json=payload)
    assert response.status_code == 201

    check = client.get("/movies/193610")
    assert check.status_code == 200
    assert check.json()["title"] == "New Movie"


def test_update_movie():
    payload = {"movieId": 2, "title": "Updated Title", "genres": "Drama"}
    response = client.put("/movies/2", json=payload)
    assert response.status_code == 200

    check = client.get("/movies/2")
    assert check.json()["title"] == "Updated Title"


def test_delete_movie():
    client.post("/movies/", json={"movieId": 4, "title": "To Delete", "genres": "Horror"})

    response = client.delete("/movies/4")
    assert response.status_code == 200

    check = client.get("/movies/4")
    assert check.status_code == 404


def test_read_links_list():
    response = client.get("/links/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_create_link():
    payload = {"movieId": 2, "imdbId": "tt002", "tmdbId": "tm002"}
    response = client.post("/links/", json=payload)
    assert response.status_code == 201

    check = client.get("/links/2")
    assert check.json()["imdbId"] == "tt002"


def test_update_link():
    payload = {"movieId": 1, "imdbId": "tt_updated", "tmdbId": "tm001"}
    response = client.put("/links/1", json=payload)
    assert response.status_code == 200

    check = client.get("/links/1")
    assert check.json()["imdbId"] == "tt_updated"


def test_create_rating():
    payload = {"userId": 2, "movieId": 1, "rating": 4, "timestamp": 12345}
    response = client.post("/ratings/", json=payload)
    assert response.status_code == 201

    check = client.get("/ratings/2/1")
    assert check.status_code == 200
    assert check.json()["rating"] == 4.0


def test_update_rating():
    payload = {"userId": 1, "movieId": 1, "rating": 1, "timestamp": 99999}
    response = client.put("/ratings/1/1", json=payload)
    assert response.status_code == 200

    check = client.get("/ratings/1/1")
    assert check.json()["rating"] == 1.0


def test_delete_rating():
    response = client.delete("/ratings/2/1")
    assert response.status_code == 200

    check = client.get("/ratings/2/1")
    assert check.status_code == 404

def test_create_tag():
    payload = {"userId": 1, "movieId": 2, "tag": "boring", "timestamp": 55555}
    response = client.post("/tags/", json=payload)
    assert response.status_code == 201

    check = client.get("/tags/1/2/boring")
    assert check.status_code == 200


def test_read_tag_not_found():
    response = client.get("/tags/1/1/non_existent_tag")
    assert response.status_code == 404


def test_delete_tag():
    response = client.delete("/tags/1/1/funny")
    assert response.status_code == 200

    check = client.get("/tags/1/1/funny")
    assert check.status_code == 404