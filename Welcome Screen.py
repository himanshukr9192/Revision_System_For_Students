import gradio as gr
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create tables if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    password TEXT,
                    is_admin INTEGER DEFAULT 0
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS pdfs (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    course_id INTEGER,
                    pdf_name TEXT,
                    upload_date TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (course_id) REFERENCES courses(id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY,
                    course_name TEXT,
                    admin_id INTEGER,
                    FOREIGN KEY (admin_id) REFERENCES users(id)
                )''')

# Function to authenticate user
def authenticate(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    return user

# Function to register a new user
def register_user(username, password, is_admin=0):
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        return "Username already exists. Please choose a different one."
    else:
        cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", (username, password, is_admin))
        conn.commit()
        return "Registration successful. You can now log in."

# Function to add a new course
def add_course(course_name, admin_id):
    cursor.execute("INSERT INTO courses (course_name, admin_id) VALUES (?, ?)", (course_name, admin_id))
    conn.commit()
    return "Course added successfully."

# Function to add a new PDF
def add_pdf(user_id, course_id, pdf_name, upload_date):
    cursor.execute("INSERT INTO pdfs (user_id, course_id, pdf_name, upload_date) VALUES (?, ?, ?, ?)", (user_id, course_id, pdf_name, upload_date))
    conn.commit()
    return "PDF added successfully."

# Function to get courses
def get_courses():
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    return courses

# Function to get PDFs for a user
def get_pdfs_for_user(user_id):
    cursor.execute("SELECT * FROM pdfs WHERE user_id = ?", (user_id,))
    pdfs = cursor.fetchall()
    return pdfs

# Function to get user's current profile selections
def get_user_selections(user_id):
    cursor.execute("SELECT course_name, pdf_name FROM courses JOIN pdfs ON courses.id = pdfs.course_id WHERE user_id = ?", (user_id,))
    selections = cursor.fetchall()
    return selections

# Define Gradio interface for selecting courses
def select_course(user_id, course_id, upload_date):
    # Assuming user selects the course from a dropdown menu
    # Here, we simply save the selected course to the database along with the provided date
    add_pdf(user_id, course_id, "", upload_date)
    return "Course selected successfully."

# Define Gradio interface for selecting PDFs
def select_pdf(user_id, pdf_name, upload_date):
    # Here, we save the selected PDF to the database along with the user's ID and the provided upload date
    # In a real application, you would need a way for users to select PDFs from a list
    add_pdf(user_id, 0, pdf_name, upload_date)
    return "PDF selected successfully."

# Define Gradio interface for displaying welcome screen
def welcome_screen(user_id):
    selections = get_user_selections(user_id)
    welcome_message = f"Welcome! Your current profile selections:\n"
    for course, pdf in selections:
        welcome_message += f"- Course: {course}, PDF: {pdf}\n"
    return welcome_message

def main():
    select_course_interface = gr.Interface(
        fn=select_course,
        inputs=["text", "text", "text"],
        outputs="text",
        title="Select Course",
        description="Enter your user ID, course ID, and upload date (YYYY-MM-DD HH:MM:SS)."
    )

    select_pdf_interface = gr.Interface(
        fn=select_pdf,
        inputs=["text", "text", "text"],
        outputs="text",
        title="Select PDF",
        description="Enter your user ID, PDF name, and upload date (YYYY-MM-DD HH:MM:SS) to select a PDF."
    )

    welcome_screen_interface = gr.Interface(
        fn=welcome_screen,
        inputs="text",
        outputs="text",
        title="Welcome Screen",
        description="Displaying your current profile selections."
    )

    select_course_interface.launch()
    select_pdf_interface.launch()
    welcome_screen_interface.launch()

if __name__ == "__main__":
    main()
