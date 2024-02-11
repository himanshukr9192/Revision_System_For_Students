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
                    FOREIGN KEY (user_id) REFERENCES users(id)
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

# Define Gradio interface for login
def login(username, password):
    user = authenticate(username, password)
    if user:
        if user[3] == 1:
            return f"Welcome, {username}! You are now logged in as administrator."
        else:
            return f"Welcome, {username}! You are now logged in."
    else:
        return "Invalid username or password. Please try again."

# Define Gradio interface for registration
def register(username, password, is_admin):
    message = register_user(username, password, is_admin)
    return message

# Define Gradio interface for adding a new course
def add_new_course(course_name, admin_id):
    message = add_course(course_name, admin_id)
    return message

# Define Gradio interface for adding a new PDF
def add_new_pdf(user_id, course_id, pdf_name, upload_date):
    message = add_pdf(user_id, course_id, pdf_name, upload_date)
    return message

def main():
    login_interface = gr.Interface(
        fn=login,
        inputs=["text", "text"],
        outputs="text",
        title="Login",
        description="Enter your username and password to log in."
    )

    register_interface = gr.Interface(
        fn=register,
        inputs=["text", "text", "checkbox"],
        outputs="text",
        title="Register",
        description="Enter a username, password, and check the box if you are registering as an administrator."
    )

    add_course_interface = gr.Interface(
        fn=add_new_course,
        inputs=["text", "text"],
        outputs="text",
        title="Add New Course",
        description="Enter the course name and your admin ID to add a new course."
    )

    add_pdf_interface = gr.Interface(
        fn=add_new_pdf,
        inputs=["text", "text", "text", "text"],
        outputs="text",
        title="Add New PDF",
        description="Enter your user ID, course ID, PDF name, and upload date to add a new PDF."
    )

    login_interface.launch()
    register_interface.launch()
    add_course_interface.launch()
    add_pdf_interface.launch()

if __name__ == "__main__":
    main()
