import sqlite3

conn = sqlite3.connect('movies_database.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        movieId INTEGER PRIMARY KEY, 
        title TEXT NOT NULL,
        genres TEXT  -- Zakładając, że genres będzie przechowywać tekst, np. "Akcja, Dramat"
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS links (
        movieId INTEGER PRIMARY KEY, 
        imdbId TEXT,
        tmdbId TEXT,
        FOREIGN KEY (movieId) REFERENCES movies(movieId)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ratings (
        userId INTEGER, 
        movieId INTEGER,
        rating INTEGER,  -- Zakładając, że oceny są liczbami całkowitymi (np. od 1 do 10)
        timestamp INTEGER,  -- Zakładając, że timestamp będzie przechowywał czas w formie liczby całkowitej (np. Unix timestamp)
        PRIMARY KEY (userId, movieId),
        FOREIGN KEY (movieId) REFERENCES movies(movieId)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tags (
        userId INTEGER, 
        movieId INTEGER,
        tag TEXT,
        timestamp INTEGER,  -- Zakładając, że timestamp będzie przechowywał czas w formie liczby całkowitej (np. Unix timestamp)
        PRIMARY KEY (userId, movieId, tag),
        FOREIGN KEY (movieId) REFERENCES movies(movieId)
    );
''')

conn.commit()

conn.close()

print("Baza danych została utworzona.")
