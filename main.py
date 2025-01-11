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
    except Exception as e:
        st.write(f"An error occurred: {e}")

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

    # Ensure the page parameter is correctly extracted
    page = query_params.get("p", ["j"])[0]

    if page == "j":
        st.header('Gymnastics Meet Score Entry')

        # Load the scores from the database
        scores_df = load_scores()

        # State to keep track of selected gymnast and event
        if 'selected_gymnast' not in st.session_state:
            st.session_state.selected_gymnast = None
        if 'selected_event' not in st.session_state:
            st.session_state.selected_event = None

        # Dropdown to select gymnast number
        gymnast_number = st.selectbox('Select Gymnast Number', scores_df['Number'], key='gymnast_select')

        # Display the selected gymnast's name
        gymnast_name = scores_df[scores_df['Number'] == gymnast_number]['Name'].values[0]
        st.write(f'Gymnast Name: {gymnast_name}')

        # Dropdown to select event
        event = st.selectbox('Select Event', ['Bars', 'Floor', 'Beam', 'Vault'], key='event_select')

        # Clear score input if gymnast or event changes
        if (st.session_state.selected_gymnast != gymnast_number) or (st.session_state.selected_event != event):
            st.session_state.score_input = None

        # Update selected gymnast and event in session state
        st.session_state.selected_gymnast = gymnast_number
        st.session_state.selected_event = event

        # Input box for score
        score = st.number_input('Enter Score (0-10.00)', min_value=0.0, max_value=10.0, step=0.1, value=st.session_state.get('score_input'))

        # Check if there's already a score
        existing_score = scores_df.loc[scores_df['Number'] == gymnast_number, event].values[0]

        if existing_score != '-' and existing_score != '':
            st.warning(f'Existing score for {event}: {existing_score}')
            if st.button('Confirm Replace'):
                scores_df.loc[scores_df['Number'] == gymnast_number, event] = score
                st.write("Updated DataFrame before saving:")
                st.write(scores_df)  # Debugging statement to display the updated DataFrame
                save_scores(scores_df)
                st.success('Score updated successfully!')
                st.session_state.score_input = None  # Clear score input after confirmation
        else:
            if st.button('Confirm'):
                scores_df.loc[scores_df['Number'] == gymnast_number, event] = score
                st.write("Updated DataFrame before saving:")
                st.write(scores_df)  # Debugging statement to display the updated DataFrame
                save_scores(scores_df)
                st.success('Score submitted successfully!')
                st.session_state.score_input = None  # Clear score input after confirmation

    elif page == "v":
        st.header('Gymnastics Meet Scores')

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
                color: black.
            }
            .css-1d391kg {
                background-color: white;
                color: black.
            }
            .css-1d391kg .stDataFrame {
                border: 1px solid black.
                color: black.
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Display the scores
        st.subheader('Current Scores')
        global last_update_placeholder, scores_placeholder
        last_update_placeholder = st.empty()
        scores_placeholder = st.empty()

        # Initial load
        update_scores()

        # Automatically update the scores every 10 seconds
        while True:
            time.sleep(10)
            update_scores()

# Run the main app
if __name__ == "__main__":
    main()