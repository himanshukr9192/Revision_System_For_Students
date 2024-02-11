import gradio as gr
import sqlite3

# Function to authenticate users
def authenticate(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, role FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Function to display user's profile selections
def display_profile(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT courses.name, pdfs.name, user_selections.selection_date FROM user_selections \
                    JOIN users ON users.id = user_selections.user_id \
                    JOIN courses ON courses.id = user_selections.course_id \
                    JOIN pdfs ON pdfs.id = user_selections.pdf_id \
                    WHERE users.username=?', (username,))
    selections = cursor.fetchall()
    conn.close()
    return selections

# Function to save user's selections to the database
def save_selection(username, course_id, pdf_id, selection_date):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username=?', (username,))
    user_id = cursor.fetchone()[0]
    cursor.execute('INSERT INTO user_selections (user_id, course_id, pdf_id, selection_date) \
                    VALUES (?, ?, ?, ?)', (user_id, course_id, pdf_id, selection_date))
    conn.commit()
    conn.close()

# Gradio interface for user authentication
auth_interface = gr.Interface(fn=authenticate, inputs=['text', 'text'], outputs='text', title='User Authentication', 
                               description='Enter your username and password to log in.')

# Gradio interface for displaying user's profile selections
profile_interface = gr.Interface(fn=display_profile, inputs='text', outputs='text', title='Profile Selections', 
                                 description='Enter your username to view your current profile selections.')

# Gradio interface for selecting courses and PDFs
selection_interface = gr.Interface(fn=save_selection, inputs=['text', 'text', 'text', 'text'], outputs=None, 
                                   title='Select Courses and PDFs', description='Select courses and PDFs to add to your profile.')

auth_interface.launch()
profile_interface.launch()
selection_interface.launch()
