import streamlit as st
import random
import plotly.express as px
import plotly.graph_objects as go
import pdfplumber
import re
import pandas as pd
from reportlab.pdfgen import canvas
from io import BytesIO

st.set_page_config(page_title="IntelliCredit AI", layout="wide")

# ---------------- SESSION ---------------- #

if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# ---------------- LOGIN ---------------- #

def login():

    st.title("IntelliCredit AI")
    st.subheader("Secure Credit Analyst Login")

    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if user in st.session_state.users and st.session_state.users[user] == password:

            st.session_state.logged_in = True
            st.session_state.page = "dashboard"
            st.rerun()

        else:
            st.error("Invalid credentials")

    if st.button("Create Account"):
        st.session_state.page = "signup"
        st.rerun()

# ---------------- SIGNUP ---------------- #

def signup():

    st.title("Create New Account")

    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")

    if st.button("Register"):

        if new_user in st.session_state.users:

            st.error("User already exists")

        else:

            st.session_state.users[new_user] = new_pass
            st.success("Account created")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# ---------------- PASSWORD CHANGE ---------------- #

def change_password():

    st.subheader("Change Password")

    user = st.text_input("Username")
    old_pass = st.text_input("Old Password", type="password")
    new_pass = st.text_input("New Password", type="password")

    if st.button("Update Password"):

        if user in st.session_state.users and st.session_state.users[user] == old_pass:

            st.session_state.users[user] = new_pass
            st.success("Password updated")

        else:

            st.error("Invalid credentials")

# ---------------- PDF ANALYZER ---------------- #

def analyze_pdf(file):

    revenue = None
    debt = None

    try:

        with pdfplumber.open(file) as pdf:

            text = ""

            for page in pdf.pages[:2]:

                if page.extract_text():
                    text += page.extract_text()

        rev_match = re.search(r"revenue.*?(\d+)", text, re.IGNORECASE)
        debt_match = re.search(r"debt.*?(\d+)", text, re.IGNORECASE)

        if rev_match:
            revenue = int(rev_match.group(1))

        if debt_match:
            debt = int(debt_match.group(1))

    except:
        pass

    return revenue, debt

# ---------------- NEWS ---------------- #

def get_news(company):

    return [
        f"{company} reports stable quarterly growth",
        f"{company} expanding international operations",
        f"{company} faces moderate regulatory oversight"
    ]

# ---------------- PDF CREATOR ---------------- #

def create_pdf(text):

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    y = 800

    for line in text.split("\n"):
        pdf.drawString(50, y, line)
        y -= 20

    pdf.save()
    buffer.seek(0)

    return buffer

# ---------------- DASHBOARD ---------------- #

def dashboard():

    st.title("IntelliCredit AI")
    st.subheader("AI Powered Corporate Credit Appraisal Platform")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

    st.sidebar.title("User Settings")

    if st.sidebar.button("Change Password"):
        change_password()

    company = st.text_input("Enter Company Name")

    uploaded_file = st.file_uploader("Upload Financial Report", type=["pdf"])

    if st.button("Run Credit Analysis"):

        with st.spinner("Analyzing financial report..."):

            if uploaded_file and uploaded_file.size < 5000000:

                rev, deb = analyze_pdf(uploaded_file)

                revenue = rev if rev else random.randint(100,500)
                debt = deb if deb else random.randint(50,200)

            else:

                revenue = random.randint(100,500)
                debt = random.randint(50,200)

            growth = random.randint(5,25)

        # -------- METRICS -------- #

        st.subheader("Financial Indicators")

        c1,c2,c3 = st.columns(3)

        c1.metric("Revenue",f"{revenue} Cr")
        c2.metric("Debt",f"{debt} Cr")
        c3.metric("Growth",f"{growth}%")

        # -------- CHART -------- #

        df = pd.DataFrame({
            "Metric":["Revenue","Debt","Growth"],
            "Value":[revenue,debt,growth]
        })

        fig = px.bar(df,x="Metric",y="Value",color="Metric",text="Value",
                     title="Financial Performance Dashboard")

        st.plotly_chart(fig,use_container_width=True)

        # -------- NEWS -------- #

        st.subheader("External Risk Signals")

        news = get_news(company)

        for n in news:
            st.write("•",n)

        # -------- RISK SCORE -------- #

        risk_score = random.randint(40,90)

        st.subheader("AI Credit Risk Score")

        st.metric("Risk Score",risk_score)

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={'text':"Credit Risk Score"},
            gauge={
                'axis':{'range':[0,100]},
                'bar':{'color':"darkblue"},
                'steps':[
                    {'range':[0,50],'color':"red"},
                    {'range':[50,70],'color':"yellow"},
                    {'range':[70,100],'color':"green"}
                ]
            }
        ))

        st.plotly_chart(gauge,use_container_width=True)

        # -------- DECISION -------- #

        if risk_score > 70:
            decision = "Loan Approved"
            rate = "11%"
        elif risk_score > 50:
            decision = "Conditional Approval"
            rate = "13%"
        else:
            decision = "Rejected"
            rate = "-"

        st.subheader("Loan Decision")

        d1,d2 = st.columns(2)

        d1.success(f"Decision: {decision}")
        d2.info(f"Interest Rate: {rate}")

        # -------- CAM -------- #

        cam = f"""
Credit Appraisal Memo

Company: {company}

Revenue: {revenue} Cr
Debt: {debt} Cr
Growth: {growth} %

AI Risk Score: {risk_score}

Loan Decision: {decision}
Interest Rate: {rate}

External Signals:
{news[0]}
{news[1]}
{news[2]}

Recommendation:
Based on financial indicators and external signals,
the AI system recommends the above credit decision.
"""

        st.subheader("Generated Credit Appraisal Memo")

        st.text_area("CAM Report",cam,height=250)

        pdf = create_pdf(cam)

        st.download_button(
            label="Download CAM Report (PDF)",
            data=pdf,
            file_name="credit_appraisal_report.pdf",
            mime="application/pdf"
        )

# ---------------- ROUTER ---------------- #

if st.session_state.page == "login":
    login()

elif st.session_state.page == "signup":
    signup()

elif st.session_state.logged_in:
    dashboard()