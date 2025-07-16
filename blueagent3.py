import streamlit as st
import pandas as pd
import numpy as np
import requests
from io import BytesIO
import re
from urllib.parse import quote
import time

# Page configuration
st.set_page_config(
    page_title="Blue Agent",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Apple-inspired design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #007BFF 0%, #0056b3 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 20px rgba(0, 123, 255, 0.15);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    .input-section {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 2px 20px rgba(0, 0, 0, 0.06);
        margin-bottom: 2rem;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .applicant-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .applicant-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    
    .level-badge {
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    .level-high {
        background: #d4edda;
        color: #155724;
    }
    
    .level-mid {
        background: #fff3cd;
        color: #856404;
    }
    
    .level-low {
        background: #f8d7da;
        color: #721c24;
    }
    
    .action-buttons {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    
    .btn-email {
        background: #FF4757;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.2s ease;
        border: none;
        cursor: pointer;
        font-size: 0.9rem;
        box-shadow: 0 2px 10px rgba(255, 71, 87, 0.3);
    }
    
    .btn-email:hover {
        background: #ff3742;
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(255, 71, 87, 0.4);
        text-decoration: none;
        color: white;
    }
    
    .btn-teams {
        background: #007BFF;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.2s ease;
        border: none;
        cursor: pointer;
        font-size: 0.9rem;
        box-shadow: 0 2px 10px rgba(0, 123, 255, 0.3);
    }
    
    .btn-teams:hover {
        background: #0056b3;
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.4);
        text-decoration: none;
        color: white;
    }
    
    .stButton > button {
        background: #007BFF;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 10px rgba(0, 123, 255, 0.3);
    }
    
    .stButton > button:hover {
        background: #0056b3;
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.4);
    }
    
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e9ecef;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: border-color 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #007BFF;
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
    }
    
    .info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .info-item {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007BFF;
    }
    
    .info-item strong {
        color: #007BFF;
        font-weight: 600;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2px solid #f3f3f3;
        border-top: 2px solid #007BFF;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 0.5rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #007BFF;
        margin: 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

def calculate_bmi(weight, height):
    """Calculate BMI from weight (kg) and height (cm)"""
    try:
        weight = float(weight)
        height = float(height) / 100  # Convert cm to meters
        bmi = weight / (height ** 2)
        return round(bmi, 2)
    except:
        return None

def analyze_applicant_level(bmi, experience_years, education_level, skills):
    """Analyze applicant level based on BMI and other factors"""
    # BMI threshold check
    if bmi and bmi > 25:
        return "Low"
    
    # Rule-based scoring for other factors
    score = 0
    
    # Experience scoring
    if experience_years >= 5:
        score += 3
    elif experience_years >= 2:
        score += 2
    elif experience_years >= 1:
        score += 1
    
    # Education scoring
    education_scores = {
        'PhD': 3,
        'Masters': 2,
        'Bachelor': 1,
        'High School': 0
    }
    score += education_scores.get(education_level, 0)
    
    # Skills scoring (basic keyword matching)
    relevant_skills = ['python', 'java', 'sql', 'machine learning', 'data analysis', 'project management']
    skill_matches = sum(1 for skill in relevant_skills if skill.lower() in skills.lower())
    score += min(skill_matches, 3)  # Max 3 points for skills
    
    # Determine level based on total score
    if score >= 7:
        return "High"
    elif score >= 4:
        return "Mid"
    else:
        return "Low"

def create_mailto_link(email, name, level):
    """Create a mailto link for Outlook integration"""
    subject = f"Interview Opportunity - {name}"
    body = f"""Dear {name},

Thank you for your application. Based on our initial assessment, we would like to invite you for an interview.

Your application has been classified as: {level} Level

We will contact you shortly to schedule a convenient time for the interview.

Best regards,
Blue Agent HR Team"""
    
    mailto_link = f"mailto:{email}?subject={quote(subject)}&body={quote(body)}"
    return mailto_link

def create_teams_link(email, name):
    """Create a Teams meeting link"""
    # This would typically integrate with Microsoft Graph API
    # For demo purposes, we'll create a generic Teams link
    teams_link = "https://teams.microsoft.com/l/meetup-join/19%3ameeting_example"
    return teams_link

def process_excel_data(excel_url):
    """Process Excel data from OneDrive/SharePoint link"""
    try:
        # Convert OneDrive/SharePoint sharing link to direct download link
        if 'sharepoint.com' in excel_url or 'onedrive.com' in excel_url:
            # Extract file ID and create direct download link
            if '?id=' in excel_url:
                file_id = excel_url.split('?id=')[1].split('&')[0]
                download_url = excel_url.replace('?id=', '?download=1&id=')
            else:
                download_url = excel_url.replace('?', '?download=1&')
        else:
            download_url = excel_url
        
        # Read Excel file
        response = requests.get(download_url)
        response.raise_for_status()
        
        # Load into pandas
        df = pd.read_excel(BytesIO(response.content))
        
        return df, None
    except Exception as e:
        return None, str(e)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔵 Blue Agent</h1>
        <p>AI-Powered Applicant Analysis & Management System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("### 📊 Excel Data Input")
    
    excel_url = st.text_input(
        "Paste your Microsoft Excel Online (OneDrive/SharePoint) link:",
        placeholder="https://yourcompany.sharepoint.com/sites/hr/Shared%20Documents/applicants.xlsx",
        help="Make sure the Excel file is shared with view permissions"
    )
    
    col1, col2 = st.columns([2, 1])
    with col1:
        analyze_button = st.button("🔍 Fetch & Analyze", type="primary")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'applicants_data' not in st.session_state:
        st.session_state.applicants_data = None
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    
    # Process data when button is clicked
    if analyze_button and excel_url:
        with st.spinner("Fetching and analyzing data..."):
            # For demo purposes, we'll create sample data if URL processing fails
            df, error = process_excel_data(excel_url)
            
            if df is None:
                st.markdown(f'<div class="error-message">⚠️ Could not fetch data from URL: {error}</div>', unsafe_allow_html=True)
                st.markdown('<div class="error-message">📝 Using sample data for demonstration...</div>', unsafe_allow_html=True)
                
                # Create sample data
                sample_data = {
                    'Name': ['John Smith', 'Sarah Johnson', 'Mike Chen', 'Emily Davis', 'Robert Wilson'],
                    'Email': ['john.smith@email.com', 'sarah.johnson@email.com', 'mike.chen@email.com', 'emily.davis@email.com', 'robert.wilson@email.com'],
                    'Weight_kg': [70, 65, 85, 60, 95],
                    'Height_cm': [175, 160, 180, 165, 170],
                    'Experience_Years': [3, 5, 2, 7, 1],
                    'Education': ['Bachelor', 'Masters', 'Bachelor', 'PhD', 'High School'],
                    'Skills': ['Python, SQL, Data Analysis', 'Java, Project Management, Leadership', 'Python, Machine Learning', 'Research, Statistics, Python', 'Basic Computer Skills']
                }
                df = pd.DataFrame(sample_data)
            
            # Process each applicant
            applicants = []
            for _, row in df.iterrows():
                bmi = calculate_bmi(row['Weight_kg'], row['Height_cm'])
                level = analyze_applicant_level(
                    bmi, 
                    row['Experience_Years'], 
                    row['Education'], 
                    row['Skills']
                )
                
                applicant = {
                    'name': row['Name'],
                    'email': row['Email'],
                    'weight': row['Weight_kg'],
                    'height': row['Height_cm'],
                    'bmi': bmi,
                    'experience': row['Experience_Years'],
                    'education': row['Education'],
                    'skills': row['Skills'],
                    'level': level
                }
                applicants.append(applicant)
            
            st.session_state.applicants_data = applicants
            st.session_state.analysis_complete = True
            
            time.sleep(1)  # Brief pause for UX
    
    # Display results
    if st.session_state.analysis_complete and st.session_state.applicants_data:
        st.markdown('<div class="success-message">✅ Analysis completed successfully!</div>', unsafe_allow_html=True)
        
        # Statistics
        total_applicants = len(st.session_state.applicants_data)
        high_level = sum(1 for a in st.session_state.applicants_data if a['level'] == 'High')
        mid_level = sum(1 for a in st.session_state.applicants_data if a['level'] == 'Mid')
        low_level = sum(1 for a in st.session_state.applicants_data if a['level'] == 'Low')
        
        st.markdown(f"""
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-number">{total_applicants}</div>
                <div class="stat-label">Total Applicants</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{high_level}</div>
                <div class="stat-label">High Level</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{mid_level}</div>
                <div class="stat-label">Mid Level</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{low_level}</div>
                <div class="stat-label">Low Level</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display applicants
        st.markdown("### 👥 Applicant Analysis Results")
        
        for applicant in st.session_state.applicants_data:
            level_class = f"level-{applicant['level'].lower()}"
            
            mailto_link = create_mailto_link(applicant['email'], applicant['name'], applicant['level'])
            teams_link = create_teams_link(applicant['email'], applicant['name'])
            
            st.markdown(f"""
            <div class="applicant-card">
                <h3 style="margin: 0 0 1rem 0; color: #007BFF;">{applicant['name']}</h3>
                <div class="level-badge {level_class}">
                    {applicant['level']} Level
                </div>
                
                <div class="info-grid">
                    <div class="info-item">
                        <strong>Email:</strong><br>{applicant['email']}
                    </div>
                    <div class="info-item">
                        <strong>BMI:</strong><br>{applicant['bmi']} {'(⚠️ >25)' if applicant['bmi'] and applicant['bmi'] > 25 else '(✅ ≤25)'}
                    </div>
                    <div class="info-item">
                        <strong>Experience:</strong><br>{applicant['experience']} years
                    </div>
                    <div class="info-item">
                        <strong>Education:</strong><br>{applicant['education']}
                    </div>
                </div>
                
                <div style="margin: 1rem 0;">
                    <strong>Skills:</strong> {applicant['skills']}
                </div>
                
                <div class="action-buttons">
                    <a href="{mailto_link}" class="btn-email" target="_blank">
                        📧 Send Email via Outlook
                    </a>
                    <a href="{teams_link}" class="btn-teams" target="_blank">
                        📹 Schedule Teams Interview
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 2rem 0;">
        <p>🔵 Blue Agent - Powered by AI | Built with Streamlit</p>
        <p style="font-size: 0.9rem;">Deploy on Streamlit Cloud for optimal performance</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()