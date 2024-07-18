import streamlit as st
import sqlite3
import pandas as pd

# Connect to the SQLite database (or any other database)
conn = sqlite3.connect('bus_data.db')
cursor = conn.cursor()

# Fetch data from the database
query = "SELECT * FROM bus_data"
data = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Display the data in Streamlit
st.title("Database Bus Details ")
st.write("Here is the data from the database:")
st.dataframe(data)

# Optionally, you can display the data in other formats
st.table(data)
