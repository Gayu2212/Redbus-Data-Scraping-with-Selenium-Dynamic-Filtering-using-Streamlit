import streamlit as st
import sqlite3
import pandas as pd

# Function to fetch data from the SQLite database
def fetch_data():
    conn = sqlite3.connect('bus_data.db')
    query = "SELECT * FROM bus_data"
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

# Fetch the data
data = fetch_data()

ROWS_PER_PAGE = 20

# Streamlit app
st.set_page_config(page_title="Available Bus", page_icon="🚌", layout="wide")

custom_css = """
<style>
    .table-container {
        margin-top: 20px;
        width: 100%;
        overflow-x: auto;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
    }
    th, td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
    th {
        background-color: #4CAF50;
        color: white;
    }

    .header {
        text-align: center;
        margin-bottom: 20px;
    }
    .header img {
        vertical-align: middle;
    }
    .pagination {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    .pagination button {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
    }
    .pagination button:hover {
        background-color: white;
        color: black;
        border: 2px solid #4CAF50;
    }
</style>
"""

# Header
st.markdown("<div class='header'><h1>Available Buses 🚌</h1></div>", unsafe_allow_html=True)

# Inject custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("Please Filter Here:")

route = st.sidebar.multiselect(
    "Select The Route",
    options=data["bus_route_name"].unique()
)

bus_name = st.sidebar.multiselect(
    "Select the Bus Name",
    options=data["bus_name"].unique()
)

bus_type = st.sidebar.multiselect(
    "Select The Bus Type",
    options=data["bus_type"].unique()
)

# Apply filters
filtered_data = data.copy()

if route:
    filtered_data = filtered_data[filtered_data["bus_route_name"].isin(route)]
if bus_name:
    filtered_data = filtered_data[filtered_data["bus_name"].isin(bus_name)]
if bus_type:
    filtered_data = filtered_data[filtered_data["bus_type"].isin(bus_type)]

# Pagination
total_rows = len(filtered_data)
total_pages = -(-total_rows // ROWS_PER_PAGE)  # Ceiling division

# Initialize session state for pagination
if 'page' not in st.session_state:
    st.session_state.page = 0

# Handle pagination buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("Previous"):
        if st.session_state.page > 0:
            st.session_state.page -= 1
with col3:
    if st.button("Next"):
        if st.session_state.page < total_pages - 1:
            st.session_state.page += 1

# Calculate the range of rows to display
start_row = st.session_state.page * ROWS_PER_PAGE
end_row = min(start_row + ROWS_PER_PAGE, total_rows)

# Display the filtered data in a styled table
st.markdown(
    f"""
    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Bus Route Name</th>
                    <th>Bus Name</th>
                    <th>Bus Link</th>
                    <th>Bus Type</th>
                    <th>Departure Time</th>
                    <th>Duration</th>
                    <th>Arrival Time</th>
                    <th>Rating</th>
                    <th>Fare</th>
                    <th>Seats Available</th>
                </tr>
            </thead>
            <tbody>
                {''.join(
        f"<tr>"
        f"<td>{row['bus_route_name']}</td>"
        f"<td>{row['bus_name']}</td>"
        f"<td><a href='{row['bus_link']}'>Book Now</a></td>"
        f"<td>{row['bus_type']}</td>"
        f"<td>{row['departure_time']}</td>"
        f"<td>{row['duration']}</td>"
        f"<td>{row['arrival_time']}</td>"
        f"<td>{row['rating']}</td>"
        f"<td>{row['fare']}</td>"
        f"<td>{row['seats_available']}</td>"
        f"</tr>"
        for _, row in filtered_data.iloc[start_row:end_row].iterrows()
    )}
            </tbody>
        </table>
    </div>
    """,
    unsafe_allow_html=True
)

# Display current page number
st.write(f"Page {st.session_state.page + 1} of {total_pages}")
