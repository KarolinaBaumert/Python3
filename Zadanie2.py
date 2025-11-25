import sqlite3
import csv

conn = sqlite3.connect('movies_database.db')
cursor = conn.cursor()

def load_data_from_csv(csv_file, table_name, columns):
    with open(csv_file, newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            cursor.execute(f'''
                INSERT OR REPLACE INTO {table_name} ({", ".join(columns)})
                VALUES ({", ".join("?" * len(columns))})
            ''', row)
        conn.commit()


load_data_from_csv('movies.csv', 'movies', ['movieId', 'title', 'genres'])

load_data_from_csv('links.csv', 'links', ['movieId', 'imdbId', 'tmdbId'])

load_data_from_csv('ratings.csv', 'ratings', ['userId', 'movieId', 'rating', 'timestamp'])

load_data_from_csv('tags.csv', 'tags', ['userId', 'movieId', 'tag', 'timestamp'])

conn.close()

print("Dane zostały załadowane do bazy danych.")
