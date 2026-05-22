import streamlit as st
import pdfplumber
import pandas as pd
from database import create_tables, save_resume, save_job, save_match, get_all_matches
from matcher import match_resume_to_job

create_tables()

st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Resume & Job Matcher")
st.markdown("Upload a resume and paste a job description to get an AI match score!")

tab1, tab2 = st.tabs(["🔍 Match Resume", "📊 Match History"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Resume")
        candidate_name = st.text_input("Candidate Name", placeholder="e.g. John Doe")
        upload_option = st.radio("Input Method", ["Upload PDF", "Paste Text"])

        resume_text = ""

        if upload_option == "Upload PDF":
            pdf_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
            if pdf_file:
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:
                        resume_text += page.extract_text() or ""
                st.success("PDF loaded ✅")
                st.text_area("Preview", resume_text[:500] + "...", height=150)
        else:
            resume_text = st.text_area("Paste Resume Text Here", height=250)

    with col2:
        st.subheader("💼 Job Description")
        job_title = st.text_input("Job Title", placeholder="e.g. Python Developer")
        job_description = st.text_area("Paste Job Description Here", height=300)

    st.divider()

    if st.button("🚀 Analyze Match", use_container_width=True):
        if not candidate_name:
            st.error("Please enter candidate name!")
        elif not resume_text:
            st.error("Please provide a resume!")
        elif not job_title:
            st.error("Please enter job title!")
        elif not job_description:
            st.error("Please provide a job description!")
        else:
            with st.spinner("AI is analyzing... please wait ⏳"):
                result = match_resume_to_job(resume_text, job_description)
                resume_id = save_resume(candidate_name, resume_text)
                job_id = save_job(job_title, job_description)
                save_match(resume_id, job_id, result["score"], result["feedback"])

            st.success("✅ Analysis Complete!")
            st.divider()

            score = result["score"]
            col_a, col_b, col_c = st.columns(3)

            with col_a:
                st.metric("Match Score", f"{score}/100")
            with col_b:
                if score >= 75:
                    st.success(f"✅ {result['recommendation']}")
                elif score >= 50:
                    st.warning(f"⚠️ {result['recommendation']}")
                else:
                    st.error(f"❌ {result['recommendation']}")
            with col_c:
                st.progress(score / 100)

            st.divider()

            col_x, col_y = st.columns(2)
            with col_x:
                st.subheader("✅ Matching Skills")
                st.write(result["matching_skills"])
            with col_y:
                st.subheader("❌ Missing Skills")
                st.write(result["missing_skills"])

            st.subheader("📝 AI Feedback")
            st.info(result["feedback"])

with tab2:
    st.subheader("📊 All Past Matches")
    matches = get_all_matches()

    if not matches:
        st.info("No matches yet. Go to Match tab first!")
    else:
        df = pd.DataFrame(matches, columns=[
            "ID", "Candidate", "Job Title", "Score", "Feedback", "Date"
        ])
        st.dataframe(df, use_container_width=True)