# 📄 AI Resume Analyzer

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![License](https://img.shields.io/badge/License-MIT-green)

A web app that compares your **resume (PDF)** with a **job description** and shows
your match score, matched skills, missing skills and improvement tips.

## Why I built this
Many resumes get rejected because they don't match the keywords of a job description.
This tool helps students quickly see which skills they should highlight or learn.

## Features
- Upload resume as PDF and paste any job description
- Skill extraction with synonym handling (`js` = `javascript`, `sklearn` = `scikit-learn`)
- Overall score = 70% skill match + 30% TF-IDF text similarity
- Matched, missing and extra skills
- Simple improvement suggestions
- Unit tests and GitHub Actions CI

## Tech Stack
Python, Streamlit, pypdf, scikit-learn, pytest

## Project Structure
```
resume-analyzer/
├── app.py            # Streamlit UI
├── analyzer.py       # extraction, matching, scoring
├── skills.py         # skills and aliases dictionary
├── tests/            # unit tests
├── docs/             # screenshots
└── .github/workflows # CI (runs tests on every push)
```

## Run Locally
```bash
git clone https://github.com/srishtiii-60/resume-analyzer.git
cd resume-analyzer
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
streamlit run app.py
```

## Run Tests
```bash
pytest
```

## How the score works
1. Skills are detected in both resume and job description using a skills dictionary.
2. `skill score = matched skills / skills required in JD`
3. `similarity = cosine similarity of TF-IDF vectors`
4. `overall = 0.7 * skill score + 0.3 * similarity`

## Live Demo
Add your Streamlit Cloud link here after deployment.

## Screenshots
Add screenshots in the `docs/` folder and link them here:
`![App](docs/screenshot.png)`

## Limitations
- Works only with text-based PDFs (scanned PDFs are not supported)
- Skills are limited to the dictionary in `skills.py`

## Future Improvements
- [ ] Hindi resume support
- [ ] AI suggestions using the Gemini API
- [ ] DOCX resume support
- [ ] Export report as PDF

## Author
**Srishti** — [GitHub](https://github.com/srishtiii-60)

## License
MIT
