import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

# Page config
st.set_page_config(
    page_title="DGCA FDTL Monitor",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>

.main-title {
    text-align:center;
    font-size:42px;
    font-weight:600;
    margin-bottom:40px;
}

.center-block {
    max-width:1000px;
    margin:auto;
}

.stTabs [data-baseweb="tab-list"] {
    justify-content:center;
}

.stTabs [data-baseweb="tab"] {
    font-size:18px;
    padding:10px 20px;
}

.stTabs [aria-selected="true"] {
    color:#4A90E2 !important;
    border-bottom:3px solid #4A90E2 !important;
}

.dataframe {
    margin:auto;
}

</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-title">DGCA Flight Duty Time Limitation Monitor</div>', unsafe_allow_html=True)

# Center container
with st.container():

    st.markdown('<div class="center-block">', unsafe_allow_html=True)

    tabs = st.tabs(["Pilots", "Duty Records", "Violations"])

    # ---------------- Pilots ----------------
    with tabs[0]:

        st.subheader("Registered Pilots")

        try:
            response = requests.get(f"{API_URL}/pilots")

            if response.status_code == 200:
                pilots = response.json()
                df = pd.DataFrame(pilots)

                if df.empty:
                    st.write("No pilots found")
                else:
                    st.dataframe(df, use_container_width=True)

            else:
                st.write("API error:", response.status_code)

        except Exception as e:
            st.write("Unable to load pilots")
            st.write(e)

    # ---------------- Duty Records ----------------
    with tabs[1]:

        st.subheader("Duty Records")

        try:
            response = requests.get(f"{API_URL}/duty")

            if response.status_code == 200:
                duties = response.json()
                df = pd.DataFrame(duties)

                if df.empty:
                    st.write("No duty records found")
                else:
                    st.dataframe(df, use_container_width=True)

            else:
                st.write("API error:", response.status_code)

        except Exception as e:
            st.write("Unable to load duty records")
            st.write(e)

    # ---------------- Violations ----------------
    with tabs[2]:

        st.subheader("Detected Violations")

        try:
            response = requests.get(f"{API_URL}/violations")

            if response.status_code == 200:
                violations = response.json()
                df = pd.DataFrame(violations)

                if df.empty:
                    st.write("No violations detected")
                else:
                    st.dataframe(df, use_container_width=True)

            else:
                st.write("API error:", response.status_code)

        except Exception as e:
            st.write("Unable to load violations")
            st.write(e)

    st.markdown('</div>', unsafe_allow_html=True)