import json
import os
import socket
import sqlite3
import time

prev_class = prev_title = ""
prev_timestamp = int(time.time())

conn = sqlite3.connect("window_events.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    window_class TEXT,
                    window_title TEXT,
                    timestamp INTEGER,
                    duration INTEGER
                 )''')
conn.commit()


def handle(line):
    global prev_class, prev_title, prev_timestamp
    curr_time = int(time.time())
    event_type, data = line.split(">>", 1)
    if event_type in ("activewindow", "windowtitle"):
        win_class, win_title = data.split(",", 1)
        if event_type == "windowtitle" and win_class != prev_class:
            return
        if prev_class:
            event_data = {
                "window_class": prev_class,
                "window_title": prev_title,
                "timestamp": prev_timestamp,
                "duration": curr_time - prev_timestamp
            }
            print(json.dumps(event_data))
            cursor.execute('''INSERT INTO events (window_class, window_title, timestamp, duration)
                              VALUES (:window_class, :window_title, :timestamp, :duration)''', event_data)
            conn.commit()
        prev_class, prev_title, prev_timestamp = win_class, win_title, curr_time


sock_path = f"{os.getenv(
    'XDG_RUNTIME_DIR')}/hypr/{os.getenv('HYPRLAND_INSTANCE_SIGNATURE')}/.socket2.sock"
with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
    sock.connect(sock_path)
    with sock.makefile() as f:
        for line in f:
            handle(line.strip())
