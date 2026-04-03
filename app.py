import streamlit as st
import pandas as pd
from datetime import datetime
from jinja2 import Template
import weasyprint
import os
from supabase import create_client, Client  # For research data persistence

# ====================== CONFIG ======================
st.set_page_config(page_title="VitaAI Doctor - Research", page_icon="🩺", layout="wide")
st.title("🩺 VitaAI Doctor")
st.caption("Research Edition | Symptom Analysis + Lifestyle Plan | 2000-Patient Study")

# Medical icons from healthicons.org (free)
st.sidebar.image("https://healthicons.org/icons/svg/stethoscope.svg", width=80)

# ====================== RESEARCHER MODE ======================
PASSWORD = st.sidebar.text_input("Researcher Password (for dashboard)", type="password")
if PASSWORD == "research2026":  # Change this to your own secure password
    st.sidebar.success("✅ Researcher Mode Unlocked")
    researcher_mode = True
else:
    researcher_mode = False

# ====================== SUPABASE SETUP (for 2000 patients) ======================
# Get your free Supabase project at https://supabase.com (5 min setup)
# Then add these in Streamlit Cloud → Settings → Secrets
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "your-supabase-url")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "your-anon-key")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL != "your-supabase-url" else None

def save_to_research_db(data):
    if supabase:
        supabase.table("patient_research").insert(data).execute()

# ====================== PATIENT FORM ======================
st.header("Patient Input")

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", 1, 120, 41)
    height_cm = st.number_input("Height (cm)", 100, 250, 168)
    weight_kg = st.number_input("Weight (kg)", 30, 200, 70)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

with col2:
    lifestyle = st.text_area("Lifestyle (job, commute, exercise, sleep, diet)", 
                            "Desk job AGM HR, bus commute 5:30AM-9PM, minimal walking, office work")
    symptoms = st.text_area("Symptoms & how many days?", 
                           "Left heel pain since January 2026 (3+ months)")
    duration = st.number_input("Duration of symptoms (days)", 1, 3650, 90)

consent = st.checkbox("✅ I consent to my **anonymized** data being used for research purposes (optional but helps the 2000-patient study)")

if st.button("🔍 Get AI Analysis & Report", type="primary"):
    if not consent and st.checkbox("Skip consent (data will not be saved for research)"):
        pass
    else:
        # ====================== MOCK AI ANALYSIS (replace with real API later) ======================
        # You can later replace this with Gemini / Grok API call
        analysis = {
            "summary": "Mild Vitamin D deficiency likely contributing to heel pain. No major systemic disease.",
            "lifestyle": "Add 15-min daily walk + sun exposure. Ergonomic desk setup. Calf/heel stretches 3x/day.",
            "food": "Daily: Fatty fish/egg + fortified milk. Weekly menu: Dal, rice, vegetables, yogurt, banana.",
            "doctor": "Neuromedicine + Orthopedics follow-up. Endocrinologist if Vitamin D remains low.",
            "tests": "Repeat Vitamin D, Serum Calcium, Foot X-ray if pain persists.",
            "red_flags": "Seek urgent care if numbness, swelling, or fever appears."
        }

        # Save anonymized research data
        research_data = {
            "timestamp": datetime.now().isoformat(),
            "age": age,
            "gender": gender,
            "bmi": round(weight_kg / ((height_cm/100)**2), 1),
            "symptoms": symptoms,
            "duration_days": duration,
            "lifestyle_summary": lifestyle[:100]
        }
        if consent and supabase:
            save_to_research_db(research_data)

        # ====================== BEAUTIFUL REPORT ======================
        st.success("✅ Analysis Complete!")
        
        # HTML template for professional PDF
        html_template = Template("""
        <h1 style="text-align:center; color:#0d9488;">VitaAI Doctor Research Report</h1>
        <p><strong>Date:</strong> {{ date }} | <strong>Patient ID:</strong> ANON-{{ pid }}</p>
        <h2>Summary</h2><p>{{ summary }}</p>
        <h2>Lifestyle Recommendations</h2><p>{{ lifestyle }}</p>
        <h2>Food Habits (Bangladesh-friendly)</h2><p>{{ food }}</p>
        <h2>Recommended Doctor & Tests</h2><p>{{ doctor }}<br>{{ tests }}</p>
        <hr><p style="color:#666; font-size:0.8em;">Disclaimer: Research & informational only. Not medical advice.</p>
        """)
        
        rendered_html = html_template.render(
            date=datetime.now().strftime("%d %b %Y"),
            pid=str(abs(hash(str(datetime.now()))) % 100000),
            summary=analysis["summary"],
            lifestyle=analysis["lifestyle"],
            food=analysis["food"],
            doctor=analysis["doctor"],
            tests=analysis["tests"]
        )
        
        # Generate PDF
        pdf_bytes = weasyprint.HTML(string=rendered_html).write_pdf()
        
        colA, colB = st.columns(2)
        with colA:
            st.download_button("📄 Download PDF Report", pdf_bytes, f"vitaai_report_{datetime.now().strftime('%Y%m%d')}.pdf", "application/pdf")
        with colB:
            st.download_button("📊 Download CSV for Research", pd.DataFrame([research_data]).to_csv(index=False).encode(), "patient_data.csv", "text/csv")

        # Display nice report
        st.subheader("AI Analysis")
        for k, v in analysis.items():
            st.write(f"**{k.title()}:** {v}")

# ====================== RESEARCHER DASHBOARD ======================
if researcher_mode:
    st.header("📊 Researcher Dashboard (2000-Patient Study)")
    if supabase:
        response = supabase.table("patient_research").select("*").execute()
        df = pd.DataFrame(response.data)
        st.dataframe(df)
        st.download_button("Export Full CSV for Analysis", df.to_csv(index=False).encode(), "2000_patient_research.csv")
        st.metric("Total Records", len(df))
        st.bar_chart(df["age"].value_counts())
    else:
        st.info("Connect Supabase for live research data.")

st.caption("Built with Streamlit • GitHub • Supabase • For research purposes only")
