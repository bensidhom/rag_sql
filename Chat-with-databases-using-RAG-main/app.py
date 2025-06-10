# app.py
import streamlit as st
from utils import get_chain
from utils import connect_to_sql
st.set_page_config(page_icon='📚', page_title="Chat with SQLite Database")

st.title("Chat with SQLite 💬")

db_path = st.text_input("Enter the full path to your SQLite file", value="mydb.sqlite")
question = st.text_area("Ask a question about your database:")

if st.button("Get Answer"):
    if db_path and question:
        with st.spinner("Processing your query..."):
            response = get_chain(question, db_path)
            st.subheader("🔎 Generated SQL")
            st.code(response["sql_query"])
            st.subheader("📊 SQL Result")
            st.write(response["result"])

if st.checkbox("Show table and column info"):
    try:
        db = connect_to_sql(db_path)
        st.write("🧾 Tables:", db.get_table_names())
        for t in db.get_table_names():
            st.write(f"📋 Columns in `{t}`:", db.run(f"PRAGMA table_info({t});"))
    except Exception as e:
        st.error(f"❌ Error reading schema: {e}")