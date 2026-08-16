import streamlit as st
import json

from services.resume_parser import extract_text_from_pdf
from services.skill_extractor import extract_skills
from services.gap_analyzer import analyze_skill_gap
from services.roadmap_generator import generate_roadmap
from services.jd_analyzer import analyze_job_description
from utils.scoring import calculate_readiness_score


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="SkillGap AI",
    page_icon="🎯",
    layout="wide"
)


# --------------------------------------------------
# Load data
# --------------------------------------------------

def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


skills_data = load_json("data/skills.json")
job_roles = load_json("data/job_roles.json")


# --------------------------------------------------
# Session state
# --------------------------------------------------

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []

if "job_skills" not in st.session_state:
    st.session_state.job_skills = {}

if "gap_result" not in st.session_state:
    st.session_state.gap_result = None

if "readiness_score" not in st.session_state:
    st.session_state.readiness_score = 0

if "roadmap" not in st.session_state:
    st.session_state.roadmap = ""


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🎯 SkillGap AI")
st.subheader("AI-powered career skill gap analyzer")

st.write(
    "Upload your resume, select your target role, "
    "and discover what skills you need to become job-ready."
)

st.divider()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("🎯 SkillGap AI")

    st.write(
        "Analyze your current skills against "
        "your desired career role."
    )

    st.divider()

    st.info(
        "MVP Features:\n\n"
        "• Resume parsing\n"
        "• Skill extraction\n"
        "• Skill gap analysis\n"
        "• Job readiness score\n"
        "• Learning roadmap\n"
        "• Job description analysis"
    )


# --------------------------------------------------
# Main inputs
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("📄 Resume")

    resume_file = st.file_uploader(
        "Upload your resume",
        type=["pdf"]
    )


with col2:

    st.subheader("💼 Target Role")

    role = st.selectbox(
        "Select your target role",
        list(job_roles.keys())
    )


# --------------------------------------------------
# Analyze resume
# --------------------------------------------------

if st.button(
    "🚀 Analyze My Skills",
    use_container_width=True
):

    if resume_file is None:

        st.error("Please upload your resume first.")

    else:

        with st.spinner("Reading your resume..."):

            resume_text = extract_text_from_pdf(resume_file)

        if not resume_text.strip():

            st.error(
                "Could not extract text from this PDF."
            )

        else:

            st.session_state.resume_text = resume_text

            with st.spinner("Extracting your skills..."):

                detected_skills = extract_skills(
                    resume_text,
                    skills_data
                )

            st.session_state.resume_skills = detected_skills

            required_skills = job_roles[role]["skills"]

            gap_result = analyze_skill_gap(
                detected_skills,
                required_skills
            )

            st.session_state.gap_result = gap_result

            readiness = calculate_readiness_score(
                detected_skills,
                required_skills
            )

            st.session_state.readiness_score = readiness

            with st.spinner(
                "Generating your personalized roadmap..."
            ):

                roadmap = generate_roadmap(
                    role,
                    detected_skills,
                    gap_result["missing_skills"]
                )

            st.session_state.roadmap = roadmap

            st.success("Analysis completed successfully!")


# --------------------------------------------------
# Results
# --------------------------------------------------

if st.session_state.resume_skills:

    st.divider()

    st.header("📊 Your Skill Analysis")

    # ----------------------------------------------
    # Readiness
    # ----------------------------------------------

    score = st.session_state.readiness_score

    score_col1, score_col2, score_col3 = st.columns(3)

    with score_col1:

        st.metric(
            "Job Readiness",
            f"{score}%"
        )

    with score_col2:

        st.metric(
            "Skills Detected",
            len(st.session_state.resume_skills)
        )

    with score_col3:

        missing_count = len(
            st.session_state.gap_result["missing_skills"]
        )

        st.metric(
            "Skills to Learn",
            missing_count
        )

    st.progress(score / 100)

    st.divider()

    # ----------------------------------------------
    # Skills
    # ----------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("✅ Your Skills")

        for skill in st.session_state.resume_skills:

            if isinstance(skill, dict):

                name = skill.get("name", "Unknown")
                confidence = skill.get("confidence", 0)

                st.write(
                    f"**{name}** — "
                    f"{confidence * 100:.0f}% confidence"
                )

            else:

                st.write(f"✅ {skill}")

    with col2:

        st.subheader("❌ Skill Gaps")

        missing_skills = (
            st.session_state
            .gap_result["missing_skills"]
        )

        if missing_skills:

            for skill in missing_skills:

                st.write(f"🔴 {skill}")

        else:

            st.success(
                "You currently have all required skills!"
            )


    # ----------------------------------------------
    # Skill gap details
    # ----------------------------------------------

    st.divider()

    st.header("📈 Skill Gap Breakdown")

    gap_result = st.session_state.gap_result

    for item in gap_result["details"]:

        skill = item["skill"]
        required = item["required"]
        current = item["current"]
        gap = item["gap"]

        st.write(
            f"**{skill}**"
        )

        st.progress(min(current, 1.0))

        st.caption(
            f"Required: {required:.0%} | "
            f"Current: {current:.0%} | "
            f"Gap: {gap:.0%}"
        )


    # ----------------------------------------------
    # Roadmap
    # ----------------------------------------------

    st.divider()

    st.header("🗺️ Personalized Learning Roadmap")

    if st.session_state.roadmap:

        st.markdown(
            st.session_state.roadmap
        )

    # ----------------------------------------------
    # Job description
    # ----------------------------------------------

    st.divider()

    st.header("💼 Analyze a Job Description")

    job_description = st.text_area(
        "Paste a job description here",
        height=250
    )

    if st.button(
        "🔍 Analyze Job Description",
        use_container_width=True
    ):

        if not job_description.strip():

            st.warning(
                "Please paste a job description."
            )

        else:

            with st.spinner(
                "Analyzing job description..."
            ):

                jd_result = analyze_job_description(
                    job_description,
                    skills_data
                )

            st.session_state.job_skills = jd_result

            st.success(
                "Job description analyzed!"
            )


    if st.session_state.job_skills:

        st.subheader("Required Skills")

        for skill in st.session_state.job_skills.get(
            "skills",
            []
        ):

            st.write(f"🔹 {skill}")