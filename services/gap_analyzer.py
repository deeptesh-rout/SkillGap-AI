def analyze_skill_gap(
    user_skills,
    required_skills
):
    """
    Compare user skills with role requirements.

    required_skills format:

    {
        "Python": 0.7,
        "Java": 0.8,
        "DSA": 1.0
    }
    """

    user_skill_names = {}

    for skill in user_skills:

        if isinstance(skill, dict):

            name = skill["name"]

            confidence = skill.get(
                "confidence",
                1.0
            )

            user_skill_names[
                name.lower()
            ] = confidence

        else:

            user_skill_names[
                skill.lower()
            ] = 1.0


    details = []

    missing_skills = []

    strong_skills = []


    for skill, required_level in required_skills.items():

        current_level = user_skill_names.get(
            skill.lower(),
            0.0
        )

        gap = max(
            required_level - current_level,
            0.0
        )

        item = {
            "skill": skill,
            "required": required_level,
            "current": current_level,
            "gap": gap
        }

        details.append(item)

        if gap > 0:

            missing_skills.append(skill)

        else:

            strong_skills.append(skill)


    details.sort(
        key=lambda item: item["gap"],
        reverse=True
    )


    return {
        "details": details,
        "missing_skills": missing_skills,
        "strong_skills": strong_skills
    }