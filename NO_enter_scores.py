import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

# Define the paths to the CSV files
registration_csv_path = "registration.csv"
scores_csv_path = "scores.csv"

# Function to load data from CSV
def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame()

# Function to save data to CSV
def save_data(df, file_path):
    df.to_csv(file_path, index=False)

# Load registration data
competitors = load_data(registration_csv_path)

# Load existing scores
scores = load_data(scores_csv_path)

st.title("Enter Scores")

if not competitors.empty:
    # Select gymnast by number
    gymnast_number = st.number_input("Enter Gymnast Number", min_value=competitors['Number'].min(), max_value=competitors['Number'].max())
    selected_gymnast = competitors[competitors['Number'] == gymnast_number]

    if not selected_gymnast.empty:
        st.write(selected_gymnast)

        # Select event
        event = st.selectbox("Select Event", ["Bars", "Floor", "Beam", "Vault"])

        # Enter score
        score = st.number_input("Enter Score", min_value=0.0, max_value=10.0, step=0.1)

        if 'overwrite' not in st.session_state:
            st.session_state.overwrite = False

        if st.session_state.overwrite:
            st.warning("A score already exists for this gymnast and event. Do you want to overwrite it?")
            if st.button("Confirm Overwrite"):
                scores.loc[scores['Number'] == gymnast_number, event] = score
                save_data(scores, scores_csv_path)
                st.success("Score submitted successfully!")
                st.session_state.overwrite = False
            if st.button("Cancel"):
                st.info("Score submission cancelled.")
                st.session_state.overwrite = False
        else:
            if st.button("Submit Score"):
                existing_scores = scores.loc[scores['Number'] == gymnast_number, event]
                if not existing_scores.empty and existing_scores.values[0] != '-':
                    st.session_state.overwrite = True
                else:
                    scores.loc[scores['Number'] == gymnast_number, event] = score
                    save_data(scores, scores_csv_path)
                    st.success("Score submitted successfully!")
else:
    st.write("No registration data found. Please ensure the registration CSV is in the repository.")