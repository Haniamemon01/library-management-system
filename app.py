import streamlit as st
import mysql.connector

# MySQL connection details
DB_HOST = "localhost"
DB_NAME = "library_db"
DB_USER = "root"
DB_PASSWORD = "admin123"

def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def insert_book(title, author, year):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = "INSERT INTO Books (title, author, year_published) VALUES (%s, %s, %s)"
        cursor.execute(sql, (title, author, year))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        st.error(f"Database Error: {err}")
        return False

# Streamlit UI
st.title("📚 Add a New Book")

title = st.text_input("Book Title")
author = st.text_input("Author")
year = st.text_input("Year Published")

if st.button("Add Book"):
    if not title or not author or not year:
        st.warning("Please fill in all fields.")
    elif not year.isdigit():
        st.warning("Year must be a number.")
    else:
        success = insert_book(title, author, int(year))
        if success:
            st.success("Book added successfully!")
