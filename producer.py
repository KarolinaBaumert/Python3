import csv
import time
import os
import uuid
import sys

DB_FILE = 'tasks.csv'
LOCK_FILE = 'tasks.csv.lock'


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


def add_task(phone_number):
    acquire_lock()
    try:
        file_exists = os.path.exists(DB_FILE)

        with open(DB_FILE, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'payload', 'status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            task_id = str(uuid.uuid4())
            writer.writerow({
                'id': task_id,
                'payload': phone_number,
                'status': 'pending'
            })
            print(f"[PRODUCER] Dodano zadanie: {task_id} dla numeru {phone_number}")
    finally:
        release_lock()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        count = int(sys.argv[1])
    else:
        print("Uruchamiam domyślne dodawanie 1 zadania.")
        count = 1

    for i in range(count):
        add_task(f"500-000-{i:03d}")