from dotenv import load_dotenv
load_dotenv() ## load all the environment variables

import os
import sqlite3
import streamlit as st

import google.generativeai as genai # type: ignore

## Configure Gemini key and model

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
DB_PATH = "students.db"

## Prompt: describes the real STUDENT table created by sqlite.py

prompt = """
You are an expert in converting English questions to SQL queries for SQLite.
The database has one table named STUDENT with these columns:
NAME (text), SUBJECT (text), GRADE (text), MARKS (integer).
SUBJECT is one of: 'Data Science', 'Machine Learning', 'Topics in AI',
'Natural Language Processing', 'DEVOPS'. GRADE is one of: 'A', 'B', 'C'.

Examples:
Question: What is the average marks of students in Machine Learning?
SQL: SELECT AVG(MARKS) FROM STUDENT WHERE SUBJECT = 'Machine Learning';

Question: Show me all students who have marks greater than 80.
SQL: SELECT * FROM STUDENT WHERE MARKS > 80;

Question: How many students are enrolled in each subject?
SQL: SELECT SUBJECT, COUNT(*) FROM STUDENT GROUP BY SUBJECT;

Return only a single SELECT statement. Do not wrap it in ``` and do not
include the word SQL or any explanation.
"""

## Function to get a SQL query from Gemini

def get_gemini_response(question):
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content([prompt, question])
    return response.text.strip().strip("`").strip()

## Function to check the query is a single read-only SELECT

def is_safe_select(sql):
    statement = sql.strip().rstrip(";").strip()
    return statement.upper().startswith("SELECT") and ";" not in statement

## Function to run the query against a read-only connection

def read_sql_query(sql, db):
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        cur = conn.cursor()
        cur.execute(sql)
        columns = [col[0] for col in cur.description]
        rows = cur.fetchall()
    finally:
        conn.close()
    return columns, rows

## Streamlit App

st.set_page_config(page_title="Text-to-SQL")
st.header("Ask Your Database in Plain English")

question = st.text_input("Question: ", key="input")
submit = st.button("Ask the question")

if submit and question:
    sql = get_gemini_response(question)
    st.subheader("Generated SQL")
    st.code(sql, language="sql")

    if not is_safe_select(sql):
        st.error("Only single, read-only SELECT queries are allowed.")
    else:
        try:
            columns, rows = read_sql_query(sql, DB_PATH)
            st.subheader("Result")
            st.dataframe([dict(zip(columns, row)) for row in rows])
        except sqlite3.Error as e:
            st.error(f"The query failed: {e}")
