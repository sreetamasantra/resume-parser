import streamlit as st
import json
import os
from src.extractor import extract_text
from src.parser import parse_resume

# ─── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="Resume Parser",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Resume Parser")
st.markdown("Upload a resume in **PDF or DOCX** format to extract structured information.")

# ─── File Upload ───────────────────────────────────────────
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    temp_path = f"data/sample_resumes/temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Parsing resume..."):
        try:
            text = extract_text(temp_path)
            result = parse_resume(text)

            # ─── Display Results ───────────────────────────
            st.success("Resume parsed successfully!")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("👤 Personal Info")
                st.write(f"**Name:** {result['name']}")
                st.write(f"**Email:** {result['email']}")
                st.write(f"**Phone:** {result['phone']}")
                st.write(f"**LinkedIn:** {result['linkedin']}")
                st.write(f"**GitHub:** {result['github']}")

            with col2:
                st.subheader("🛠️ Skills")
                if result['skills']:
                    for skill in result['skills']:
                        st.markdown(f"- {skill}")
                else:
                    st.write("No skills found.")

            st.subheader("🎓 Education")
            st.write(result['education'])

            st.subheader("💼 Experience")
            st.write(result['experience'])

            # ─── JSON Download ─────────────────────────────
            st.subheader("⬇️ Download Parsed JSON")
            json_str = json.dumps(result, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"{result['name'].replace(' ', '_')}_parsed.json",
                mime="application/json"
            )

            # ─── Raw JSON Preview ──────────────────────────
            with st.expander("View Raw JSON"):
                st.json(result)

        except Exception as e:
            st.error(f"Error parsing resume: {str(e)}")

        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)