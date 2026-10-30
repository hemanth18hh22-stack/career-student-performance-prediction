"""
Onboarding View for Student Performance & Career Platform.
Multi-step profile onboarding wizard with adaptive academic questions,
skill proficiency ratings, and career goal calibration.
"""

import time
from typing import Any, Dict, List
import streamlit as st
import streamlit.components.v1 as components

# Ensure components.html accepts key parameter without throwing TypeError
_orig_components_html = components.html


def _safe_components_html(html_code: str, *args, key=None, **kwargs):
    """Wrapper around components.html allowing safe usage of the key parameter."""
    return _orig_components_html(html_code, *args, **kwargs)


components.html = _safe_components_html
if hasattr(st, "components") and hasattr(st.components, "v1"):
    st.components.v1.html = _safe_components_html

from app.catalog import (
    EDUCATION_LEVELS,
    HIGH_SCHOOL_CLASSES,
    HIGH_SCHOOL_STREAMS,
    DIPLOMA_BRANCHES,
    DIPLOMA_YEARS,
    UG_DEGREES,
    UG_BRANCHES_BY_DEGREE,
    UG_YEARS_4,
    UG_YEARS_3,
    PG_DEGREES,
    PG_YEARS,
    WORKER_STATUSES,
    WORKER_BACKGROUNDS,
    SKILLS_BY_TRACK,
    COMMON_SKILLS,
    DOMAINS_BY_TRACK,
    get_track,
)
from app.views.styles import inject


def render_onboarding():
    """
    Renders the complete 3-step onboarding wizard.
    Step 1: 'Your studies' (adaptive academic catalog questions).
    Step 2: 'Your skills' (track-specific skills + common skills, proficiency grid, projects).
    Step 3: 'Your career goal' (target domain cards, learning goal, weekly time commitment).
    """
    if "onb_step" not in st.session_state:
        st.session_state["onb_step"] = 1

    if "onboarding_profile" not in st.session_state:
        st.session_state["onboarding_profile"] = {}

    current_step = st.session_state["onb_step"]

    # Scroll the parent page's main container to the top when the step changes
    st.components.v1.html(
        f"""
        <!-- key: onb_scroll_step_{current_step} -->
        <script>
            (function() {{
                function scrollToTop() {{
                    try {{
                        const parentDoc = window.parent.document;
                        const candidates = [
                            parentDoc.querySelector('[data-testid="stMain"]'),
                            parentDoc.querySelector('.stMain'),
                            parentDoc.querySelector('[data-testid="stAppViewContainer"]'),
                            parentDoc.querySelector('.main'),
                            parentDoc.documentElement,
                            parentDoc.body
                        ];
                        for (const el of candidates) {{
                            if (el) {{
                                el.scrollTop = 0;
                                if (typeof el.scrollTo === 'function') {{
                                    el.scrollTo({{ top: 0, behavior: 'instant' }});
                                }}
                            }}
                        }}
                        if (window.parent && typeof window.parent.scrollTo === 'function') {{
                            window.parent.scrollTo({{ top: 0, behavior: 'instant' }});
                        }}
                    }} catch (e) {{
                        console.warn("Scroll to top failed:", e);
                    }}
                }}
                scrollToTop();
                setTimeout(scrollToTop, 50);
                setTimeout(scrollToTop, 150);
            }})();
        </script>
        """,
        height=0,
        width=0,
        key=f"onb_scroll_step_{current_step}",
    )

    # Centered single-column layout matching the auth container style
    col_l, col_center, col_r = st.columns([1, 1.85, 1])

    with col_center:
        with st.container(border=True):
            inject('<span class="auth-card-marker onboarding-card-marker"></span>')

            # Wizard Header with Step Indicator
            step_titles = {
                1: "Your studies",
                2: "Your skills",
                3: "Your career goal",
            }
            step_title = step_titles.get(current_step, "Setup")

            inject(
                f"""
                <div style="text-align: center; margin-bottom: 1.25rem;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.35rem;">🌱</div>
                    <h2 style="font-size: 1.85rem; font-weight: 700; color: #1F2937; margin: 0 0 0.3rem 0;">
                        Student Profile Setup ✨
                    </h2>
                    <p style="color: #6B7280; font-size: 0.95rem; margin: 0;">
                        Step {current_step} of 3 • <span style="font-weight: 600; color: #EC4899;">{step_title}</span>
                    </p>
                </div>
                """
            )

            # Progress Bar (Step 1: 33%, Step 2: 66%, Step 3: 100%)
            progress_val = current_step / 3.0
            st.progress(progress_val)
            st.write("")

            # Render Active Step
            if current_step == 1:
                _render_step_1()
            elif current_step == 2:
                _render_step_2()
            else:
                _render_step_3()


