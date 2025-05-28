import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

from utils.analytics import get_daily_time, get_mood_trend, get_category_breakdown
from utils.visualizer import plot_category_bar

from fpdf import FPDF

# Constants
data_file = "data/tasks.csv"
os.makedirs("data", exist_ok=True)


# Load existing data or create empty DataFrame
def load_data():
    if os.path.exists(data_file) and os.path.getsize(data_file) > 0:
        return pd.read_csv(data_file)
    else:
        return pd.DataFrame(
            columns=["Date", "Task", "Time (min)", "Mood (1-5)", "Category"]
        )


# Save data to CSV
def save_data(df):
    df.to_csv(data_file, index=False)


# Export to PDF
def export_to_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Personal Productivity Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(40, 10, "Date", border=1, fill=True)
    pdf.cell(50, 10, "Task", border=1, fill=True)
    pdf.cell(30, 10, "Time (min)", border=1, fill=True)
    pdf.cell(30, 10, "Mood", border=1, fill=True)
    pdf.cell(40, 10, "Category", border=1, ln=True, fill=True)

    pdf.set_font("Arial", size=12)
    for index, row in df.iterrows():
        date_str = pd.to_datetime(row["Date"]).strftime("%Y-%m-%d")
        pdf.cell(40, 10, date_str, border=1)
        pdf.cell(50, 10, str(row["Task"]), border=1)
        pdf.cell(30, 10, str(row["Time (min)"]), border=1)
        pdf.cell(30, 10, str(row["Mood (1-5)"]), border=1)
        pdf.cell(40, 10, str(row["Category"]), border=1, ln=True)

    report_path = "data/productivity_report.pdf"
    pdf.output(report_path)
    return report_path


# App Title
st.title("📊 Personal Productivity Tracker")

# Sidebar - Add new entry
st.sidebar.header("Add New Entry")
with st.sidebar.form("entry_form"):
    task = st.text_input("Task Name")
    time_spent = st.number_input("Time Spent (minutes)", min_value=1, max_value=1440)
    mood = st.slider("Mood (1-5)", 1, 5, 3)
    category = st.text_input("Category", value="General")
    date = st.date_input("Date", value=datetime.today())
    submitted = st.form_submit_button("Add Entry")

# Load and update data
data = load_data()
if submitted:
    new_entry = pd.DataFrame(
        {
            "Date": [date.strftime("%Y-%m-%d")],
            "Task": [task],
            "Time (min)": [time_spent],
            "Mood (1-5)": [mood],
            "Category": [category],
        }
    )
    data = pd.concat([data, new_entry], ignore_index=True)
    save_data(data)
    st.success("Entry added successfully!")

# Display data
data["Date"] = pd.to_datetime(data["Date"]).dt.date
st.subheader("📅 Logged Tasks")
st.dataframe(data.sort_values("Date", ascending=False))

# PDF Export Button
if not data.empty:
    if st.button("📄 Export to PDF"):
        path = export_to_pdf(data.sort_values("Date"))
        with open(path, "rb") as file:
            st.download_button(
                label="Download PDF Report",
                data=file,
                file_name="productivity_report.pdf",
            )

# Visualizations
st.subheader("📈 Productivity Summary")
if not data.empty:
    # Time spent per day
    daily_time = get_daily_time(data)
    st.markdown("**Total Time Spent Per Day**")
    st.line_chart(daily_time)

    # Mood trend
    mood_trend = get_mood_trend(data)
    st.markdown("**Average Mood Per Day**")
    st.line_chart(mood_trend)

    # Time per category
    category_data = get_category_breakdown(data)
    st.markdown("**Time Spent by Category**")
    fig = plot_category_bar(category_data)
    st.pyplot(fig)
else:
    st.info("No data to show yet. Add your first entry from the sidebar!")
