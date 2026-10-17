"""Streamlit UI for the AI Resume Analyzer."""

import streamlit as st

from analyzer import analyze, extract_text

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")

st.title("📄 AI Resume Analyzer")
st.caption("Upload your resume, paste a job description, and see how well they match.")

resume_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
jd_text = st.text_area("Paste the job description", height=220)

if st.button("Analyze", type="primary"):
    if not resume_file or not jd_text.strip():
        st.error("Please upload a resume and paste a job description.")
        st.stop()

    try:
        resume_text = extract_text(resume_file)
    except Exception:
        st.error("Could not read this PDF. Please upload a valid, text-based PDF.")
        st.stop()

    if not resume_text:
        st.error("No text found. Scanned/image PDFs are not supported yet.")
        st.stop()

    result = analyze(resume_text, jd_text)

    st.subheader("Result")
    c1, c2, c3 = st.columns(3)
    c1.metric("Overall match", f"{result['score']}%")
    c2.metric("Skill match", f"{result['skill_score']}%")
    c3.metric("Text similarity", f"{result['similarity']}%")
    st.progress(min(result["score"], 100) / 100)

    left, right = st.columns(2)
    with left:
        st.markdown("**✅ Matched skills**")
        st.write(", ".join(result["matched"]) or "None found")
    with right:
        st.markdown("**❌ Missing skills**")
        st.write(", ".join(result["missing"]) or "Nothing missing 🎉")

    if result["extra"]:
        st.markdown("**➕ Other skills found in your resume**")
        st.write(", ".join(result["extra"]))

    if result["suggestions"]:
        st.markdown("**💡 Suggestions**")
        for tip in result["suggestions"]:
            st.write("- " + tip)
