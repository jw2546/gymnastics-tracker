import streamlit as st
import pandas as pd
import sqlite3
import time
from datetime import datetime
import pytz

# Function to load scores from the SQLite database
def load_scores():
    conn = sqlite3.connect('scores.db')
    df = pd.read_sql_query("SELECT * FROM scores", conn)
    conn.close()
    return df

# Function to save the updated DataFrame to the SQLite database
def save_scores(df):
    try:
        conn = sqlite3.connect('scores.db')
        df.to_sql('scores', conn, if_exists='replace', index=False)
        conn.close()
        st.write("Data saved successfully.")
        log_to_console("Data saved successfully.")
    except Exception as e:
        st.write(f"An error occurred: {e}")
        log_to_console(f"An error occurred: {e}")

# Function to log messages to the browser console
def log_to_console(message):
    st.components.v1.html(f"""
        <script>
            console.log("{message}");
        </script>
    """, height=0)

# Function to update the scores
def update_scores():
    scores_df = load_scores()
    est = pytz.timezone('US/Eastern')
    current_time = datetime.now(est).strftime("%B %d, %-I:%M%p")
    last_update_placeholder.text(f"Last update: {current_time} EST")
    scores_placeholder.dataframe(scores_df.reset_index(drop=True))  # Reset the index

# Main app
def main():
    st.title('Gymnastics Meet App')

    # Get the URL parameters
    query_params = st.query_params
    st.write("Query Params:", query_params)  # Debugging statement

    # Ensure the page parameter is correctly extracted
    page = query_params.get("page", ["judge"])[0]
    st.write("Page:", page)  # Debugging statement

    if page == "judge":
        st.header('Gymnastics Meet Score Entry')
        st.write("This is the judge page.")

    elif page == "view_all_scores":
        st.header('Gymnastics Meet Scores')
        st.write("This is the view all scores page.")

# Run the main app
if __name__ == "__main__":
    main()