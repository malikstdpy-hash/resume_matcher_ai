# 🔍 AI Resume & Job Matcher

An AI-powered tool that matches resumes against job descriptions using the Groq LLaMA 3.1 API, helping job seekers quickly see how well their resume aligns with a given role.

## ✨ Features
- 📄 Parses resume content from uploaded files
- 🤖 Uses the Groq LLaMA 3.1 API to analyze resume-to-job fit
- 💾 Stores match history in a local SQLite database
- 📊 Returns a match score with feedback on strengths and gaps

## 🛠️ Tech Stack
- **Language:** Python
- **AI/LLM:** Groq LLaMA 3.1 API
- **Database:** SQLite3

## 📂 Project Structure
```
resume_matcher_ai/
├── app.py            # Main application entry point
├── matcher.py         # Resume-to-job matching logic (Groq LLaMA 3.1)
├── database.py        # SQLite database handling
├── test.py             # Tests
└── requirements.txt   # Python dependencies
```

## 🚀 Getting Started

```bash
echo ".idea/" >> .gitignore
echo "*.db" >> .gitignore
git rm -r --cached .idea resume_matcher.db
git add .gitignore
git commit -m "Clean up: remove IDE config and db file from tracking"
git push

# Set your Groq API key
export GROQ_API_KEY=your_api_key_here   # Windows: set GROQ_API_KEY=your_api_key_here

# Run the app
 streamlit run app.py
```

## 📈 Future Improvements
- [ ] Support more file formats (PDF, DOCX)
- [ ] Web UI polish
- [ ] Batch resume processing

## 📫 Contact
Built by Abdul Malik — malikstdpy@gmail.com
