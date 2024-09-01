from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import random
import streamlit as st
import os
import sqlite3

import google.generativeai as genai # type: ignore
## Configure Genai Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question, prompts):
    model = genai.GenerativeModel('gemini-pro')
    selected_prompt = random.choice(prompts)
    response = model.generate_content([selected_prompt, question])
    # Ensure that the table name is correct in the SQL query
    corrected_response = response.text.replace("RESULT", "STUDENT")
    
    return corrected_response

## Fucntion To retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Define Your Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION, MARKS.
    
    For example:
    Example 1 - What is the average marks of students in the Machine Learning class? 
    The SQL command will be something like this: SELECT AVG(MARKS) FROM STUDENT WHERE CLASS="Machine Learning";
    
    Example 2 - Show me all students who have marks greater than 80. 
    The SQL command will be something like this: SELECT * FROM STUDENT WHERE MARKS > 80;

    Also, the SQL code should not have ``` in the beginning or end and the word SQL should not appear in the output.
    """,

    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION, GRADE.
    
    For example:
    Example 1 - List the names of all students who have an 'A' grade. 
    The SQL command will be something like this: SELECT NAME FROM STUDENT WHERE GRADE="A";
    
    Example 2 - How many students are in the DEVOPS class? 
    The SQL command will be something like this: SELECT COUNT(*) FROM STUDENT WHERE CLASS="DEVOPS";

    Also, the SQL code should not have ``` in the beginning or end and the word SQL should not appear in the output.
    """,

    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, SUBJECT, GRADE, MARKS.
    
    For example:
    Example 1 - Retrieve the name and marks of students who scored above 90 in Data Science. 
    The SQL command will be something like this: SELECT NAME, MARKS FROM STUDENT WHERE CLASS="Data Science" AND MARKS > 90;
    
    Example 2 - Show the details of all students sorted by their marks in descending order. 
    The SQL command will be something like this: SELECT * FROM STUDENT ORDER BY MARKS DESC;

    Also, the SQL code should not have ``` in the beginning or end and the word SQL should not appear in the output.
    """,

    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, SUBJECT, GRADE, MARKS.
    
    For example:
    Example 1 - Find out how many students are enrolled in each subject. 
    The SQL command will be something like this: SELECT SUBJECT, COUNT(*) FROM STUDENT GROUP BY SUBJECT;
    
    Example 2 - List the names of students who have 'B' grade in Natural Language Processing. 
    The SQL command will be something like this: SELECT NAME FROM STUDENT WHERE SUBJECT="Natural Language Processing" AND GRADE="B";

    Also, the SQL code should not have ``` in the beginning or end and the word SQL should not appear in the output.
    """,

    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION, MARKS.
    
    For example:
    Example 1 - What are the names of students in section 'A'? 
    The SQL command will be something like this: SELECT NAME FROM STUDENT WHERE SECTION="A";
    
    Example 2 - Retrieve all records where the marks are between 70 and 90. 
    The SQL command will be something like this: SELECT * FROM STUDENT WHERE MARKS BETWEEN 70 AND 90;

    Also, the SQL code should not have ``` in the beginning or end and the word SQL should not appear in the output.
    """
]

## Streamlit App

st.set_page_config(page_title="Retrieve SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"students.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)