def _render_step_1():
    """Renders Step 1: 'Your studies' with catalog-driven adaptive questions."""
    saved_profile = st.session_state.get("onboarding_profile", {})

    inject(
        """
        <div style="margin-bottom: 1.2rem;">
            <h3 style="font-size: 1.25rem; font-weight: 600; color: #1F2937; margin: 0 0 0.25rem 0;">
                Tell us about your education 📚
            </h3>
            <p style="color: #6B7280; font-size: 0.88rem; margin: 0;">
                We'll tailor your performance predictions and career roadmaps based on your current academic track.
            </p>
        </div>
        """
    )

    # 1. Main Education Level
    default_level_idx = 0
    saved_level = saved_profile.get("education_level")
    if saved_level in EDUCATION_LEVELS:
        default_level_idx = EDUCATION_LEVELS.index(saved_level)

    education_level = st.selectbox(
        "Current Education Level",
        options=EDUCATION_LEVELS,
        index=default_level_idx,
        key="onb_input_education_level",
    )

    # Collect answers for this step
    answers: Dict[str, Any] = {"education_level": education_level}

    # 2. Adaptive Questions Per Level
    if education_level == "High School (Class 9-12)":
        saved_class = saved_profile.get("high_school_class", 11)
        class_idx = HIGH_SCHOOL_CLASSES.index(saved_class) if saved_class in HIGH_SCHOOL_CLASSES else 2

        hs_class = st.selectbox(
            "Select Class",
            options=HIGH_SCHOOL_CLASSES,
            index=class_idx,
            format_func=lambda c: f"Class {c}",
            key="onb_input_hs_class",
        )
        answers["high_school_class"] = hs_class

        # Stream only appears for Class 11 and Class 12
        if hs_class in [11, 12]:
            saved_stream = saved_profile.get("high_school_stream", HIGH_SCHOOL_STREAMS[0])
            stream_idx = (
                HIGH_SCHOOL_STREAMS.index(saved_stream)
                if saved_stream in HIGH_SCHOOL_STREAMS
                else 0
            )
            hs_stream = st.selectbox(
                "Stream",
                options=HIGH_SCHOOL_STREAMS,
                index=stream_idx,
                key="onb_input_hs_stream",
            )
            answers["high_school_stream"] = hs_stream

    elif education_level == "Diploma / Polytechnic":
        col_branch, col_year = st.columns([1.2, 1])
        with col_branch:
            saved_branch = saved_profile.get("diploma_branch", DIPLOMA_BRANCHES[0])
            branch_idx = (
                DIPLOMA_BRANCHES.index(saved_branch)
                if saved_branch in DIPLOMA_BRANCHES
                else 0
            )
            dip_branch = st.selectbox(
                "Branch / Field",
                options=DIPLOMA_BRANCHES,
                index=branch_idx,
                key="onb_input_diploma_branch",
            )
            answers["diploma_branch"] = dip_branch

        with col_year:
            saved_year = saved_profile.get("diploma_year", DIPLOMA_YEARS[0])
            year_idx = (
                DIPLOMA_YEARS.index(saved_year)
                if saved_year in DIPLOMA_YEARS
                else 0
            )
            dip_year = st.selectbox(
                "Year of Study",
                options=DIPLOMA_YEARS,
                index=year_idx,
                format_func=lambda y: f"{y} Year" if y in ["1st", "2nd", "3rd"] else y,
                key="onb_input_diploma_year",
            )
            answers["diploma_year"] = dip_year

    elif education_level == "Undergraduate (Degree)":
        saved_degree = saved_profile.get("ug_degree", UG_DEGREES[0])
        degree_idx = (
            UG_DEGREES.index(saved_degree)
            if saved_degree in UG_DEGREES
            else 0
        )
        ug_degree = st.selectbox(
            "Degree Program",
            options=UG_DEGREES,
            index=degree_idx,
            key="onb_input_ug_degree",
        )
        answers["ug_degree"] = ug_degree

        branch_options = UG_BRANCHES_BY_DEGREE.get(ug_degree, ["Other"])
        year_options = UG_YEARS_4 if ug_degree == "B.Tech / B.E." else UG_YEARS_3

        col_branch, col_year = st.columns([1.3, 1])
        with col_branch:
            saved_branch = saved_profile.get("ug_branch", branch_options[0])
            b_idx = branch_options.index(saved_branch) if saved_branch in branch_options else 0
            ug_branch = st.selectbox(
                "Branch / Specialization",
                options=branch_options,
                index=b_idx,
                key=f"onb_input_ug_branch_{ug_degree}",
            )
            answers["ug_branch"] = ug_branch

        with col_year:
            saved_year = saved_profile.get("ug_year", year_options[0])
            y_idx = year_options.index(saved_year) if saved_year in year_options else 0
            ug_year = st.selectbox(
                "Year of Study",
                options=year_options,
                index=y_idx,
                format_func=lambda y: f"{y} Year" if y in ["1st", "2nd", "3rd", "4th"] else y,
                key=f"onb_input_ug_year_{ug_degree}",
            )
            answers["ug_year"] = ug_year

    elif education_level == "Postgraduate":
        col_degree, col_year = st.columns([1.2, 1])
        with col_degree:
            saved_degree = saved_profile.get("pg_degree", PG_DEGREES[0])
            degree_idx = PG_DEGREES.index(saved_degree) if saved_degree in PG_DEGREES else 0
            pg_degree = st.selectbox(
                "Postgraduate Degree",
                options=PG_DEGREES,
                index=degree_idx,
                key="onb_input_pg_degree",
            )
            answers["pg_degree"] = pg_degree

        with col_year:
            saved_year = saved_profile.get("pg_year", PG_YEARS[0])
            year_idx = PG_YEARS.index(saved_year) if saved_year in PG_YEARS else 0
            pg_year = st.selectbox(
                "Year of Study",
                options=PG_YEARS,
                index=year_idx,
                format_func=lambda y: f"{y} Year" if y in ["1st", "2nd"] else y,
                key="onb_input_pg_year",
            )
            answers["pg_year"] = pg_year

        saved_spec = saved_profile.get("pg_specialization", "")
        pg_specialization = st.text_input(
            "Specialization / Major",
            value=saved_spec,
            placeholder="e.g. Data Science, Machine Learning, Power Systems, Finance...",
            key="onb_input_pg_spec",
        )
        answers["pg_specialization"] = pg_specialization

    elif education_level == "Self-learner / Working professional":
        saved_status = saved_profile.get("worker_status", WORKER_STATUSES[0])
        status_idx = (
            WORKER_STATUSES.index(saved_status)
            if saved_status in WORKER_STATUSES
            else 0
        )
        worker_status = st.selectbox(
            "Current Professional Status",
            options=WORKER_STATUSES,
            index=status_idx,
            key="onb_input_worker_status",
        )
        answers["worker_status"] = worker_status

        saved_bg = saved_profile.get("worker_background", WORKER_BACKGROUNDS[0])
        bg_idx = (
            WORKER_BACKGROUNDS.index(saved_bg)
            if saved_bg in WORKER_BACKGROUNDS
            else 0
        )
        worker_background = st.selectbox(
            "Background Field",
            options=WORKER_BACKGROUNDS,
            index=bg_idx,
            key="onb_input_worker_bg",
        )
        answers["worker_background"] = worker_background

    st.write("")

    # 3. Weekly Study Hours Slider
    saved_hours = saved_profile.get("study_hours", 15)
    study_hours = st.slider(
        "Weekly study / learning hours",
        min_value=0,
        max_value=40,
        value=int(saved_hours),
        step=1,
        help="Estimated hours spent studying, attending classes, or practicing technical skills each week.",
        key="onb_input_study_hours",
    )
    answers["study_hours"] = study_hours
    answers["weekly_hours"] = study_hours

    st.write("")

    # 4. Navigation Buttons (Back & Next)
    col_back, col_next = st.columns([1, 1.2])

    with col_back:
        is_logged_in = False
        try:
            is_logged_in = bool(st.user.is_logged_in)
        except Exception:
            is_logged_in = False

        if is_logged_in:
            if st.button("Sign out", key="onb_signout_btn", use_container_width=True):
                try:
                    st.logout()
                except Exception:
                    pass
                st.session_state.clear()
                st.session_state["screen"] = "login"
                st.rerun()
        else:
            if st.button("⬅️ Return to Login", key="onb_back_btn", use_container_width=True):
                st.session_state["screen"] = "login"
                st.rerun()

    with col_next:
        if st.button("Next: Skills ➡️", key="onb_next_btn", type="primary", use_container_width=True):
            # Validation check
            if education_level == "Postgraduate":
                if not answers.get("pg_specialization", "").strip():
                    st.error("Please enter your postgraduate specialization.")
                    return

            # Compute candidate track using catalog helper
            detected_track = get_track(answers)
            answers["track"] = detected_track

            # Merge with existing profile answers and save
            merged = {**st.session_state.get("onboarding_profile", {}), **answers}
            st.session_state["onboarding_profile"] = merged
            st.session_state["onb_step"] = 2
            st.rerun()


