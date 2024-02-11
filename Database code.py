import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create tables for user profiles, courses, and PDFs
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS pdfs (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    course_id INTEGER,
                    FOREIGN KEY (course_id) REFERENCES courses(id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS user_selections (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    pdf_id INTEGER,
                    course_id INTEGER,
                    selection_date DATE,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (pdf_id) REFERENCES pdfs(id),
                    FOREIGN KEY (course_id) REFERENCES courses(id)
                )''')

# Commit changes and close connection
conn.commit()
conn.close()
