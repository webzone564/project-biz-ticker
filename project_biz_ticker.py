import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# ---------- CONFIG -----------

st.set_page_config(page_title="Project Biz Ticker", layout="centered")

# ---------- CONNECT TO GOOGLE SHEET -----------

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
service_account_info = json.loads(st.secrets["gcp_service_account"])
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(credentials)
sheet = client.open("project_biz_status").sheet1
data = pd.DataFrame(sheet.get_all_records())

# ---------- UI LOGIC -----------

st.title("🚀 Project Biz Availability")

# Let user choose their identity
user = st.selectbox("Who are you?", options=["Jai", "Rishit"])

# Show current status
my_status = data.loc[data['name'] == user, 'status'].values[0]
other_user = "Rishit" if user == "Jai" else "Jai"
other_status = data.loc[data['name'] == other_user, 'status'].values[0]

st.write(f"### ✅ You are currently: **{my_status}**")
st.write(f"### 👀 {other_user} is currently: **{other_status}**")

# Toggle
if st.button("Toggle My Status"):
    new_status = "Available" if my_status == "Not Available" else "Not Available"
    st.write("🔁 New Status to be set:", new_status)

    row = data[data['name'] == user].index[0] + 2  # +2 to match sheet row
    st.write("🧩 Row number in sheet:", row)

    try:
        sheet.update_cell(row, 2, new_status)
        st.success("✅ Sheet updated successfully!")
    except Exception as e:
        st.error(f"❌ Failed to update sheet: {e}")

    