def _render_step_2():
    """Renders Step 2: 'Your skills' with track-tailored multiselect, proficiency grid, and projects."""
    saved_profile = st.session_state.get("onboarding_profile", {})
    detected_track = saved_profile.get("track") or get_track(saved_profile)
    saved_profile["track"] = detected_track

    track_labels = {
        "tech": "Technology & Software Engineering",
        "core_engineering": "Core Engineering & Design",
        "business": "Business, Commerce & Analytics",
        "science": "Pure & Applied Sciences",
        "arts": "Humanities, Arts & Media",
        "school": "Foundational Academics",
    }
    track_name = track_labels.get(detected_track, "General Academics")

    inject(
        f"""
        <div style="margin-bottom: 1.2rem;">
            <div style="display: inline-flex; align-items: center; gap: 0.5rem; background: #FFF1EE; border: 1px solid #FECDD3; padding: 0.35rem 0.85rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600; color: #BE123C; margin-bottom: 0.6rem;">
                <span>🎯 Matched Track:</span>
                <span style="color: #EC4899;">{track_name}</span>
            </div>
            <h3 style="font-size: 1.25rem; font-weight: 600; color: #1F2937; margin: 0 0 0.25rem 0;">
                Your Skills & Competencies 🛠️
            </h3>
            <p style="color: #6B7280; font-size: 0.88rem; margin: 0;">
                Select the tools and subjects you are familiar with, then rate your proficiency level.
            </p>
        </div>
        """
    )

    # 1. Available Skills: SKILLS_BY_TRACK[track] + COMMON_SKILLS (deduped preserving order)
    track_skills = SKILLS_BY_TRACK.get(detected_track, SKILLS_BY_TRACK["tech"])
    available_skills: List[str] = list(dict.fromkeys(track_skills + COMMON_SKILLS))

    # Saved selections
    saved_skills_list = saved_profile.get("skills_list", [])
    valid_defaults = [s for s in saved_skills_list if s in available_skills]
    # If no saved skills, provide default selections relevant to track
    if not valid_defaults:
        if detected_track == "tech":
            valid_defaults = [s for s in ["Python", "SQL", "Machine Learning"] if s in available_skills]
        elif detected_track == "school":
            valid_defaults = [s for s in ["Mathematics", "Science"] if s in available_skills]
        else:
            valid_defaults = track_skills[:2]

    selected_skills = st.multiselect(
        "Select your skills",
        options=available_skills,
        default=valid_defaults,
        placeholder="Choose skills (e.g. Python, SQL, Communication...)",
        key="onb_skills_multiselect",
    )

    # 2. Proficiency Rating Grid (Beginner / Intermediate / Advanced)
    saved_skills_dict = saved_profile.get("skills", {})
    skills_levels: Dict[str, str] = {}

    if selected_skills:
        inject(
            """
            <div style="margin: 1.3rem 0 0.6rem 0;">
                <div style="font-weight: 600; font-size: 0.95rem; color: #1F2937;">Rate your proficiency:</div>
                <div style="font-size: 0.82rem; color: #6B7280;">Specify your current experience level for each selected skill.</div>
            </div>
            """
        )
        cols = st.columns(2)
        level_options = ["Beginner", "Intermediate", "Advanced"]
        for idx, skill in enumerate(selected_skills):
            with cols[idx % 2]:
                saved_lvl = saved_skills_dict.get(skill, "Beginner")
                lvl_idx = level_options.index(saved_lvl) if saved_lvl in level_options else 0
                lvl = st.selectbox(
                    f"⭐ {skill}",
                    options=level_options,
                    index=lvl_idx,
                    key=f"onb_skill_lvl_{skill}",
                )
                skills_levels[skill] = lvl
    else:
        inject(
            """
            <div style="background: #FFF7F5; border: 1px dashed #FDBA74; border-radius: 12px; padding: 0.85rem; margin-top: 0.8rem; text-align: center; color: #C2410C; font-size: 0.88rem;">
                👆 Pick one or more skills above to rate your experience levels.
            </div>
            """
        )

    st.write("")

    # 3. Projects Completed (0 to 8)
    saved_projects = saved_profile.get("projects", 2)
    projects = st.number_input(
        "Projects completed (0 to 8)",
        min_value=0,
        max_value=8,
        value=int(max(0, min(8, saved_projects))),
        step=1,
        help="Academic course assignments, personal software builds, or practical projects completed so far.",
        key="onb_projects_input",
    )

    st.write("")

    # 4. Navigation Buttons (Back & Next)
    col_back, col_next = st.columns([1, 1.2])

    with col_back:
        if st.button("⬅️ Back to Studies", key="onb_step2_back_btn", use_container_width=True):
            st.session_state["onb_step"] = 1
            st.rerun()

    with col_next:
        if st.button("Next: Career Goal ➡️", key="onb_step2_next_btn", type="primary", use_container_width=True):
            if not selected_skills:
                st.warning("Please choose at least one skill to proceed.")
                return

            saved_profile["skills_list"] = selected_skills
            saved_profile["skills"] = skills_levels
            saved_profile["projects"] = int(projects)
            st.session_state["onboarding_profile"] = saved_profile
            st.session_state["onb_step"] = 3
            st.rerun()


