import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def match_resume_to_job(resume_text, job_description):
    prompt = f"""
You are an expert HR recruiter and resume analyst.

Analyze the following resume against the job description and provide:

1. A MATCH SCORE from 0 to 100
2. MATCHING SKILLS
3. MISSING SKILLS
4. OVERALL FEEDBACK
5. RECOMMENDATION (Strongly Recommended / Recommended / Maybe / Not Recommended)

Respond in this EXACT format:
SCORE: [number only]
MATCHING SKILLS: [list]
MISSING SKILLS: [list]
FEEDBACK: [text]
RECOMMENDATION: [text]

--- RESUME ---
{resume_text}

--- JOB DESCRIPTION ---
{job_description}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content
    return parse_result(result)

def parse_result(text):
    data = {
        "score": 0,
        "matching_skills": "N/A",
        "missing_skills": "N/A",
        "feedback": "N/A",
        "recommendation": "N/A"
    }

    for line in text.split("\n"):
        if line.startswith("SCORE:"):
            try:
                data["score"] = int(line.replace("SCORE:", "").strip())
            except:
                data["score"] = 0
        elif line.startswith("MATCHING SKILLS:"):
            data["matching_skills"] = line.replace("MATCHING SKILLS:", "").strip()
        elif line.startswith("MISSING SKILLS:"):
            data["missing_skills"] = line.replace("MISSING SKILLS:", "").strip()
        elif line.startswith("FEEDBACK:"):
            data["feedback"] = line.replace("FEEDBACK:", "").strip()
        elif line.startswith("RECOMMENDATION:"):
            data["recommendation"] = line.replace("RECOMMENDATION:", "").strip()

    return data