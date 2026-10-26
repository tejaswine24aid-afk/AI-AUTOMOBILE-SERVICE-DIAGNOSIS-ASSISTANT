"""
Streamlit Frontend Application for Automobile Service Diagnosis Assistant.
Communicates with FastAPI backend for vehicle diagnosis and history tracking.
"""

import streamlit as st
import requests
import pandas as pd
from typing import Dict, Any, Optional

# Constants
API_BASE_URL = "http://127.0.0.1:8000"

# Set Streamlit page configuration
st.set_page_config(
    page_title="Automobile Service Diagnosis Assistant",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Automotive Dark Theme CSS
CUSTOM_CSS = """
<style>
    /* Global Background & Typography */
    .stApp {
        background-color: #0b1120;
        color: #e2e8f0;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #cbd5e1 !important;
        font-weight: 500;
        padding: 6px 10px;
        border-radius: 6px;
    }
    
    /* Headers & Text */
    h1, h2, h3, h4 {
        color: #f8fafc !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }
    
    /* Primary Buttons */
    div.stButton > button:first-child {
        background-color: #2563eb;
        color: #ffffff;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        transition: background-color 0.2s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #1d4ed8;
        color: #ffffff;
        border: none;
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def check_api_health() -> bool:
    """Checks if the FastAPI backend service is reachable and running."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=2)
        return response.status_code == 200 and response.json().get("status") == "running"
    except Exception:
        return False


def call_diagnose_api(vehicle: str, symptom: str) -> Optional[Dict[str, Any]]:
    """Sends diagnosis request to the FastAPI backend."""
    try:
        payload = {"vehicle": vehicle, "symptom": symptom}
        response = requests.post(f"{API_BASE_URL}/api/diagnose", json=payload, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Backend returned error: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error(
            "⚠️ **Backend Unavailable:** Could not connect to FastAPI server at `http://127.0.0.1:8000`. "
            "Please ensure the backend is started using `run_app.bat` or `uvicorn backend.main:app --port 8000`."
        )
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return None


def fetch_history() -> Optional[list]:
    """Retrieves diagnosis history from the FastAPI backend."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/history", timeout=4)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return None


# Session State for Navigation & Results
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"
if "diagnosis_result" not in st.session_state:
    st.session_state.diagnosis_result = None

# Sidebar Navigation & System Status
with st.sidebar:
    st.markdown("### 🚗 AutoDiagnosis")
    st.caption("Automobile Service Assistant")
    st.divider()

    selected_page = st.radio(
        "Navigation",
        ["🏠 Home", "🔍 Diagnose Vehicle", "📋 Diagnosis History", "ℹ️ About Project"],
        index=["🏠 Home", "🔍 Diagnose Vehicle", "📋 Diagnosis History", "ℹ️ About Project"].index(
            st.session_state.page if st.session_state.page in ["🏠 Home", "🔍 Diagnose Vehicle", "📋 Diagnosis History", "ℹ️ About Project"] else "🏠 Home"
        )
    )
    st.session_state.page = selected_page

    st.divider()
    st.markdown("#### ⚡ System Status")
    is_online = check_api_health()
    if is_online:
        st.markdown("Backend: :green[● Online (FastAPI 8000)]")
    else:
        st.markdown("Backend: :red[● Offline (Port 8000)]")

    st.divider()
    st.caption("College 1-Credit Mini Project\nBuilt with FastAPI & Streamlit")


# ==========================================
# PAGE 1: HOME PAGE
# ==========================================
if st.session_state.page == "🏠 Home":
    st.title("🚗 Automobile Service Diagnosis Assistant")
    st.markdown("A clean, user-friendly tool to identify possible automobile problems from reported vehicle symptoms.")

    st.write("")
    
    # 3 Feature Containers
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.markdown("### 🔍 Diagnose")
            st.write("Enter your vehicle problem or choose from common symptom categories.")
    with col2:
        with st.container(border=True):
            st.markdown("### ⚙️ Simple Analysis")
            st.write("Get immediate assessment of root causes and problem severity level.")
    with col3:
        with st.container(border=True):
            st.markdown("### 🛠️ Service Guidance")
            st.write("View step-by-step basic DIY checks and recommended repair actions.")

    st.write("")

    # Call to Action Button
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        if st.button("🚀 Start Diagnosis", use_container_width=True):
            st.session_state.page = "🔍 Diagnose Vehicle"
            st.rerun()

    st.divider()
    st.info("🛡️ **Note:** This application acts as a preliminary rule-based diagnosis assistant designed for educational and practical vehicle troubleshooting guidance.")


# ==========================================
# PAGE 2: DIAGNOSIS PAGE
# ==========================================
elif st.session_state.page == "🔍 Diagnose Vehicle":
    st.title("🔍 Vehicle Service Diagnosis")
    st.write("Describe the issue with your vehicle or select a common symptom from the list below.")

    common_symptom_options = [
        "-- Select a common symptom (optional) --",
        "Battery / Starting Problem",
        "Engine Overheating",
        "Brake Problem",
        "Flat Tyre",
        "Engine Oil Problem",
        "AC Not Cooling",
        "Engine Misfire",
        "Poor Acceleration",
        "Check Engine Light",
        "Alternator Problem"
    ]

    with st.container(border=True):
        col_v, col_s = st.columns([1, 2])
        with col_v:
            vehicle_type = st.selectbox(
                "🚗 Vehicle Type",
                ["Car", "Bike", "SUV", "Van"],
                help="Select the vehicle type"
            )
        with col_s:
            selected_symptom = st.selectbox(
                "📋 Common Symptoms",
                common_symptom_options,
                help="Optionally pick a pre-categorized issue"
            )

        problem_description = st.text_area(
            "📝 Describe Your Problem",
            placeholder="Example: My car is overheating and the temperature gauge is very high.",
            height=110,
            help="Type your custom observation or leave blank if a common symptom is selected."
        )

        st.caption("💡 *Tip: You can either type your symptoms in detail or select from the common symptom dropdown.*")

        diagnose_clicked = st.button("🔍 Diagnose Problem", use_container_width=True)

    if diagnose_clicked:
        # Determine the final symptom query
        final_symptom = ""
        if problem_description.strip():
            final_symptom = problem_description.strip()
            # If both are specified, combine them
            if selected_symptom != common_symptom_options[0]:
                final_symptom = f"{selected_symptom}: {final_symptom}"
        elif selected_symptom != common_symptom_options[0]:
            final_symptom = selected_symptom

        if not final_symptom:
            st.warning("⚠️ Please provide a problem description or select a common symptom.")
        else:
            with st.spinner("Analyzing automobile symptoms via FastAPI backend..."):
                result = call_diagnose_api(vehicle=vehicle_type, symptom=final_symptom)
                if result:
                    st.session_state.diagnosis_result = result

    # Display Result Section if available
    if st.session_state.diagnosis_result:
        res = st.session_state.diagnosis_result
        st.divider()
        st.subheader("📋 Diagnosis Result")

        # Format severity
        sev = res.get("severity", "Low").capitalize()
        if sev == "Urgent":
            severity_badge = ":red[🔴 **Urgent**]"
        elif sev == "High":
            severity_badge = ":orange[🟠 **High**]"
        elif sev == "Medium":
            severity_badge = ":violet[🟡 **Medium**]"
        else:
            severity_badge = ":green[🟢 **Low**]"

        # Main Diagnosis Card using native container
        with st.container(border=True):
            col_left, col_right = st.columns([3, 1])
            with col_left:
                st.caption(f"🚗 VEHICLE: **{res.get('vehicle', 'Car').upper()}**")
                st.markdown(f"### {res.get('problem', 'Vehicle Diagnosis')}")
            with col_right:
                st.caption("SEVERITY LEVEL")
                st.markdown(f"### {severity_badge}")

            st.divider()

            st.markdown(f"**Reported Symptom:** *\"{res.get('symptom', '')}\"*")
            st.write("")

            # Possible Cause Callout
            st.info(f"🔍 **Possible Cause:**\n\n{res.get('possible_cause', 'Unknown')}")

            # Basic Checks & Recommended Action in Two Columns
            col_checks, col_action = st.columns(2)
            
            with col_checks:
                with st.container(border=True):
                    st.markdown("#### 🔧 Basic Checks")
                    checks = res.get("basic_checks", [])
                    if checks:
                        for check in checks:
                            st.markdown(f"- {check}")
                    else:
                        st.write("No specific preliminary checks required.")

            with col_action:
                with st.container(border=True):
                    st.markdown("#### 🛠️ Recommended Action")
                    action_msg = res.get('recommended_action', 'Consult a qualified service technician.')
                    if sev in ["Urgent", "High"]:
                        st.warning(f"**Next Steps:**\n\n{action_msg}")
                    else:
                        st.success(f"**Next Steps:**\n\n{action_msg}")

            st.write("")
            # Disclaimer Box
            disclaimer_msg = res.get(
                "disclaimer",
                "This is a preliminary diagnosis assistant. Consult a qualified mechanic for final inspection and repair."
            )
            st.caption(f"🛡️ **Disclaimer:** {disclaimer_msg}")


# ==========================================
# PAGE 3: HISTORY PAGE
# ==========================================
elif st.session_state.page == "📋 Diagnosis History":
    st.title("📋 Past Diagnosis History")
    st.write("Review all previously analyzed diagnosis records stored in the SQLite database.")

    col_ref, _ = st.columns([1, 4])
    with col_ref:
        if st.button("🔄 Refresh Records"):
            st.rerun()

    history_records = fetch_history()

    if history_records is None:
        st.error(
            "⚠️ Unable to load history from backend. Please verify FastAPI is running at `http://127.0.0.1:8000`."
        )
    elif len(history_records) == 0:
        st.info("ℹ️ No diagnosis records found yet. Go to **Diagnose Vehicle** to perform your first diagnosis.")
    else:
        # Convert to Pandas DataFrame for clean tabular presentation
        df = pd.DataFrame(history_records)
        
        display_df = df.rename(columns={
            "id": "ID",
            "date": "Date & Time",
            "vehicle": "Vehicle",
            "symptom": "Reported Symptom",
            "diagnosis": "Diagnosed Problem",
            "severity": "Severity"
        })

        st.markdown(f"**Total Records Stored:** `{len(df)}`")
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


# ==========================================
# PAGE 4: ABOUT PAGE
# ==========================================
elif st.session_state.page == "ℹ️ About Project":
    st.title("ℹ️ About the Project")
    
    with st.container(border=True):
        st.markdown("### 🚗 Automobile Service Diagnosis Assistant")
        st.write(
            "The **Automobile Service Diagnosis Assistant** is a web-based decision-support mini project "
            "that helps automobile owners, drivers, and service technicians perform preliminary problem identification "
            "from reported vehicle symptoms."
        )

    st.write("")

    col_t, col_o = st.columns(2)
    with col_t:
        with st.container(border=True):
            st.markdown("### 🛠️ Technologies Used")
            st.markdown(
                "- **Python 3** — Core programming language\n"
                "- **FastAPI** — High-performance RESTful API backend\n"
                "- **Streamlit** — Interactive web frontend interface\n"
                "- **SQLite** — Lightweight embedded database for history logging\n"
                "- **Pydantic** — Data validation and schema enforcement\n"
                "- **Requests** — HTTP client for Streamlit-to-FastAPI communication"
            )

    with col_o:
        with st.container(border=True):
            st.markdown("### 🎯 Project Objective")
            st.write(
                "*“To provide a simple, clean, and user-friendly tool for preliminary automobile problem identification, "
                "severity assessment, and service guidance.”*"
            )
            st.divider()
            st.markdown(
                "**Academic Scope:** 1-Credit Academic Mini Project  \n"
                "**Architecture:** Client (Streamlit) ➔ API (FastAPI) ➔ Knowledge Base & SQLite"
            )

    st.write("")
    st.info(
        "🛡️ **Academic Disclaimer:** This project is developed for educational purposes to demonstrate "
        "API-driven architecture and rule-based diagnostic systems. It does not replace certified automotive mechanic inspections."
    )
