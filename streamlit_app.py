import streamlit as st
import pandas as pd
import geopandas as gpd
import time
from matplotlib import pyplot as plt


def main():

    # Set Page Format
    #st.set_page_config(layout="wide") 
    st.title("One of a Kind")

    # Read Data
    df = pd.read_csv("data/MW.csv", encoding='cp1252')
    states = gpd.read_file('shape/cb_2018_us_state_5m.shp')
    
    df_state = pd.read_csv("data/state.csv", encoding="unicode_escape")
    df['State'] = df['State'].str.lower()
    # Convert column names to lowercase to match both datasets before merging
    df.columns = df.columns.str.lower()

    # Merge the DataFrames
    merged_df = pd.merge(df, df_state[['state', 'year', 'governor']], left_on=['state', 'year'], right_on=['state', 'year'])
    selected_columns = ["year","state",	"state.minimum.wage", "governor", "effective.minimum.wage.2020.dollars"]
    merged_df = merged_df[selected_columns]

    # Sidebar for filtering/sorting
    with st.sidebar: 
        # Filter data based on selected year
        st.subheader("Filter Data")
        # Animate function
        def play_animation():
            while st.session_state["slider"] < 2016:
                st.session_state["slider"] += 1
                time.sleep(10)
            
        # Slider
        selected_year = st.slider("Select a year:", min_value=1980, max_value=2016, value=1980, step=1, key="slider")
        animate = st.button("Play",on_click=play_animation)
            


    filtered_df = merged_df[merged_df['year'] == selected_year]

    colors = filtered_df['governor'].apply(lambda x: 'blue' if x == 'D' else 'red')

    filtered_df_unmerged = df[df['year'] == selected_year]
    states['wage'] = states['NAME'].str.lower().map(filtered_df_unmerged.set_index('state')['effective.minimum.wage.2020.dollars'])


    # Map
    st.subheader("Effective Minimum Wage by State (Adjusted to 2020 inflation)")
    fig, ax = plt.subplots(figsize=(10, 8))  # Adjust the figsize as needed
    ax.set_axis_off()
    ax.set_xlim(-126, -66) 
    ax.set_ylim(24, 50)
    
    # set scale for legend
    LEGEND_MIN = 5
    LEGEND_MAX = 20

    states.plot(column="wage", ax=ax, linewidth=0.5,    edgecolor='0.8', 
                cmap='cividis', legend=True, vmin=LEGEND_MIN, vmax=LEGEND_MAX) 
    
    st.pyplot(fig)  

    # Bar plot: Minimum Wage by State
    st.subheader("Bar Plot: Minimum Wage by State")
    plt.figure(figsize=(7, 12)) 

    # Sort the DataFrame by 'state' for correct correlation
    filtered_df_state = filtered_df.sort_values(by='state')

    # set scale for bars    
    BAR_MIN = 0
    BAR_MAX = 20

    plt.barh(filtered_df_state['state'], filtered_df_state['state.minimum.wage'], color=colors)
    plt.title('Minimum Wage by State')
    plt.xlabel('Minimum Wage U$D')
    plt.ylabel('State')
    plt.xlim(BAR_MIN, BAR_MAX)
    plt.gca().invert_yaxis()

    st.pyplot(plt)

    # Display the filtered DataFrame
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)


   
if __name__ == "__main__":
    main()

