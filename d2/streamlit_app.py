import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt 

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

    colors = filtered_df['governor'].apply(lambda x: 'blue' if x == 'D' else 'red')

    # Bar plot: Minimum Wage by State
    st.title("Bar Plot: Minimum Wage by State")
    plt.figure(figsize=(7, 12)) 

    # Sort the DataFrame by 'state' for correct correlation
    filtered_df = filtered_df.sort_values(by='state')

    plt.barh(filtered_df['state'], filtered_df['state.minimum.wage'], color=colors)
    plt.title('Minimum Wage by State')
    plt.xlabel('Minimum Wage U$D')
    plt.ylabel('State')
    plt.gca().invert_yaxis()

    st.pyplot(plt)

    # Map
    st.title("Effective Minimum Wage by State")
    fig = px.choropleth(
        df,
        locations='state',
        locationmode="USA-states",
        scope="usa",
        color='effective.minimum.wage',
        color_continuous_scale="Viridis_r",
    )
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
