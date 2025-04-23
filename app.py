import streamlit as st
import mysql.connector
import os

# Function to connect to the database
def connect_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# UI
st.title("📚 Add New Book")

title = st.text_input("Book Title")
author = st.text_input("Author")
year = st.text_input("Year Published")

if st.button("➕ Add Book"):
    if not title or not author or not year:
        st.warning("Please fill in all fields.")
    else:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            sql = "INSERT INTO Books (title, author, year_published) VALUES (%s, %s, %s)"
            cursor.execute(sql, (title, author, int(year)))
            conn.commit()
            cursor.close()
            conn.close()
            st.success("✅ Book added successfully!")
        except ValueError:
            st.error("⚠️ Year must be a number.")
        except mysql.connector.Error as err:
            st.error(f"❌ Failed to add book: {err}")
