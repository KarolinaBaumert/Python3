import csv
import time
import os
import shutil

DB_FILE = 'tasks.csv'
LOCK_FILE = 'tasks.csv.lock'
TEMP_FILE = 'tasks.tmp.csv'
WORKER_ID = os.getpid()


def acquire_lock():
    while os.path.exists(LOCK_FILE):
        time.sleep(0.1)
    try:
        with open(LOCK_FILE, 'w') as f:
            f.write('LOCKED')
    except Exception:
        acquire_lock()


def release_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)


def get_and_start_task():
    task_to_do = None

    if not os.path.exists(DB_FILE):
        return None

    acquire_lock()
    try:
        updated_rows = []
        found = False

        with open(DB_FILE, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames

            for row in reader:
                if not found and row['status'] == 'pending':
                    row['status'] = 'in_progress'
                    task_to_do = row
                    found = True
                updated_rows.append(row)

        if found:
            with open(DB_FILE, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(updated_rows)

    finally:
        release_lock()

    return task_to_do


def finish_task(task_id):
    acquire_lock()
    try:
        rows = []
        with open(DB_FILE, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            rows = list(reader)

        with open(DB_FILE, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                if row['id'] == task_id:
                    row['status'] = 'done'
                writer.writerow(row)
        print(f"[CONSUMER {WORKER_ID}] Zadanie {task_id} zakończone (DONE).")
    finally:
        release_lock()


def main():
    print(f"[CONSUMER {WORKER_ID}] Uruchomiono pracownika. Oczekiwanie na pracę...")
    while True:
        task = get_and_start_task()

        if task:
            print(f"[CONSUMER {WORKER_ID}] Pobrano zadanie {task['id']}. Praca trwa 30s...")
            time.sleep(30)

            finish_task(task['id'])
        else:
            time.sleep(5)


if __name__ == "__main__":
    main()