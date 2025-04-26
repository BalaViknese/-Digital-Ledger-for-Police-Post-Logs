import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import altair as alt
import time


st.sidebar.title("Navigation")
choice = st.sidebar.radio("Choose a section:", ["Home", "View Data", "Statistics", "Visualization", "SQL Queries"])

def load_data():
    conn = mysql.connector.connect(
        host="localhost", user="root", password="", database="police_check_post"
    )
    df = pd.read_sql("SELECT * FROM stops", conn)
    conn.close()
    return df

df = load_data()

df['stop_date'] = pd.to_datetime(df['stop_date'], errors='coerce')
df['driver_age'] = pd.to_numeric(df['driver_age'], errors='coerce')
df['stop_duration'] = pd.to_numeric(df['stop_duration'], errors='coerce')

queries = {
    "Total Stops": """SELECT COUNT(*) AS total_stops FROM stops;""",
    "Stops by Violation": """SELECT violation, COUNT(*) AS count FROM stops GROUP BY violation;""",
    "Stops by Outcome": """SELECT stop_outcome, COUNT(*) AS count FROM stops GROUP BY stop_outcome;""",
    "Average Driver Age": """SELECT AVG(driver_age) AS average_age FROM stops;""",
    "Top 5 Search Types": """SELECT search_type, COUNT(*) AS count FROM stops WHERE search_type IS NOT NULL AND search_type != '' GROUP BY search_type ORDER BY count DESC LIMIT 5;""",
    "Stops by Gender": """SELECT driver_gender, COUNT(*) AS count FROM stops GROUP BY driver_gender;""",
    "Top Violation with Arrests": """SELECT violation, 
       COUNT(*) AS total_stops,
       SUM(CASE WHEN is_arrested = 'True' THEN 1 ELSE 0 END) AS total_arrests
       FROM stops
       WHERE is_arrested IN ('True', 'False')  -- Ensuring only valid string values are considered
       GROUP BY violation
       ORDER BY total_arrests DESC
       LIMIT 3;""",
    "Average Stop Duration by Violation": """SELECT violation, AVG(stop_duration) AS avg_duration FROM stops GROUP BY violation;""",
    "Drug-Related Stops by Year": """SELECT YEAR(stop_date) AS year, COUNT(*) AS count
    FROM stops
    WHERE (drugs_related_stop = 'True')
    GROUP BY year
    ORDER BY count DESC
    LIMIT 9;""",
    "Top 5 Gender-Age Arrests": """SELECT driver_gender, driver_age, COUNT(*) AS count FROM stops GROUP BY driver_gender, driver_age ORDER BY count DESC LIMIT 5;""",
    "Stops Between 10PM and 5AM": """SELECT COUNT(*) AS count
    FROM stops
    WHERE HOUR(STR_TO_DATE(stop_time, '%H:%i:%s')) BETWEEN 22 AND 23
    OR HOUR(STR_TO_DATE(stop_time, '%H:%i:%s')) BETWEEN 0 AND 5;""",
    "Stops with Search Conducted": """SELECT violation, COUNT(*) AS count
    FROM stops
    WHERE CASE
        WHEN search_conducted = 'True' THEN 1
        WHEN search_conducted = 'False' THEN 0
        ELSE NULL
      END = 1
    GROUP BY violation;""",
    "Arrest Rate by Gender": """SELECT driver_gender,
       COUNT(*) AS total_stops,
       SUM(CASE WHEN is_arrested = 'True' THEN 1 ELSE 0 END) AS total_arrests,
       ROUND(SUM(CASE WHEN is_arrested = 'True' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS arrest_rate_percentage 
       FROM stops 
       GROUP BY driver_gender;""",
    "Violation Trends by Month": """SELECT MONTH(stop_date) AS month, violation, COUNT(*) AS count
                                    FROM stops
                                    GROUP BY month, violation
                                    ORDER BY month, violation;""",
    "Drugs Related Stop Outcome": """SELECT stop_outcome, COUNT(*) AS count
    FROM stops
    WHERE drugs_related_stop = 'True'
    GROUP BY stop_outcome
    ORDER BY count DESC;""",
    "Country Arrest Stats": """SELECT YEAR(stop_date) AS year, country_name, COUNT(*) AS total_stops,SUM(CASE WHEN is_arrested IN ('True') THEN 1 ELSE 0 END) AS total_arrests 
                               FROM stops 
                               GROUP BY year, country_name 
                               ORDER BY year, country_name;""",
    "Age, Race, and Violation Breakdown": """SELECT driver_age, driver_race, violation, COUNT(*) AS count
                                             FROM stops
                                             GROUP BY driver_age, driver_race, violation
                                             ORDER BY count DESC;""",
    "Stops by Hour of Day": """SELECT HOUR(STR_TO_DATE(stop_time, '%H:%i:%s')) AS hour_of_day, COUNT(*) AS count
                               FROM stops
                               GROUP BY hour_of_day;""",
    "Stop Duration by Age and Violation": """SELECT driver_age, violation, AVG(stop_duration) AS avg_duration FROM stops WHERE driver_age IS NOT NULL AND driver_age != '' GROUP BY driver_age, violation;""",
    "High Violation, Search, and Arrest Stats": """SELECT violation,
       COUNT(*) AS total_violations,
       SUM(CASE WHEN search_conducted = 'True' THEN 1 ELSE 0 END) AS total_searches,
       SUM(CASE WHEN is_arrested = 'True' THEN 1 ELSE 0 END) AS total_arrests
    FROM stops
    GROUP BY violation
    HAVING 
    SUM(CASE WHEN search_conducted = 'True' THEN 1 ELSE 0 END) > 500
    AND 
    SUM(CASE WHEN is_arrested = 'True' THEN 1 ELSE 0 END) > 400;""",
    "Country, Gender, Age, and Race Breakdown": """SELECT country_name, driver_gender, driver_age, driver_race, COUNT(*) AS count
                                                   FROM stops
                                                   GROUP BY driver_age, driver_race;""",
    "Top 5 Violations with Highest Arrest Rate": """SELECT violation, SUM(CASE WHEN is_arrested = 'True' THEN 1 ELSE 0 END) / COUNT(*)*100 AS arrest_rate FROM stops GROUP BY violation ORDER BY arrest_rate DESC LIMIT 5;"""
}

