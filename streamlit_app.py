import streamlit as st
import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt

def main():
    st.title("One of a Kind")

    df = pd.read_csv("data/MW.csv", encoding='cp1252')
    states = gpd.read_file('shape/cb_2018_us_state_5m.shp')
    
    df_state = pd.read_csv("data/state.csv", encoding="unicode_escape")
    df['State'] = df['State'].str.lower()
    # Convert column names to lowercase to match both datasets before merging
    df.columns = df.columns.str.lower()

    # Merge the DataFrames
    merged_df = pd.merge(df, df_state[['state', 'year', 'governor']], left_on=['state', 'year'], right_on=['state', 'year'])

    # Filter data based on selected year
    selected_year = st.slider("Select a year:", min_value=1980, max_value=2020, value=1980, step=1)
    filtered_df = merged_df[merged_df['year'] == selected_year]

    filtered_df_unmerged = df[df['year'] == selected_year]
    states['wage'] = states['NAME'].str.lower().map(filtered_df_unmerged.set_index('state')['effective.minimum.wage.2020.dollars'])

    fig, ax = plt.subplots(figsize=(10, 8))  # Adjust the figsize as needed
    ax.set_axis_off()
    ax.set_xlim(-126, -66) 
    ax.set_ylim(24, 50)
    
    
    LEGEND_MIN = 5
    LEGEND_MAX = 17.5

    states.plot(column="wage", ax=ax, linewidth=0.5,    edgecolor='0.8', 
                cmap='Greens', legend=True, vmin=LEGEND_MIN, vmax=LEGEND_MAX) 
    
    st.pyplot(fig)  

    st.subheader(f'Data for the year {selected_year}')
    st.write(filtered_df)



   
if __name__ == "__main__":
    main()

