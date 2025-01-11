import streamlit as st

# Main app
def main():
    st.title('Gymnastics Meet App')

    # Get the URL parameters
    query_params = st.experimental_get_query_params()
    st.write("Query Params:", query_params)  # Debugging statement

    # Ensure the page parameter is correctly extracted
    if "page" in query_params:
        page = query_params["page"][0]
    else:
        page = "judge"
    
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