if choice == "Home":
    st.markdown(
        "<h1 style='font-size:30px; color:#333;'>Welcome to the Police Check Post Logs Dashboard!</h1>",
        unsafe_allow_html=True
    )
    st.image("E:/GUVI/ChatGPT Image Apr 18, 2025, 11_11_04 PM.png", width=670)

elif choice == "View Data":
    st.write("Displaying the raw data.")
    st.dataframe(df)
    st.write("### Data Summary")
    st.write(df.describe())

elif choice == "Statistics":
    st.write("### Police Stop Statistics")
    total_stops = df.shape[0]
    st.write(f"**Total Number of Police Stops**: {total_stops}")

    st.write("**Count of Stops by Violation Type**")
    violation_count = df['violation'].value_counts()
    st.bar_chart(violation_count)

    avg_age = df['driver_age'].mean()
    st.write(f"**Average Age of Drivers Stopped**: {avg_age:.2f} years")

    df['is_arrested'] = df['is_arrested'].replace({'True': 1, 'False': 0})
    df['is_arrested'] = pd.to_numeric(df['is_arrested'], errors='coerce')
    arrest_rate_by_gender = df.groupby('driver_gender').agg(total_stops=('driver_gender', 'size'),total_arrests=('is_arrested', 'sum'))
    arrest_rate_by_gender['arrest_rate'] = (arrest_rate_by_gender['total_arrests'] / arrest_rate_by_gender['total_stops'] * 100)
    st.write("**Arrest Rate by Driver Gender**")
    st.write(arrest_rate_by_gender)

elif choice == "SQL Queries":
    query_choice = st.selectbox("Select a query to run", list(queries.keys()))
    if query_choice:
        query = queries[query_choice]
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="police_check_post")
        result = pd.read_sql(query, conn)
        conn.close()

        st.write(f"### Results for: {query_choice}")
        st.dataframe(result)

elif choice == "Visualization":
    st.write("### Police Stop Data Visualizations")

    violation_trends = df.groupby([df['stop_date'].dt.month, 'violation']).size().reset_index(name='count')
    st.write("**Violation Trends Over Time (Monthly Count of Violations)**")
    chart = alt.Chart(violation_trends).mark_line().encode(x='stop_date:T',y='count:Q',color='violation:N')
    st.altair_chart(chart)

    gender_count = df['driver_gender'].fillna('Other').value_counts()
    st.write("**Count of Stops by Gender**")
    fig, ax = plt.subplots()
    ax.pie(gender_count, labels=gender_count.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)



    st.sidebar.subheader("Input Driver & Stop Details")
    stop_date = st.sidebar.date_input("Stop Date (Optional)", value=None)
    driver_gender = st.sidebar.selectbox("Driver Gender", ["Male", "Female", "Other"])
    driver_age = st.sidebar.slider("Driver Age", 16, 100, 30)
    driver_race = st.sidebar.selectbox("Driver Race", ["White", "Black", "Asian", "Hispanic", "Other"])

    violation = st.sidebar.selectbox("Violation",
                                     ["Speeding", "Moving violation", "Seat belt", "Equipment", "Registration/plates",
                                      "Other"])
    search_conducted = st.sidebar.checkbox("Search Conducted?")
    is_arrested = st.sidebar.checkbox("Was the Driver Arrested?")
    drugs_related_stop = st.sidebar.checkbox("Drug Related?")
    stop_outcome = st.sidebar.selectbox("Stop Outcome", ["Citation", "Warning", "Arrest", "No Action"])
    stop_duration = st.sidebar.selectbox("Stop Duration", ["0-15 Min", "16-30 Min", "30+ Min"])
    stop_time = st.sidebar.text_input("Stop Time (e.g., 22:15)", value="")


    if st.sidebar.button("Generate Report"):


        date_info = f" on {stop_date.strftime('%B %d, %Y')}" if stop_date else ""


        gender_text = driver_gender.lower()
        race_text = driver_race.lower()
        violation_text = violation.lower()
        outcome_text = stop_outcome.lower()
        search_text = "a search was conducted" if search_conducted else "no search was conducted"
        arrest_text = "The driver was arrested" if is_arrested else "The driver was not arrested"
        drug_text = "It was a drug-related stop" if drugs_related_stop else "It was not a drug-related stop"
        stop_time_text = f" at {stop_time}" if stop_time else ""

        st.write("### Simulating Process...")
        prog = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            prog.progress(i + 1)

        st.markdown("### 🚨 Stop Simulation Result")
        with st.container():
            st.success(
                f"A {driver_age}-year-old {race_text} {gender_text} driver was stopped for {violation_text}{stop_time_text}{date_info}. "
                f"{search_text.capitalize()}, and they received a {outcome_text}. The stop lasted {stop_duration.lower()}. "
                f"{arrest_text}. {drug_text}."
            )
