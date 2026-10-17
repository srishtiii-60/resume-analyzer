from analyzer import analyze, find_skills


def test_find_skills_basic():
    assert {"python", "sql"} <= find_skills("I know Python and SQL.")


def test_aliases_are_mapped():
    skills = find_skills("Worked with JS and ReactJS")
    assert "javascript" in skills
    assert "react" in skills


def test_special_characters():
    skills = find_skills("Projects in C++ and C#, backend on Node.js")
    assert {"c++", "c#", "node.js"} <= skills


def test_no_partial_word_match():
    # 'java' must not match inside 'javascript'
    assert "java" not in find_skills("Only javascript experience")


def test_analyze_matched_and_missing():
    resume = "Python, SQL, Git, Flask developer"
    jd = "Looking for Python, SQL, Docker and Flask skills"
    result = analyze(resume, jd)
    assert result["matched"] == ["flask", "python", "sql"]
    assert result["missing"] == ["docker"]
    assert 0 <= result["score"] <= 100


def test_analyze_empty_jd_skills():
    result = analyze("Python developer", "We want a team player")
    assert result["skill_score"] == 0
    assert 0 <= result["score"] <= 100
