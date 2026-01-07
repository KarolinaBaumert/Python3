import sqlite3
import time
import os

DB_FILE = 'tasks.db'
WORKER_ID = os.getpid()


def get_and_start_task():
    with sqlite3.connect(DB_FILE) as conn:
        conn.isolation_level = "IMMEDIATE"
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, payload FROM tasks
            WHERE status = 'pending'
            LIMIT 1
        """)
        row = cursor.fetchone()

        if not row:
            return None

        task_id, payload = row

        cursor.execute("""
            UPDATE tasks
            SET status = 'in_progress'
            WHERE id = ?
        """, (task_id,))

        conn.commit()

        return {"id": task_id, "payload": payload}


def finish_task(task_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            UPDATE tasks
            SET status = 'done'
            WHERE id = ?
        """, (task_id,))
    print(f"[CONSUMER {WORKER_ID}] Zadanie {task_id} zakończone (DONE).")


def main():
    print(f"[CONSUMER {WORKER_ID}] Uruchomiono pracownika. Oczekiwanie na pracę...")

    while True:
        task = get_and_start_task()

        if task:
            print(f"[CONSUMER {WORKER_ID}] Pobrano zadanie {task['id']}. Praca trwa 30s...")
            time.sleep(30)
            finish_task(task["id"])
        else:
            time.sleep(5)


if __name__ == "__main__":
    main()
