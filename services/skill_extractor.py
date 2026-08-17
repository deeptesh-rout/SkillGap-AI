import re


def normalize_text(text):
    """
    Normalize text for easier matching.
    """

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


def extract_skills(resume_text, skills_data):
    """
    Extract skills from resume text using
    the controlled skills vocabulary.

    Returns:
        List of dictionaries
    """

    normalized_resume = normalize_text(resume_text)

    detected_skills = []

    for category, skills in skills_data.items():

        for skill in skills:

            normalized_skill = normalize_text(
                skill
            )

            pattern = r"\b" + re.escape(
                normalized_skill
            ) + r"\b"

            if re.search(pattern,normalized_resume):

                detected_skills.append(
                    {
                        "name": skill,
                        "category": category,
                        "confidence": 1.0
                    }
                )

    return detected_skills