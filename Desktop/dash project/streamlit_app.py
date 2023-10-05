import streamlit as st
import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt

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

    st.write(df.columns)

    xaxis = df["state"].values
    
    yaxis=df["effective.minimum.wage"].values
    import seaborn as sns
    test = pd.DataFrame(
    {
        "x": xaxis,
        "y": yaxis
        
    }
)
    plt.figure(figsize=(7, 12)) 
    sns.barplot(data=test.sort_values('y', ascending=False), y='x', x='y')
    plt.title('minimum wage every state')
    plt.xlabel('minimum wage')
    plt.ylabel('state')
    plt.show()


    fig = px.choropleth(
                        df,
                        locations='state', 
                        locationmode="USA-states", 
                        scope="usa",
                        color='effective.minimum.wage',
                    color_continuous_scale="Viridis_r", 
                        
                        )
    fig.show()

if __name__ == "__main__":
    main()

