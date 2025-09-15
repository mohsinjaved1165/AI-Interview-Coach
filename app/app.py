import streamlit as st
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Interview Coach", layout="centered")

# Visible heading
st.markdown(
    "<h1 style='text-align: center;'>🤖 AI Interview Coach</h1>",
    unsafe_allow_html=True
)
st.markdown("---")


# ---------- State Management ----------
if "stage" not in st.session_state:
    st.session_state.stage = "jd"
if "questions" not in st.session_state:
    st.session_state.questions = []
if "index" not in st.session_state:
    st.session_state.index = 0
if "responses" not in st.session_state:
    st.session_state.responses = []
if "final_report" not in st.session_state:
    st.session_state.final_report = ""


# ---------- Stage 1: Enter Job Description ----------
if st.session_state.stage == "jd":
    st.subheader("Step 1: Enter Job Description")
    jd = st.text_area("Paste the JD here:", key="jd_input")

    if st.button("Start Interview"):
        if jd.strip():
            try:
                res = requests.post(f"{API_URL}/start", json={"jd": jd}, timeout=90)
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.questions = data["questions"]
                    st.session_state.stage = "interview"
                    st.session_state.index = 0
                    st.session_state.responses = []
                    st.session_state.final_report = ""
                    st.rerun()
                else:
                    st.error(f"❌ Error fetching questions: {res.text}")
            except Exception as e:
                st.error(f"⚠️ Failed to fetch questions: {str(e)}")
        else:
            st.warning("Please enter a Job Description to continue.")


# ---------- Stage 2: Interview Questions ----------
elif st.session_state.stage == "interview":
    q = st.session_state.questions[st.session_state.index]
    st.subheader(f"Question {st.session_state.index + 1} of {len(st.session_state.questions)}")
    st.write(q)

    ans = st.text_area("Your Answer:", key=f"ans_{st.session_state.index}")

    if st.button("Submit Answer"):
        if ans.strip():
            try:
                # --- Streaming request ---
                with requests.post(
                    f"{API_URL}/api/answer",
                    json={"question": q, "answer": ans},
                    stream=True,
                    timeout=600
                ) as r:
                    r.raise_for_status()
                    feedback = ""
                    feedback_box = st.empty()
                    for chunk in r.iter_content(chunk_size=None):
                        if chunk:
                            text = chunk.decode("utf-8")
                            feedback += text
                            feedback_box.info(f"**Feedback (streaming):** {feedback}")

                # Save response
                st.session_state.responses.append({
                    "question": q,
                    "answer": ans,
                    "feedback": feedback
                })

                # Move to next or finish
                if st.session_state.index + 1 < len(st.session_state.questions):
                    st.session_state.index += 1
                    st.rerun()
                else:
                    st.session_state.stage = "summary"
                    st.rerun()

            except Exception as e:
                st.error(f"⚠️ Failed to send answer: {str(e)}")
        else:
            st.warning("Please type an answer before submitting.")


# ---------- Stage 3: Summary ----------
elif st.session_state.stage == "summary":
    st.subheader("📊 Interview Summary")

    # Show all responses
    for r in st.session_state.responses:
        st.markdown(f"**Q:** {r['question']}")
        st.markdown(f"**Your Answer:** {r['answer']}")
        st.markdown(f"**Feedback:** {r['feedback']}")
        st.write("---")

    if st.button("Generate Final Report"):
        try:
            # --- Streaming final report ---
            with requests.post(
                f"{API_URL}/api/report",
                json={"responses": st.session_state.responses},
                stream=True,
                timeout=600
            ) as r:
                r.raise_for_status()
                report = ""
                report_box = st.empty()
                for chunk in r.iter_content(chunk_size=None):
                    if chunk:
                        text = chunk.decode("utf-8")
                        report += text
                        report_box.write(report)

            st.session_state.final_report = report
            st.success("✅ Final Report Generated")

        except Exception as e:
            st.error(f"⚠️ Failed to generate report: {str(e)}")

    # PDF Download
    if st.session_state.final_report:
        def create_pdf():
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []

            elements.append(Paragraph("Interview Report", styles["Heading1"]))
            elements.append(Spacer(1, 12))

            for r in st.session_state.responses:
                elements.append(Paragraph(f"Q: {r['question']}", styles["Heading3"]))
                elements.append(Paragraph(f"Your Answer: {r['answer']}", styles["Normal"]))
                elements.append(Paragraph(f"Feedback: {r['feedback']}", styles["Italic"]))
                elements.append(Spacer(1, 12))

            elements.append(Paragraph("Final Summary", styles["Heading2"]))
            elements.append(Paragraph(st.session_state.final_report, styles["Normal"]))

            doc.build(elements)
            buffer.seek(0)
            return buffer

        pdf_buffer = create_pdf()
        st.download_button(
            label="📥 Download Report as PDF",
            data=pdf_buffer,
            file_name="interview_report.pdf",
            mime="application/pdf"
        )

    if st.button("🔄 Restart"):
        st.session_state.stage = "jd"
        st.session_state.questions = []
        st.session_state.index = 0
        st.session_state.responses = []
        st.session_state.final_report = ""
        st.rerun()
