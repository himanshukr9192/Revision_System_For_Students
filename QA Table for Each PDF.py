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

cursor.execute('''CREATE TABLE IF NOT EXISTS qas (
                    id INTEGER PRIMARY KEY,
                    pdf_id INTEGER,
                    question TEXT,
                    answer TEXT,
                    FOREIGN KEY (pdf_id) REFERENCES pdfs(id)
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

# Function to add a new QA
def add_qa(pdf_id, question, answer):
    cursor.execute("INSERT INTO qas (pdf_id, question, answer) VALUES (?, ?, ?)", (pdf_id, question, answer))
    conn.commit()
    return "QA added successfully."

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

# Function to get QAs for a PDF
def get_qas_for_pdf(pdf_id):
    cursor.execute("SELECT * FROM qas WHERE pdf_id = ?", (pdf_id,))
    qas = cursor.fetchall()
    return qas

# Define Gradio interface for adding QA
def add_qa_interface(pdf_id, question, answer):
    add_qa(pdf_id, question, answer)
    return "QA added successfully."

# Define Gradio interface for displaying QA for a PDF
def display_qa_interface(pdf_id):
    qas = get_qas_for_pdf(pdf_id)
    qa_str = ""
    for qa in qas:
        qa_str += f"Question: {qa[2]}\nAnswer: {qa[3]}\n\n"
    return qa_str

def main():
    add_qa_interface_gr = gr.Interface(
        fn=add_qa_interface,
        inputs=["text", "text", "text"],
        outputs="text",
        title="Add QA",
        description="Enter PDF ID, question, and answer to add a QA."
    )

    display_qa_interface_gr = gr.Interface(
        fn=display_qa_interface,
        inputs="text",
        outputs="text",
        title="Display QA",
        description="Enter PDF ID to display QAs for that PDF."
    )

    add_qa_interface_gr.launch()
    display_qa_interface_gr.launch()

if __name__ == "__main__":
    main()
