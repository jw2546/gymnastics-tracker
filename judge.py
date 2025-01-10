import streamlit as st
import pandas as pd
import sqlite3

# Function to load scores from the SQLite database
def load_scores():
    conn = sqlite3.connect('scores.db')
    df = pd.read_sql_query("SELECT * FROM scores", conn)
    conn.close()
    return df

# Function to save the updated DataFrame to the SQLite database
def save_scores(df):
    conn = sqlite3.connect('scores.db')
    df.to_sql('scores', conn, if_exists='replace', index=False)
    conn.close()

# Load the scores from the database
scores_df = load_scores()

# Streamlit app
st.title('Gymnastics Meet Score Entry')

# Dropdown to select gymnast number
gymnast_number = st.selectbox('Select Gymnast Number', scores_df['Number'])

# Display the selected gymnast's name
gymnast_name = scores_df[scores_df['Number'] == gymnast_number]['Name'].values[0]
st.write(f'Gymnast Name: {gymnast_name}')

# Dropdown to select event
event = st.selectbox('Select Event', ['Bars', 'Floor', 'Beam', 'Vault'])

# Input box for score
score = st.number_input('Enter Score (0-10.00)', min_value=0.0, max_value=10.0, step=0.1)

# Check if there's already a score
existing_score = scores_df.loc[scores_df['Number'] == gymnast_number, event].values[0]

if existing_score != '':
    st.warning(f'Existing score for {event}: {existing_score}')
    if st.button('Confirm Replace'):
        scores_df.loc[scores_df['Number'] == gymnast_number, event] = score
        save_scores(scores_df)
        st.success('Score updated successfully!')
else:
    if st.button('Submit Score'):
        scores_df.loc[scores_df['Number'] == gymnast_number, event] = score
        save_scores(scores_df)
        st.success('Score submitted successfully!')