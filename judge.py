import streamlit as st
import pandas as pd
import sqlite3
import streamlit.components.v1 as components

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
    components.html(f"""
        <script>
            console.log("{message}");
        </script>
    """, height=0)

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
        st.write("Updated DataFrame before saving:")
        st.write(scores_df)  # Debugging statement to display the updated DataFrame
        save_scores(scores_df)
        st.success('Score updated successfully!')
else:
    if st.button('Submit Score'):
        scores_df.loc[scores_df['Number'] == gymnast_number, event] = score
        st.write("Updated DataFrame before saving:")
        st.write(scores_df)  # Debugging statement to display the updated DataFrame
        save_scores(scores_df)
        st.success('Score submitted successfully!')