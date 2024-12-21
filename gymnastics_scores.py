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
if 'competitors' not in st.session_state:
    st.session_state.competitors = load_data(registration_csv_path)

# Load existing scores
if 'scores' not in st.session_state:
    st.session_state.scores = load_data(scores_csv_path)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Enter Scores", "Display Scores", "View Results"])

if page == "Enter Scores":
    st.title("Enter Scores")

    if not st.session_state.competitors.empty:
        competitors = st.session_state.competitors

        # Select gymnast by number
        gymnast_number = st.number_input("Enter Gymnast Number", min_value=competitors['Number'].min(), max_value=competitors['Number'].max())
        selected_gymnast = competitors[competitors['Number'] == gymnast_number]

        if not selected_gymnast.empty:
            st.write(selected_gymnast)

            # Select event
            event = st.selectbox("Select Event", ["Bars", "Floor", "Beam", "Vault"])

            # Enter score
            score = st.number_input("Enter Score", min_value=0.0, max_value=10.0, step=0.1)

            if st.button("Submit Score"):
                new_score = pd.DataFrame({'Number': [gymnast_number], 'Name': [selected_gymnast['Name'].values[0]], 'Event': [event], 'Score': [score]})
                st.session_state.scores = pd.concat([st.session_state.scores, new_score], ignore_index=True)
                save_data(st.session_state.scores, scores_csv_path)

                st.success("Score submitted successfully!")
    else:
        st.write("No registration data found. Please ensure the registration CSV is in the repository.")

if page == "Display Scores":
    if 'score_queue' not in st.session_state:
        st.session_state.score_queue = []

    if not st.session_state.scores.empty:
        st.session_state.score_queue = st.session_state.scores.to_dict('records')

    if st.session_state.score_queue:
        while st.session_state.score_queue:
            current_score = st.session_state.score_queue.pop(0)
            gymnast_name = current_score['Name']
            gymnast_number = current_score['Number']
            event = current_score['Event']
            score = f"{current_score['Score']:.2f}"

            st.markdown(
                """
                <style>
                .score-display {
                    background-color: white;
                    color: black;
                    padding: 40px;
                    border-radius: 10px;
                    text-align: center;
                    width: 100%;
                    height: 80vh;
                    margin: 0;
                }
                .score-display .score {
                    font-size: 150px;
                }
                .score-display .name {
                    text-align: left;
                    float: left;
                    font-size: 30px;
                }
                .score-display .number {
                    text-align: right;
                    float: right;
                    font-size: 30px;
                }
                .score-display .event {
                    text-align: left;
                    clear: both;
                    font-size: 40px;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="score-display">
                    <div class="name"><h2>{gymnast_name}</h2></div>
                    <div class="number"><h2>{gymnast_number}</h2></div>
                    <div style="clear: both;"></div>
                    <div class="score"><h1>{score}</h1></div>
                    <div class="event"><h2>{event}</h2></div>
                </div>
                """,
                unsafe_allow_html=True
            )

            time.sleep(20)
    else:
        st.write("No scores to display.")

if page == "View Results":
    st.title("View Results")

    if not st.session_state.scores.empty:
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
            st.session_state.scores.to_html(classes='results-table', index=False),
            unsafe_allow_html=True
        )
    else:
        st.write("No scores to display.")