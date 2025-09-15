from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict
import json

# Import Ollama LLM
try:
    from langchain_ollama import OllamaLLM
    llm = OllamaLLM(model="llama3")
except ImportError:
    from langchain_community.llms import Ollama
    llm = Ollama(model="llama3")

app = FastAPI()


# ------------------------
# Data Models
# ------------------------
class JDRequest(BaseModel):
    jd: str

class AnswerRequest(BaseModel):
    question: str
    answer: str

class ReportRequest(BaseModel):
    responses: List[Dict[str, str]]


# ------------------------
# Warmup on Startup
# ------------------------
@app.on_event("startup")
async def warmup_model():
    print("⚡ Warming up model...")
    try:
        _ = llm.invoke("Hello, just warming up the model.")
        print("✅ Model warmed up")
    except Exception as e:
        print(f"❌ Warmup failed: {e}")


# ------------------------
# Generate Interview Questions
# ------------------------
@app.post("/start")
async def start_interview(req: JDRequest):
    prompt = f"""
    Based on this job description, generate 5 short and clear interview questions.
    Job Description: {req.jd}
    Return only the questions in a numbered list, no explanations.
    """

    result = llm.invoke(prompt)
    questions = [q.strip("12345). ") for q in result.split("\n") if q.strip()]

    return {"questions": questions[:5]}


# ------------------------
# Stream Feedback
# ------------------------
@app.post("/api/answer")
async def answer_question(req: AnswerRequest):
    prompt = f"""
    Interview Question: {req.question}
    Candidate Answer: {req.answer}

    Provide constructive feedback on the answer in 3-4 sentences.
    """

    def generate():
        try:
            for chunk in llm.stream(prompt):
                if chunk:
                    yield chunk
        except Exception as e:
            yield f"\n[Error: {str(e)}]"

    return StreamingResponse(generate(), media_type="text/plain")


# ------------------------
# Stream Final Report
# ------------------------
@app.post("/api/report")
async def generate_report(req: ReportRequest):
    responses_json = json.dumps(req.responses, indent=2)

    prompt = f"""
    Here are the candidate's interview responses with feedback:
    {responses_json}

    Write a final interview summary highlighting strengths, weaknesses, and overall performance.
    """

    def generate():
        try:
            for chunk in llm.stream(prompt):
                if chunk:
                    yield chunk
        except Exception as e:
            yield f"\n[Error: {str(e)}]"

    return StreamingResponse(generate(), media_type="text/plain")
