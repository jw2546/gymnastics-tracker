import streamlit as st
import pandas as pd
import sqlite3
import time
from datetime import datetime
import pytz

# Function to load the scores from the SQLite database
def load_scores():
    conn = sqlite3.connect('scores.db')
    df = pd.read_sql_query("SELECT * FROM scores", conn)
    conn.close()
    print(df)  # Debugging statement to print the DataFrame
    return df

# Streamlit app
st.title('Gymnastics Meet Scores')

# Custom CSS for white background and black text
st.markdown(
    """
    <style>
    .main {
        background-color: white;
        color: black;
    }
    .stDataFrame {
        border: 1px solid black;
        color: black;
    }
    .css-1d391kg {
        background-color: white;
        color: black;
    }
    .css-1d391kg .stDataFrame {
        border: 1px solid black;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the scores
st.subheader('Current Scores')
last_update_placeholder = st.empty()
scores_placeholder = st.empty()

# Function to update the scores
def update_scores():
    scores_df = load_scores()
    est = pytz.timezone('US/Eastern')
    current_time = datetime.now(est).strftime("%B %d, %-I:%M%p")
    last_update_placeholder.text(f"Last update: {current_time} EST")
    scores_placeholder.dataframe(scores_df.reset_index(drop=True))  # Reset the index

# Initial load
update_scores()

# Automatically update the scores every 10 seconds
while True:
    time.sleep(10)
    update_scores()