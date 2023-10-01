import streamlit as st
import pandas as pd

def main():
    st.title("One of a Kind")

    df = pd.read_csv("data/MW.csv", encoding='cp1252')
    df_state = pd.read_csv("data/state.csv", encoding="unicode_escape")
    df['State'] = df['State'].str.lower()
    # Convert column names to lowercase to match both datasets before merging
    df.columns = df.columns.str.lower()

    # Merge the DataFrames
    merged_df = pd.merge(df, df_state[['state', 'year', 'governor']], left_on=['state', 'year'], right_on=['state', 'year'])

    # Filter data based on selected year
    selected_year = st.slider("Select a year:", min_value=1980, max_value=2020, value=1980, step=1)
    filtered_df = merged_df[merged_df['year'] == selected_year]

    # Display the filtered DataFrame
    st.title("Filtered Data")
    st.dataframe(filtered_df)

if __name__ == "__main__":
    main()
