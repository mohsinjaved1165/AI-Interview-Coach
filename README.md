🤖 **AI Interview Coach**

AI Interview Coach is an interactive tool that helps candidates practice technical interviews.
It asks tailored interview questions based on a job description, collects candidate answers, gives real-time feedback, and finally generates a comprehensive interview report highlighting strengths, weaknesses, and recommendations.

📌 **Problem Statement**

Preparing for interviews can be stressful:

Candidates don’t know what kind of questions to expect.

They rarely receive constructive feedback on their answers.

Practicing alone makes it hard to evaluate performance.

💡 **Solution**

AI Interview Coach provides:

Custom interview questions generated from a given job description.

Step-by-step practice (questions → answers → feedback).

Real-time feedback streaming (no long waiting).

Final summary report covering strengths, weaknesses, and overall performance.

Simple Streamlit UI that feels like a real mock interview session.

🛠️ **Tech Stack**

Backend: FastAPI

Frontend: Streamlit

LLM Integration: Ollama
 with LangChain

Language: Python 3.11

Deployment Ready: Works locally with uvicorn + streamlit

🔄 **Workflow**

User enters a job description.

Backend generates interview questions using an LLM.

User answers each question in the Streamlit UI.

Backend streams feedback for each answer.

Once all questions are answered, a final report is generated.

Candidate can review full performance analysis.

🚀 **Getting Started**
1. Clone Repository
git clone https://github.com/mohsinjaved1165/AI-Interview-Coach.git
cd ai-interview-coach

2. Setup Virtual Environments

You can either use one shared venv (simpler) or two separate venvs (backend + frontend).

🖥️ Option A: Single venv for both
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

pip install -r api/requirements_api.txt
pip install -r app/requirements_app.txt


Then run backend + frontend from same terminal (in two tabs).

🖥️ Option B: Separate venvs (backend + frontend)
Backend (FastAPI)
cd api
python3 -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate        # Windows

pip install -r requirements.txt
uvicorn api:app --reload --port 8000

Frontend (Streamlit)
cd app
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
streamlit run app.py


Open 👉 http://localhost:8501

📂 **Project Structure**
ai-interview-coach/
├── api/
│   ├── api.py
│   └── requirements_api.txt   # Backend dependencies
│
├── app/
│   ├── app.py
│   └── requirements_app.txt   # Frontend dependencies
│
├── README.md

📖 **Usage**

Open the Streamlit app.

Step 1: Enter the job description.

Step 2: Answer the interview questions one by one.

Receive real-time feedback after each response.

After all questions, click Generate Final Report.

Review the comprehensive interview analysis.

🌟 **Example**

Job Description: “Senior QA Engineer with Selenium and Python expertise.”

Sample Question: “Can you describe the most complex Selenium automation project you’ve worked on?”

Feedback: “Good explanation of framework setup, but could elaborate on CI/CD integration.”

Final Report: “Candidate demonstrates strong automation skills, needs improvement in test strategy discussions.”

🤝 **Contributing**

Contributions are welcome! Feel free to fork, submit issues, or make pull requests.
