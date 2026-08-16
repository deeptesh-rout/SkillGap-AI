import re


def normalize_text(text):

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


def analyze_job_description(
    job_description,
    skills_data
):
    """
    Extract skills from a job description.
    """

    normalized_jd = normalize_text(
        job_description
    )

    detected_skills = []

    for category, skills in skills_data.items():

        for skill in skills:

            normalized_skill = normalize_text(
                skill
            )

            pattern = (
                r"\b"
                + re.escape(normalized_skill)
                + r"\b"
            )

            if re.search(
                pattern,
                normalized_jd
            ):

                detected_skills.append(
                    skill
                )

    return {
        "skills": detected_skills
    }