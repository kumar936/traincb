import sqlite3

# Connect or create
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create table
c.execute('''
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    destination TEXT,
    time_slot TEXT,
    crowd TEXT,
    stand_time INTEGER,
    sit_from TEXT
)
''')

conn.commit()
conn.close()
print("✅ Database and table created.")
