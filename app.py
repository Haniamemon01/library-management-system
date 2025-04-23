import streamlit as st
import mysql.connector

# Database credentials - use Streamlit secrets in deployment
DB_HOST = st.secrets["DB_HOST"] if "DB_HOST" in st.secrets else "localhost"
DB_USER = st.secrets["DB_USER"] if "DB_USER" in st.secrets else "root"
DB_PASSWORD = st.secrets["DB_PASSWORD"] if "DB_PASSWORD" in st.secrets else "admin123"
DB_NAME = "library_db"

def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def add_book(title, author, year):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "INSERT INTO Books (title, author, year_published) VALUES (%s, %s, %s)"
        cursor.execute(query, (title, author, year))
        conn.commit()
        st.success("✅ Book added successfully!")
    except Exception as e:
        st.error(f"❌ Failed to add book: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def view_books():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, year_published FROM Books ORDER BY id DESC")
        data = cursor.fetchall()
        if data:
            st.table(data)
        else:
            st.info("📭 No books found.")
    except Exception as e:
        st.error(f"❌ Could not fetch books: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def main():
    st.set_page_config(page_title="Library DBMS", page_icon="📚")
    st.title("📚 Library Management System")
    st.markdown("Easily add and view books in your MySQL-powered database.")

    with st.form("book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.text_input("Year Published")
        submitted = st.form_submit_button("Add Book")

        if submitted:
            if not (title and author and year):
                st.warning("⚠️ Please fill all fields.")
            elif not year.isdigit():
                st.warning("⚠️ Year must be a number.")
            else:
                add_book(title, author, int(year))

    st.markdown("---")
    st.subheader("📖 View All Books")
    view_books()

if __name__ == "__main__":
    main()
