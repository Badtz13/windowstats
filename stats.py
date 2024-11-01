import sqlite3

conn = sqlite3.connect("window_events.db")
cursor = conn.cursor()

cursor.execute('''SELECT window_class, SUM(duration) as total_duration 
                  FROM events 
                  GROUP BY window_class 
                  ORDER BY total_duration DESC''')

for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} seconds")

conn.close()
