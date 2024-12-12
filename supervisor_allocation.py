import streamlit as st
import pandas as pd
from assignment_model import assign_topics
import openai

# Title of the app
st.title("Supervisor Assignment System with OpenAI")

# Sidebar for inputs
st.sidebar.header("Settings")

# OpenAI API key input
openai_api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

# Input file paths for lecturers and students
lecturers_path = st.sidebar.text_input("Path to Lecturers CSV", "C:/Users/Admin/Desktop/lecturers.csv")
students_path = st.sidebar.text_input("Path to Students CSV", "C:/Users/Admin/Desktop/students.csv")

if st.sidebar.button("Load and Process Data"):
    try:
        # Validate OpenAI API key
        if not openai_api_key:
            st.error("Please enter your OpenAI API key.")
        else:
            # Set OpenAI API key
            openai.api_key = openai_api_key

            # Load data
            lecturers = pd.read_csv(lecturers_path)
            students = pd.read_csv(students_path)

            st.subheader("Lecturers")
            st.write(lecturers)

            st.subheader("Students")
            st.write(students)

            # Perform assignment
            assignment = assign_topics(lecturers_path, students_path)

            st.subheader("Assignments")
            st.write(assignment)

            # Example OpenAI API usage: summarize the assignments
            st.subheader("Assignment Summary (via OpenAI)")
            assignment_text = assignment.to_string(index=False)
            summary = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Summarize the following assignment table:\n\n{assignment_text}",
                max_tokens=150
            )
            st.write(summary["choices"][0]["text"].strip())

            # Option to download the assignments
            csv = assignment.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Assignments as CSV",
                data=csv,
                file_name="assignments.csv",
                mime="text/csv",
            )
    except Exception as e:
        st.error(f"Error: {e}")
