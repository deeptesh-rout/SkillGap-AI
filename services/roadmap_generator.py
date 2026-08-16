import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


load_dotenv()


def get_hf_client():

    token = os.getenv("HF_TOKEN")

    if not token:
        return None

    return InferenceClient(
        api_key=token
    )


def generate_fallback_roadmap(
    role,
    missing_skills
):

    if not missing_skills:

        return (
            "## 🎉 You are already well prepared!\n\n"
            "You currently have the major skills required "
            f"for the **{role}** role.\n\n"
            "Focus on:\n"
            "- Building production projects\n"
            "- Improving problem solving\n"
            "- Preparing for interviews\n"
            "- Strengthening system design"
        )


    roadmap = (
        f"# 🗺️ {role} Learning Roadmap\n\n"
    )

    roadmap += (
        "Based on your current skill profile, "
        "focus on the following areas:\n\n"
    )

    for index, skill in enumerate(
        missing_skills,
        start=1
    ):

        roadmap += (
            f"## {index}. {skill}\n\n"
            f"- Learn the fundamentals of {skill}\n"
            f"- Practice practical problems\n"
            f"- Build a small project using {skill}\n"
            f"- Add the project to your portfolio\n\n"
        )

    roadmap += (
        "## 🚀 Final Step\n\n"
        "Build one capstone project combining "
        "multiple missing skills."
    )

    return roadmap


def generate_roadmap(
    role,
    current_skills,
    missing_skills
):

    client = get_hf_client()

    if client is None:

        return generate_fallback_roadmap(
            role,
            missing_skills
        )


    current_skill_names = []

    for skill in current_skills:

        if isinstance(skill, dict):

            current_skill_names.append(
                skill["name"]
            )

        else:

            current_skill_names.append(
                skill
            )


    prompt = f"""
You are an expert career mentor.

Create a practical learning roadmap for:

Target role:
{role}

Current skills:
{", ".join(current_skill_names)}

Missing skills:
{", ".join(missing_skills)}

Create a structured 90-day roadmap.

Include:

1. Fundamentals
2. Practical exercises
3. Projects
4. Portfolio development
5. Interview preparation

Keep the roadmap realistic for a student.

Return Markdown only.
"""


    try:

        response = client.chat_completion(
            model="HuggingFaceH4/zephyr-7b-beta",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1200
        )

        return response.choices[
            0
        ].message.content

    except Exception as error:

        print(
            f"Hugging Face error: {error}"
        )

        return generate_fallback_roadmap(
            role,
            missing_skills
        )