# Text-to-SQL

Ask questions about a database in plain English and get the answer back: a
Google Gemini model turns the question into a SQL query, which runs against a
SQLite database of student records. Built with Streamlit.

## Example

```
Question:  What is the average marks of students in Machine Learning?
Generated: SELECT AVG(MARKS) FROM STUDENT WHERE SUBJECT="Machine Learning";
Result:    (75.4,)
```

The result above is illustrative — the data is randomly generated, so numbers differ per setup.

## Tech stack

| Layer     | Choice                            |
|-----------|-----------------------------------|
| UI        | Streamlit                         |
| LLM       | Google Gemini (`google-generativeai`) |
| Database  | SQLite                            |

## How it works

1. **Data:** `sqlite.py` creates `students.db` with a `STUDENT` table
   (`Name`, `Subject`, `Grade`, `Marks`) and inserts 100 sample records.
2. **Prompting:** `app.py` sends the user's question to Gemini with a few-shot
   prompt that describes the table and gives example question → SQL pairs.
3. **Execution:** the generated SQL runs against SQLite, and the rows are shown
   in the app.

## Run it locally

1. Get a Gemini API key: https://aistudio.google.com/app/apikey
2. Clone the repo and install dependencies:
   ```
   git clone https://github.com/rushabhrn/Text-to-SQL.git
   cd Text-to-SQL
   pip install -r requirements.txt
   ```
3. Create a `.env` file:
   ```
   GOOGLE_API_KEY=your_gemini_key
   ```
4. Create and seed the database:
   ```
   python sqlite.py
   ```
5. Start the app and open http://localhost:8501:
   ```
   streamlit run app.py
   ```

## Known limitations

- Generated SQL is executed as-is. A production version should allow only
  read-only `SELECT` statements and open the database in read-only mode.
- The prompt relies on few-shot examples rather than reading the schema from the
  database, so it has to be updated by hand if the table changes.

## What I'd build next

- Validate generated SQL (read-only, single statement) before running it.
- Read the schema from SQLite automatically so the app works with any database.
- Show the generated SQL next to the results, and retry with the error message
  when a query fails.
