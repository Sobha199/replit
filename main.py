
import streamlit as st
import pandas as pd
import datetime
from io import BytesIO

# Load Data
login_df = pd.read_csv(Tracking Sample (1).csv")
login_df.columns = login_df.columns.str.strip().str.lower().str.replace(" ", "_")
tracking_df = pd.read_csv("Tracking Sample (1).csv")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'emp_id' not in st.session_state:
    st.session_state.emp_id = None

# Set page config
st.set_page_config(page_title="S2M Portal", layout="centered")

# Apply theme
st.markdown("""
    <style>
    body {background-color: white;}
    .stTextInput > div > div > input {
        border: 2px solid black;
    }
    </style>
""", unsafe_allow_html=True)

# Page 1 - Login
def login_page():
    tracking_df = pd.read_csv(""Login tracking.csv")
    st.image("s2m-logo.png", width=200)
    st.title("S2M Health Private Ltd Login")
    username = st.text_input("username")
    password = st.text_input("password", type="password")
    if st.button("Sign In"):
        with st.spinner("Logging in..."):
            user_row = login_df[(login_df['username'] == username) & (login_df['password'] == password)]
            if not user_row.empty:
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.session_state.emp_id = user_row.iloc[0]['Emp ID']
                st.session_state.emp_name = user_row.iloc[0]['Emp Name']
                st.session_state.team_lead = user_row.iloc[0]['Team Lead']
            else:
                st.error("Invalid username or password")

# Page 2 - Form Input
def form_page():
    st.title("Data Entry Form")
    today = datetime.date.today()
    emp_id = st.session_state.emp_id
    emp_name = st.session_state.emp_name
    team_lead = st.session_state.team_lead

    with st.form("entry_form"):
        date = st.date_input("Date", value=today)
        st.text_input("Emp ID", value=emp_id, disabled=True)
        st.text_input("Emp Name", value=emp_name, disabled=True)
        project = st.selectbox("Project", ["Elevance MA", "Elevance ACA", "Health OS"])
        project_category = st.selectbox("Project Category", ["Entry", "Recheck", "QA"])
        login_name = st.multiselect("Login Name", login_df["Login Name"].unique())
        login_id = st.text_input("Login ID", value=", ".join([str(login_df[login_df["Login Name"] == name]["Login ID"].values[0]) for name in login_name]) if login_name else "", disabled=True)
        st.text_input("Team Lead", value=team_lead, disabled=True)
        chart_id = st.text_input("Chart ID")
        page_no = st.number_input("Page No", min_value=1)
        no_of_dos = st.number_input("No of DOS", min_value=0)
        no_of_codes = st.number_input("No of Codes", min_value=0)
        error_type = st.text_input("Error Type")
        error_comments = st.text_input("Error Comments")
        no_of_errors = st.number_input("No of Errors", min_value=0)
        chart_status = st.selectbox("Chart Status", ["Completed", "Pending", "Rejected"])
        auditor_emp_id = st.text_input("Auditor Emp ID")
        auditor_emp_name = st.text_input("Auditor Emp Name")
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            new_row = pd.DataFrame([[date, emp_id, emp_name, project, project_category, login_id, ", ".join(login_name), team_lead, chart_id, page_no, no_of_dos, no_of_codes, error_type, error_comments, no_of_errors, chart_status, auditor_emp_id, auditor_emp_name]],
                columns=tracking_df.columns)
            tracking_df.loc[len(tracking_df)] = new_row.iloc[0]
            tracking_df.to_csv("Tracking Sample (1).csv", index=False)
            st.success("Data submitted successfully!")
            st.dataframe(new_row)

# Page 3 - Dashboard
def dashboard_page():
    st.title("Dashboard")
    df = pd.read_csv("Tracking Sample (1).csv")
    st.metric("Working Days", df["Date"].nunique())
    st.metric("No of Charts", df["Chart id"].nunique())
    st.metric("No of DOS", df["No of Dos"].sum())
    st.metric("No of ICD", df["No of codes"].sum())
    working_hours = df["Date"].nunique() * 8
    cph = round(df["No of codes"].sum() / working_hours, 2) if working_hours else 0
    st.metric("CPH", cph)

# Page routing
if not st.session_state.logged_in:
    login_page()
else:
    menu = st.sidebar.radio("Navigation", ["Form", "Dashboard"])
    if menu == "Form":
        form_page()
    else:
        dashboard_page()
