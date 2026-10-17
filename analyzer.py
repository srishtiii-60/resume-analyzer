"""Core logic: PDF text extraction, skill matching and scoring."""

import re
from typing import Dict, List, Set

from pypdf import PdfReader

from skills import SKILL_ALIASES

try:  # scikit-learn is used for text similarity (optional but recommended)
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    SKLEARN_AVAILABLE = True
except ImportError:  # pragma: no cover
    SKLEARN_AVAILABLE = False

SKILL_WEIGHT = 0.7       # weight of skill match in the final score
SIMILARITY_WEIGHT = 0.3  # weight of overall text similarity


def extract_text(pdf_file) -> str:
    """Extract text from a PDF (path or file-like object)."""
    reader = PdfReader(pdf_file)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def _alias_pattern(alias: str) -> re.Pattern:
    # Lookarounds instead of \b so that c++, c#, node.js work properly.
    return re.compile(r"(?<![a-z0-9+#])" + re.escape(alias) + r"(?![a-z0-9+#])")


_PATTERNS = {
    skill: [_alias_pattern(alias) for alias in aliases]
    for skill, aliases in SKILL_ALIASES.items()
}


def find_skills(text: str) -> Set[str]:
    """Return the set of canonical skills found in the text."""
    text = _normalize(text)
    return {
        skill
        for skill, patterns in _PATTERNS.items()
        if any(p.search(text) for p in patterns)
    }


def text_similarity(resume_text: str, jd_text: str) -> float:
    """TF-IDF cosine similarity between resume and JD (0.0 to 1.0)."""
    if not SKLEARN_AVAILABLE or not resume_text.strip() or not jd_text.strip():
        return 0.0
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        matrix = vectorizer.fit_transform([resume_text, jd_text])
    except ValueError:  # empty vocabulary
        return 0.0
    return float(cosine_similarity(matrix[0], matrix[1])[0][0])


def build_suggestions(missing: List[str]) -> List[str]:
    tips = []
    for skill in missing[:5]:
        tips.append(
            f"Add a project or experience line that shows '{skill}' "
            f"(only if you genuinely have it)."
        )
    if missing:
        tips.append("Mirror the job description's keywords naturally in your summary.")
    return tips


def analyze(resume_text: str, jd_text: str) -> Dict:
    """Compare a resume with a job description."""
    resume_skills = find_skills(resume_text)
    jd_skills = find_skills(jd_text)

    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)
    extra = sorted(resume_skills - jd_skills)

    skill_score = (len(matched) / len(jd_skills) * 100) if jd_skills else 0.0
    similarity = text_similarity(resume_text, jd_text) * 100

    if jd_skills:
        overall = SKILL_WEIGHT * skill_score + SIMILARITY_WEIGHT * similarity
    else:
        overall = similarity

    return {
        "score": round(overall),
        "skill_score": round(skill_score),
        "similarity": round(similarity),
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "suggestions": build_suggestions(missing),
    }
