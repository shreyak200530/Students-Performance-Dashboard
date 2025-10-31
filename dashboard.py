import pandas as pd
import streamlit as st
from PIL import Image

# Use raw string for Windows-style path
image = Image.open(r"C:\Users\Shreya\OneDrive\Desktop\studentdashboard\streamlit.jpg")

st.title("Student Performance Dashboard")
st.image(image, caption="Dashboard Banner", width=40, use_container_width=True)
st.header("Dataset")

data = pd.read_csv('students_data.csv')  # Ensure CSV path is correct
df = data.copy()

# Sidebar Filters
st.sidebar.header("Filters")

course_options = ["All"] + sorted(df['Course'].unique().tolist())
selected_course = st.sidebar.selectbox("Select Course", course_options)
if selected_course != "All":
    df = df[df["Course"] == selected_course]

city_options = sorted(df['City'].unique().tolist())
selected_cities = st.sidebar.multiselect("Select City", city_options, default=city_options)
df = df[df['City'].isin(selected_cities)]

min_marks = st.sidebar.slider("Filter by minimum marks", min_value=int(df['Marks'].min()),
                              max_value=int(df['Marks'].max()), value=int(df['Marks'].min()))
df = df[df['Marks'] >= min_marks]

gender = st.sidebar.radio("Choose Gender", ["All", "Male", "Female"])
if gender != "All":
    df = df[df['Gender'] == gender]

st.header("Filtered Data")
st.dataframe(df)

# Summary Statistics
st.header("Summary Statistics")
avg_marks = df['Marks'].mean() if not df.empty else 0
avg_attendance = df['Attendance (%)'].mean() if not df.empty else 0
total_students = len(df)

col1, col2, col3 = st.columns(3)
col1.metric("Average Marks", f"{avg_marks:.2f}")
col2.metric("Average Attendance (%)", f"{avg_attendance:.2f}")
col3.metric("Total Students", total_students)

# Student Search
st.header("Student Search")
search_name = st.text_input("Enter student name to search:")
if search_name:
    result = df[df["Name"].str.contains(search_name, case=False)]
    st.dataframe(result)

col4, col5 = st.columns(2)
if col4.button("Show Top Performers"):
    st.dataframe(df[df['Marks'] > 90])

if col5.button("Show All Data"):
    st.dataframe(data)  # Show all data

st.header("Charts")
if not df.empty:
    st.bar_chart(df.set_index("Student_ID")["Marks"])
else:
    st.warning("No data to display for the given filter combination.")

# Messages based on average marks
if avg_marks > 85:
    st.success("Excellent performance!")
elif avg_marks >= 70:
    st.info("Good performance.")
else:
    st.warning("Needs improvement.")
