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

# Load registration data
competitors = load_data(registration_csv_path)

# Load existing scores
scores = load_data(scores_csv_path)

st.title("View Results")

if not competitors.empty:
    # Initialize a DataFrame to store results
    results = competitors[['Number', 'Name']].copy()
    events = ["Bars", "Floor", "Beam", "Vault"]

    # Add columns for each event
    for event in events:
        results[event] = "-"

    # Fill in the scores for each event
    for index, row in scores.iterrows():
        gymnast_number = row['Number']
        for event in events:
            if pd.notna(row[event]):
                results.loc[results['Number'] == gymnast_number, event] = row[event]

    st.markdown(
        """
        <style>
        .results-table {
            background-color: white;
            color: black;
            border: 1px solid black;
            border-collapse: collapse;
            width: 100%;
        }
        .results-table th, .results-table td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        results.to_html(classes='results-table', index=False),
        unsafe_allow_html=True
    )
else:
    st.write("No registration data found. Please ensure the registration CSV is in the repository.")