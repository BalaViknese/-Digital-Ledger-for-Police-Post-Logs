# -Digital-Ledger-for-Police-Post-Logs
Law Enforcement &amp; Public Safety Real-time Monitoring Systems

**What This Project Does**
This dashboard helps you:
	• View all the raw stop data
	• Run 20+ pre-built SQL queries with one click
	• See statistics like average driver age, arrest rates, etc.
	• Explore interactive visualizations (like pie charts & line charts)
	• Simulate a traffic stop using sidebar input (yep, like a mini story!)

**Purpose of the files used**

File				Description
app.py				Main Streamlit code for the dashboard
STOPS.csv			Cleaned version of the raw dataset
Police_Dataset - file.csv	Original messy dataset I used
requirements.txt		Python packages needed to run this


**Softwares Used**
	• Python 
	• Streamlit – for the UI
	• MySQL – where the data lives
	• Pandas – for data wrangling
	• Matplotlib & Altair – for visualizations
	• SQL – wrote lots of queries manually!

**Data Cleaning **
The original dataset had a bunch of missing datas. So, I:
	• Kept rows that had at least half the important data
	• Converted date/time & age columns to proper formats
	• Saved the cleaned version as STOPS.csv
This cleaned file is the one I used in MySQL and Streamlit.

**What I Learned**
	• How to build a Streamlit app from scratch
	• Writing complex SQL queries
	• Data cleaning in pandas
	• Creating pie and line charts
	• Connecting Python with MySQL
	• This was a great hands-on experience that helped me understand how everything connects—from raw data to a user-friendly dashboard.

** Future Plans**
	• Add login functionality (admin/user) using Django
	
**Thank you!**
Thanks for checking out my project! Feel free to give me feedback or suggestions.
