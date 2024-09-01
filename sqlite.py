import sqlite3
import random

# Connect to the database (or create it)
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Create the STUDENT table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS STUDENT (
                    Name TEXT,
                    Subject TEXT,
                    Grade TEXT,
                    Marks INTEGER)''')

# List of names, subjects, and grades
names = [
    'Krish', 'Sudhanshu', 'Darius', 'Vikash', 'Dipesh', 
    'Amit', 'Priya', 'Neha', 'Raj', 'Simran', 
    'Arjun', 'Sonal', 'Kiran', 'Rahul', 'Pooja',
    'Anil', 'Kavita', 'Rohit', 'Swati', 'Gaurav',
    'Maya', 'Rakesh', 'Meera', 'Anjali', 'Sandeep',
    'Manish', 'Sunita', 'Nikhil', 'Priti', 'Ashok',
    'Sneha', 'Deepak', 'Nisha', 'Anita', 'Kunal',
    'Akash', 'Komal', 'Sagar', 'Monika', 'Prakash',
    'Harsh', 'Ritu', 'Yash', 'Ruchi', 'Alok',
    'Tanya', 'Isha', 'Sameer', 'Divya', 'Arvind'
]
subjects = ['Data Science', 'Machine Learning', 'Topics in AI', 'Natural Language Processing', 'DEVOPS']
grades = ['A', 'B', 'C']

# Insert 100 records with varied marks between 50 and 100
for i in range(100):
    name = names[i % len(names)] + str(i // len(names))  # Ensure unique names
    subject = subjects[i % len(subjects)]
    grade = grades[i % len(grades)]
    mark = random.randint(50, 100)  # Generate a random mark between 50 and 100
    
    cursor.execute(f'''INSERT INTO STUDENT (Name, Subject, Grade, Marks) 
                       VALUES ('{name}', '{subject}', '{grade}', {mark})''')

# Commit the transaction and close the connection
conn.commit()
conn.close()
