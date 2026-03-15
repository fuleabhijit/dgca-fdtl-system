import streamlit as st
import requests
import pandas as pd
from datetime import datetime, date, time

API_URL = "https://dgca-fdtl-system-1.onrender.com"

st.set_page_config(
    page_title="FDTL Compliance Monitor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@500;600&display=swap');

html, body, [class*="css"], .stApp {
    background-color: #0a0a0a !important;
    font-family: 'DM Mono', monospace !important;
    color: #f0efe8 !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.stTabs [data-baseweb="tab-list"] {
    background: #0a0a0a !important;
    border-bottom: 0.5px solid #1e1e1e !important;
    padding: 0 32px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #444 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    padding: 14px 20px !important;
    border: none !important;
    border-bottom: 1.5px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #f0efe8 !important;
    border-bottom: 1.5px solid #f0efe8 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding: 28px 32px !important;
    background: #0a0a0a !important;
}
[data-testid="metric-container"] {
    background: #0f0f0f !important;
    border: 0.5px solid #1e1e1e !important;
    border-radius: 0 !important;
    padding: 20px 24px !important;
}
[data-testid="metric-container"] label {
    font-size: 9px !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #444 !important;
    font-family: 'DM Mono', monospace !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 32px !important;
    font-weight: 500 !important;
    color: #f0efe8 !important;
}
[data-testid="stDataFrame"] {
    border: 0.5px solid #1a1a1a !important;
    border-radius: 0 !important;
}
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label,
[data-testid="stDateInput"] label,
[data-testid="stTimeInput"] label,
[data-testid="stTextInput"] label {
    font-size: 9px !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #444 !important;
    font-family: 'DM Mono', monospace !important;
}
[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
[data-testid="stTimeInput"] input,
[data-testid="stTextInput"] input {
    background: #0f0f0f !important;
    border: 0.5px solid #1e1e1e !important;
    border-radius: 0 !important;
    color: #f0efe8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
}
.stButton > button {
    background: #f0efe8 !important;
    color: #0a0a0a !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    padding: 10px 24px !important;
    width: 100% !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
[data-testid="stAlert"] {
    border-radius: 0 !important;
    background: #0f0f0f !important;
    border: 0.5px solid #1e1e1e !important;
    border-left: 2px solid #f0efe8 !important;
    font-size: 11px !important;
    font-family: 'DM Mono', monospace !important;
    color: #888 !important;
}
.sec {
    font-size: 9px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #333;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 0.5px solid #1a1a1a;
}
</style>
""", unsafe_allow_html=True)


# ── HELPERS ───────────────────────────────────────────────────────────────────
def safe_get(endpoint, params=None):
    try:
        r = requests.get(f"{API_URL}{endpoint}", params=params, timeout=10)
        if r.status_code == 200 and r.text.strip():
            return r.json()
        return []
    except Exception:
        return []


def safe_post(endpoint, params):
    try:
        r = requests.post(f"{API_URL}{endpoint}", params=params, timeout=10)
        if r.status_code == 200 and r.text.strip():
            return r.json(), None
        return None, r.json().get("detail", r.text) if r.text else f"Error {r.status_code}"
    except Exception as e:
        return None, str(e)


# ── TOPBAR ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#0a0a0a;padding:0 32px;height:52px;
            display:flex;align-items:center;justify-content:space-between;
            border-bottom:0.5px solid #1a1a1a;">
    <div style="display:flex;align-items:center;gap:12px;">
        <div style="width:28px;height:28px;border:1px solid #2a2a2a;
                    display:flex;align-items:center;justify-content:center;
                    font-size:10px;color:#555;font-family:'DM Mono',monospace;">FD</div>
        <div>
            <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:500;
                        color:#f0efe8;letter-spacing:0.05em;">FDTL Compliance Monitor</div>
            <div style="font-size:9px;color:#2a2a2a;letter-spacing:0.1em;
                        text-transform:uppercase;font-family:'DM Mono',monospace;">
                DGCA CAR Section 7 · Series C Part II</div>
        </div>
    </div>
    <div style="display:flex;align-items:center;gap:6px;">
        <span style="width:5px;height:5px;border-radius:50%;background:#f0efe8;
                     display:inline-block;"></span>
        <span style="font-size:9px;color:#444;letter-spacing:0.1em;
                     text-transform:uppercase;font-family:'DM Mono',monospace;">
            Live</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ── FETCH DATA ────────────────────────────────────────────────────────────────
pilots     = safe_get("/pilots")
duties     = safe_get("/duty")
violations = safe_get("/violations")
pilot_map  = {p["id"]: p["name"] for p in pilots}
high_v     = sum(1 for v in violations if v.get("severity") == "HIGH")
medium_v   = sum(1 for v in violations if v.get("severity") == "MEDIUM")


# ── METRICS ───────────────────────────────────────────────────────────────────
st.markdown("<div style='padding:24px 32px 0;background:#0a0a0a;'>", unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Pilots",          len(pilots))
c2.metric("Duty Records",    len(duties))
c3.metric("Violations",      len(violations))
c4.metric("High Severity",   high_v)
c5.metric("Medium Severity", medium_v)
st.markdown("</div>", unsafe_allow_html=True)


# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview", "Duty Records", "Violations", "AI Analysis", "Add Record"
])


# ════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec">Recent Violations</div>', unsafe_allow_html=True)

    if violations:
        for v in violations[:8]:
            sev  = v.get("severity", "LOW")
            bg   = {"HIGH": "#f0efe8", "MEDIUM": "#1a1a1a"}.get(sev, "transparent")
            fg   = {"HIGH": "#0a0a0a", "MEDIUM": "#888"}.get(sev, "#333")
            bord = "" if sev != "LOW" else "border:0.5px solid #222;"
            name = pilot_map.get(v.get("pilot_id"), "Unknown")
            st.markdown(f"""
            <div style="padding:11px 0;border-bottom:0.5px solid #111;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                    <span style="font-size:10px;color:#c8c7c0;font-family:'DM Mono',monospace;">{name}</span>
                    <span style="font-size:9px;background:{bg};color:{fg};padding:2px 8px;
                                 letter-spacing:0.1em;font-family:'DM Mono',monospace;{bord}">{sev}</span>
                </div>
                <div style="font-size:9px;color:#333;font-family:'DM Mono',monospace;">{v.get('violation_type','—')}</div>
                <div style="font-size:10px;color:#555;margin-top:3px;font-family:'DM Mono',monospace;">{v.get('description','—')}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No violations recorded.")

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec">Registered Pilots</div>', unsafe_allow_html=True)
    if pilots:
        st.dataframe(pd.DataFrame(pilots), use_container_width=True, hide_index=True)
    else:
        st.info("No pilots registered.")


# ════════════════════════════════════════════════════════════════════
# TAB 2 — DUTY RECORDS
# ════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec">Duty Period Records</div>', unsafe_allow_html=True)
    if duties:
        df_du = pd.DataFrame(duties)
        df_du["pilot_name"] = df_du["pilot_id"].map(pilot_map).fillna("Unknown")
        show = ["id", "pilot_name", "duty_start", "duty_end"]
        if "duration_hours" in df_du.columns:
            show.append("duration_hours")
        st.dataframe(df_du[show], use_container_width=True, hide_index=True)
    else:
        st.info("No duty records found.")


# ════════════════════════════════════════════════════════════════════
# TAB 3 — VIOLATIONS
# ════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec">Violation Log</div>', unsafe_allow_html=True)

    f1, f2 = st.columns(2)
    with f1:
        sev_filter = st.selectbox("Severity", ["ALL", "HIGH", "MEDIUM", "LOW"])
    with f2:
        p_opts = {"ALL": None}
        p_opts.update({p["name"]: p["id"] for p in pilots})
        p_filter = st.selectbox("Pilot", list(p_opts.keys()))

    params = {}
    if sev_filter != "ALL":
        params["severity"] = sev_filter
    if p_opts.get(p_filter):
        params["pilot_id"] = p_opts[p_filter]

    fv = safe_get("/violations", params=params)
    if fv:
        df_v = pd.DataFrame(fv)
        if "pilot_id" in df_v.columns:
            df_v["pilot_name"] = df_v["pilot_id"].map(pilot_map).fillna("Unknown")
        show_v = [c for c in ["id","pilot_name","violation_type","description","severity"]
                  if c in df_v.columns]

        def sev_style(val):
            if val == "HIGH":   return "background-color:#f0efe8;color:#0a0a0a"
            if val == "MEDIUM": return "background-color:#1a1a1a;color:#888"
            if val == "LOW":    return "color:#333"
            return ""

        st.dataframe(
            df_v[show_v].style.applymap(sev_style, subset=["severity"]),
            use_container_width=True, hide_index=True
        )
    else:
        st.info("No violations match the selected filters.")


# ════════════════════════════════════════════════════════════════════
# TAB 4 — AI ANALYSIS
# ════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec">Groq AI — Violation Analysis</div>', unsafe_allow_html=True)

    a1, a2 = st.columns([1, 2])
    with a1:
        vid = st.number_input("Violation ID", min_value=1, step=1)
        run = st.button("Run Analysis")
    with a2:
        if run:
            result = safe_get(f"/violations/{int(vid)}/explain")
            if isinstance(result, dict) and "ai_explanation" in result:
                st.markdown(f"""
                <div style="background:#0f0f0f;border:0.5px solid #1e1e1e;padding:20px 24px;">
                    <div style="display:flex;gap:32px;margin-bottom:14px;padding-bottom:14px;
                                border-bottom:0.5px solid #1a1a1a;">
                        <div>
                            <div style="font-size:9px;letter-spacing:0.12em;text-transform:uppercase;
                                        color:#333;margin-bottom:4px;font-family:'DM Mono',monospace;">Pilot</div>
                            <div style="font-size:12px;color:#f0efe8;font-family:'DM Mono',monospace;">
                                {result['pilot']}</div>
                        </div>
                        <div>
                            <div style="font-size:9px;letter-spacing:0.12em;text-transform:uppercase;
                                        color:#333;margin-bottom:4px;font-family:'DM Mono',monospace;">Violation</div>
                            <div style="font-size:12px;color:#f0efe8;font-family:'DM Mono',monospace;">
                                {result['violation_type']}</div>
                        </div>
                    </div>
                    <div style="font-size:11px;color:#888;line-height:1.8;
                                font-family:'DM Mono',monospace;">{result['ai_explanation']}</div>
                </div>
                """, unsafe_allow_html=True)
            elif isinstance(result, dict) and "error" in result:
                st.error(result["error"])
            else:
                st.error("No result. Check the Violation ID.")
        else:
            st.markdown("""
            <div style="background:#0f0f0f;border:0.5px solid #1a1a1a;padding:24px;
                        color:#333;font-size:11px;line-height:1.8;font-family:'DM Mono',monospace;">
                Enter a Violation ID and click Run Analysis.
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# TAB 5 — ADD RECORD
# ════════════════════════════════════════════════════════════════════
with tab5:
    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown('<div class="sec">Register Pilot</div>', unsafe_allow_html=True)
        pilot_name_input = st.text_input("Full Name",   placeholder="e.g. Rajesh Sharma")
        emp_id_input     = st.text_input("Employee ID", placeholder="e.g. AI-006")
        if st.button("Register Pilot"):
            if not pilot_name_input.strip() or not emp_id_input.strip():
                st.error("Both fields are required.")
            else:
                data, err = safe_post("/pilots/", {
                    "name": pilot_name_input.strip(),
                    "employee_id": emp_id_input.strip()
                })
                if data is not None:
                    st.success(f"Pilot registered — {data.get('name')}  |  ID: {data.get('id')}")
                else:
                    st.error(f"Failed: {err}")

    with col_b:
        st.markdown('<div class="sec">Log Duty Period</div>', unsafe_allow_html=True)
        if not pilots:
            st.warning("No pilots found. Register a pilot first.")
        else:
            pilot_choices  = {p["name"]: p["id"] for p in pilots}
            selected_pilot = st.selectbox("Pilot", list(pilot_choices.keys()))

            d1, d2 = st.columns(2)
            with d1:
                start_date = st.date_input("Start Date", value=date.today(), key="sd")
                start_time = st.time_input("Start Time", value=time(6, 0),   key="st")
            with d2:
                end_date = st.date_input("End Date",   value=date.today(), key="ed")
                end_time = st.time_input("End Time",   value=time(19, 0),  key="et")

            duty_start_dt = datetime.combine(start_date, start_time)
            duty_end_dt   = datetime.combine(end_date,   end_time)
            duration      = (duty_end_dt - duty_start_dt).total_seconds() / 3600

            over      = duration > 13
            dur_color = "#f0efe8" if over else "#555"
            warn      = "EXCEEDS 13H LIMIT" if over else ""
            st.markdown(
                f'<div style="margin:12px 0;padding:10px 16px;border:0.5px solid #1a1a1a;'
                f'background:#0a0a0a;display:flex;align-items:baseline;gap:12px;">'
                f'<span style="font-size:9px;color:#333;letter-spacing:0.12em;'
                f'text-transform:uppercase;">Duration</span>'
                f'<span style="font-size:22px;color:{dur_color};">{duration:.1f} h</span>'
                f'<span style="font-size:9px;color:#f0efe8;letter-spacing:0.1em;">{warn}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

            if st.button("Log Duty Record"):
                if duration <= 0:
                    st.error("End time must be after start time.")
                else:
                    data, err = safe_post("/duty/", {
                        "pilot_id":   pilot_choices[selected_pilot],
                        "duty_start": duty_start_dt.isoformat(),
                        "duty_end":   duty_end_dt.isoformat()
                    })
                    if data is not None:
                        hrs = data.get("duration_hours") or round(duration, 2)
                        st.success(f"Duty logged — {selected_pilot}  |  {hrs} h")
                        if over:
                            st.warning("Violation detected — check the Violations tab.")
                    else:
                        st.error(f"Failed: {err}")