def _render_step_3():
    """Renders Step 3: 'Your career goal' with selectable domain cards, learning goal, and weekly time."""
    saved_profile = st.session_state.get("onboarding_profile", {})
    detected_track = saved_profile.get("track") or get_track(saved_profile)
    saved_profile["track"] = detected_track

    domain_options = DOMAINS_BY_TRACK.get(detected_track, DOMAINS_BY_TRACK["tech"])

    inject(
        """
        <div style="margin-bottom: 1.2rem;">
            <h3 style="font-size: 1.25rem; font-weight: 600; color: #1F2937; margin: 0 0 0.25rem 0;">
                Your Career Goal & Commitment 🎯
            </h3>
            <p style="color: #6B7280; font-size: 0.88rem; margin: 0;">
                Choose your target specialization and define your weekly learning pace.
            </p>
        </div>
        """
    )

    # 1. Target Domain Cards (DOMAINS_BY_TRACK[track] styled as selectable cards)
    inject('<span class="domain-cards-marker"></span>')
    inject(
        """
        <div style="font-weight: 600; font-size: 0.95rem; color: #1F2937; margin-bottom: 0.4rem;">
            Select your target career domain:
        </div>
        """
    )

    saved_domain = saved_profile.get("domain", domain_options[0])
    domain_idx = domain_options.index(saved_domain) if saved_domain in domain_options else 0

    selected_domain = st.radio(
        "Target Domain",
        options=domain_options,
        index=domain_idx,
        label_visibility="collapsed",
        key="onb_domain_radio",
    )

    st.write("")

    # 2. Learning Goal Options
    goal_options = [
        "Get a job",
        "Higher studies",
        "Improve grades",
        "Switch careers",
        "Learn for fun",
    ]
    saved_goal = saved_profile.get("goal", goal_options[0])
    goal_idx = goal_options.index(saved_goal) if saved_goal in goal_options else 0

    selected_goal = st.selectbox(
        "Primary learning goal",
        options=goal_options,
        index=goal_idx,
        key="onb_learning_goal_select",
    )

    # 3. Time Per Week Commitment Options
    time_options = ["under 5 hrs", "5 to 10", "10 to 20", "20 plus"]
    saved_time = saved_profile.get("hours_per_week", time_options[1])
    time_idx = time_options.index(saved_time) if saved_time in time_options else 1

    selected_time = st.selectbox(
        "Time dedicated per week",
        options=time_options,
        index=time_idx,
        key="onb_time_per_week_select",
    )

    st.write("")

    # 4. Navigation Buttons (Back & Finish)
    col_back, col_next = st.columns([1, 1.3])

    with col_back:
        if st.button("⬅️ Back to Skills", key="onb_step3_back_btn", use_container_width=True):
            st.session_state["onb_step"] = 2
            st.rerun()

    with col_next:
        if st.button("Finish and see my dashboard 🎉", key="onb_finish_btn", type="primary", use_container_width=True):
            # Gather all education answers, weekly hours, skills, projects, domain, goal, hours_per_week
            weekly_study_hours = saved_profile.get("study_hours", 15)

            final_profile: Dict[str, Any] = {
                **saved_profile,
                "education_level": saved_profile.get("education_level", "Undergraduate (Degree)"),
                "track": detected_track,
                "weekly_hours": weekly_study_hours,
                "skills": saved_profile.get("skills", {}),
                "projects": saved_profile.get("projects", 2),
                "domain": selected_domain,
                "goal": selected_goal,
                "hours_per_week": selected_time,
            }

            # Save canonical profile to session_state["profile"]
            st.session_state["profile"] = final_profile
            st.session_state["profile_just_completed"] = True

            # Celebrate with balloons and friendly message
            st.balloons()
            st.success("🎉 Welcome aboard! Your personalized student profile is calibrated. Launching dashboard...")

            # Transition to analyzer screen
            time.sleep(1.0)
            st.session_state["screen"] = "analyzer"
            st.rerun()
