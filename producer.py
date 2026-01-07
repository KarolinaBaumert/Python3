import sqlite3
import uuid
import sys

DB_FILE = 'tasks.db'


def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)


def add_task(phone_number):
    task_id = str(uuid.uuid4())

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO tasks (id, payload, status) VALUES (?, ?, ?)",
            (task_id, phone_number, "pending")
        )

    print(f"[PRODUCER] Dodano zadanie {task_id} dla numeru {phone_number}")


if __name__ == "__main__":
    init_db()

    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    for i in range(count):
        add_task(f"500-000-{i:03d}")
