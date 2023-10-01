import streamlit as st
import pandas as pd
import seaborn as sns


def main():
    st.title("Streamlit App Template")

    df = pd.read_csv("data")
    
    # Add your content here
    st.write("Welcome to your Streamlit app!")
    
    # Example: Adding a button
    if st.button("Click me"):
        st.write("Button clicked!")
    
    # Example: Getting user input
    user_input = st.text_input("Enter something:")
    st.write("You entered:", user_input)
    
    # Example: Displaying data
    st.write("Displaying a DataFrame:")
    data = {'col1': [1, 2, 3],
            'col2': [10, 20, 30]}
    df = pd.DataFrame(data)
    st.write(df)
    
    # Example: Plotting a chart
    st.write("Plotting a chart:")
    chart_data = {'x': [1, 2, 3, 4, 5],
                  'y': [10, 20, 15, 25, 30]}
    chart_df = pd.DataFrame(chart_data)
    st.line_chart(chart_df)

if __name__ == "__main__":
    main()