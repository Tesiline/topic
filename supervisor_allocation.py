import streamlit as st
import pandas as pd
import sys
import os

# Add the current directory to Python's search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Debugging: Check if the module can be found
print("Current working directory:", os.getcwd())
print("Python path:", sys.path)

# Try importing the assignment_model module
try:
    from assignment_model import assign_topics
except ModuleNotFoundError as e:
    st.error(f"Error: {e}")
    st.stop()

# Streamlit app title
st.title("Supervisor Assignment System")

# Sidebar inputs for CSV file paths and OpenAI API key
st.sidebar.header("Settings")
openai_api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
lecturers_path = st.sidebar.text_input("Path to Lecturers CSV", "C:/Users/Admin/Desktop/lecturers.csv")
students_path = st.sidebar.text_input("Path to Students CSV", "C:/Users/Admin/Desktop/students.csv")

if st.sidebar.button("Load and Process Data"):
    try:
        # Validate OpenAI API key
        if not openai_api_key:
            st.error("Please enter your OpenAI API key.")
        else:
            # Set OpenAI API key
            import openai
            openai.api_key = openai_api_key

            # Load data
            lecturers = pd.read_csv(lecturers_path)
            students = pd.read_csv(students_path)

            # Display the data
            st.subheader("Lecturers")
            st.write(lecturers)

            st.subheader("Students")
            st.write(students)

            # Perform topic assignment
            assignment = assign_topics(lecturers_path, students_path)

            # Display the assignment results
            st.subheader("Assignments")
            st.write(assignment)

            # Example: Summarize assignments using OpenAI
            st.subheader("Assignment Summary (via OpenAI)")
            assignment_text = assignment.to_string(index=False)
            summary = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Summarize the following assignment table:\n\n{assignment_text}",
                max_tokens=150
            )
            st.write(summary["choices"][0]["text"].strip())

            # Option to download the assignments as CSV
            csv = assignment.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Assignments as CSV",
                data=csv,
                file_name="assignments.csv",
                mime="text/csv",
            )
    except Exception as e:
        st.error(f"Error: {e}")
