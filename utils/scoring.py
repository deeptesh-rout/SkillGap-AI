def calculate_readiness_score(
    user_skills,
    required_skills
):
    """
    Calculate job readiness from 0 to 100.
    """

    user_skill_levels = {}

    for skill in user_skills:

        if isinstance(skill, dict):

            name = skill["name"]

            confidence = skill.get(
                "confidence",
                1.0
            )

            user_skill_levels[
                name.lower()
            ] = confidence

        else:

            user_skill_levels[
                skill.lower()
            ] = 1.0


    total_required = 0.0
    total_current = 0.0


    for skill, required_level in required_skills.items():

        current_level = user_skill_levels.get(
            skill.lower(),
            0.0
        )

        total_required += required_level

        total_current += min(
            current_level,
            required_level
        )


    if total_required == 0:

        return 0


    score = (
        total_current
        / total_required
    ) * 100


    return round(
        min(score, 100),
        2
    )