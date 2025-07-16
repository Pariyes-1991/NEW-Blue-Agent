import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Blue Agent", page_icon="💼", layout="wide")

st.markdown("""
    <h1 style='text-align: center; color: #007BFF;'>Blue Agent</h1>
    <p style='text-align: center;'>Modern Applicant Analyzer with AI-based Scoring</p>
""", unsafe_allow_html=True)

st.divider()

excel_link = st.text_input("🔗 Paste your Microsoft Excel Online Link:")

if st.button("Fetch & Analyze"):
    try:
        df = pd.read_excel(excel_link)
        st.success("Data fetched successfully! Showing preview:")
        st.dataframe(df)

        def analyze_with_ai(text):
            try:
                api_url = "https://api-inference.huggingface.co/models/distilbert-base-uncased"
                headers = {"Authorization": "Bearer hf_your_token_here"}
                payload = {"inputs": text}
                response = requests.post(api_url, headers=headers, json=payload)
                if response.status_code == 200:
                    return "AI evaluated the input as acceptable"
                else:
                    return "AI could not evaluate the input"
            except:
                return "AI error occurred"

        def calculate_bmi(row):
            try:
                bmi = row['น้ำหนัก'] / ((row['ส่วนสูง'] / 100) ** 2)
                return round(bmi, 2)
            except:
                return None

        def assign_info_level(bmi):
            if bmi is None:
                return "Unknown", "BMI data is missing"
            elif bmi > 25:
                return "Low", "BMI exceeds 25"
            else:
                return "High", "BMI within healthy range"

        def assign_exp_level(exp_years, description):
            if exp_years >= 5:
                return "High", "Experience over 5 years"
            elif exp_years >= 2:
                return "Mid", "Experience between 2 and 5 years"
            else:
                ai_result = analyze_with_ai(description)
                return ai_result, f"AI evaluated description: {ai_result}"

        df['BMI'] = df.apply(calculate_bmi, axis=1)
        df[['Info Level', 'Info Reason']] = df['BMI'].apply(lambda bmi: pd.Series(assign_info_level(bmi)))
        df[['Exp Level', 'Exp Reason']] = df.apply(lambda row: pd.Series(assign_exp_level(row['ประสบการณ์ (ปี)'], row.get('รายละเอียดเพิ่มเติม', ''))), axis=1)

        st.subheader("🎯 Analyzed Results")
        for idx, row in df.iterrows():
            st.markdown(f"""
                <div style='border:1px solid #ccc; border-radius:10px; padding:10px; margin-bottom:10px;'>
                    <h4 style='color:#007BFF;'>{row['ชื่อ']}</h4>
                    <ul>
                        <li>BMI: <b>{row['BMI']}</b></li>
                        <li>Info Level: <b>{row['Info Level']}</b> - {row['Info Reason']}</li>
                        <li>Experience Level: <b>{row['Exp Level']}</b> - {row['Exp Reason']}</li>
                    </ul>
                    <a href="mailto:?subject=Applicant: {row['ชื่อ']}&body=Please review this applicant." target="_blank">
                        <button style='background:#007BFF; color:white; padding:5px 10px; border:none; border-radius:5px;'>📧 Send Email</button>
                    </a>
                    <a href="https://teams.microsoft.com/l/meeting/new" target="_blank">
                        <button style='background:red; color:white; padding:5px 10px; border:none; border-radius:5px; margin-left:10px;'>📅 Schedule Interview</button>
                    </a>
                </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❗ Error loading data: {e}")
