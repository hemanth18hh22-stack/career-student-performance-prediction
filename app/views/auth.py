import re
import time
import random
import streamlit as st
from app.views.styles import inject

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"


def is_valid_email(email: str) -> bool:
    """Validates standard email format."""
    return bool(re.match(EMAIL_REGEX, email.strip())) if email else False


def is_valid_phone(phone: str) -> bool:
    """Validates 10-digit Indian phone number format."""
    digits = re.sub(r"\D", "", phone.strip()) if phone else ""
    return len(digits) == 10


def is_valid_password(pwd: str) -> bool:
    """Checks password minimum length requirement (>= 8)."""
    return len(pwd.strip()) >= 8 if pwd else False


def generate_otp() -> str:
    """Generates a random 6-digit OTP string."""
    return f"{random.randint(100000, 999999)}"


def render_login():
    """Renders the warm, welcoming two-column Sunrise login screen."""
    col_hero, col_card = st.columns([1.1, 1], gap="large")

    with col_hero:
        inject(
            """
            <div class="auth-hero-panel">
                <div>
                    <div class="auth-hero-floating-logo">🌅</div>
                    <h1 class="auth-hero-title">Your future starts with one step ✨</h1>
                    <p class="auth-hero-desc">Unlock personalized academic insights, track your core competencies, and shape your educational journey with confidence.</p>
                    <div class="auth-feature-cards" style="width: 100%; margin: 0; padding: 0; box-sizing: border-box;">
                        <div class="auth-feature-item" style="margin: 0; padding: 0.95rem 1.2rem; width: 100%; box-sizing: border-box;">
                            <div class="auth-feature-icon">🎯</div>
                            <div class="auth-feature-text">
                                <h4>Smart Performance Predictions</h4>
                                <p>Machine learning powered forecasts based on real student metrics.</p>
                            </div>
                        </div>
                        <div class="auth-feature-item" style="margin: 0; padding: 0.95rem 1.2rem; width: 100%; box-sizing: border-box;">
                            <div class="auth-feature-icon">💡</div>
                            <div class="auth-feature-text">
                                <h4>Personalized Growth Insights</h4>
                                <p>Pinpoint exact strengths and improvement areas before exam day.</p>
                            </div>
                        </div>
                        <div class="auth-feature-item" style="margin: 0; padding: 0.95rem 1.2rem; width: 100%; box-sizing: border-box;">
                            <div class="auth-feature-icon">🚀</div>
                            <div class="auth-feature-text">
                                <h4>Clear Career Pathways</h4>
                                <p>Bridge the gap between your technical skills and industry roles.</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div style="font-size: 0.86rem; color: rgba(255, 255, 255, 0.92); margin-top: 2rem;">🌱 Empowering students to realize their highest academic potential.</div>
            </div>
            """
        )

    with col_card:
        with st.container(border=True):
            inject('<span class="auth-card-marker"></span>')
            inject(
                """
                <div class="auth-card-header">
                    <h2>Welcome back 🌱</h2>
                    <p>Sign in to access your student dashboard & predictions</p>
                </div>
                """
            )

            # Continue with Google button
            inject('<span class="google-btn-marker"></span>')
            if st.button("Continue with Google", key="login_google_btn", use_container_width=True):
                st.info("Google sign-in will be connected in the next stage")

            # Divider with "or continue with"
            inject(
                """
                <div class="auth-divider">
                    <span>or continue with</span>
                </div>
                """
            )

            # Tabs: Email vs Phone
            tab_email, tab_phone = st.tabs(["Email", "Phone"])

            with tab_email:
                login_email = st.text_input(
                    "Email Address",
                    placeholder="student@example.com",
                    key="login_email_input",
                )
                login_pwd = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password (min 8 characters)",
                    key="login_pwd_input",
                )

                if st.button("Log in", key="login_email_submit", type="primary", use_container_width=True):
                    if not login_email or not is_valid_email(login_email):
                        st.error("Please enter a valid email address (e.g., student@example.com).")
                    elif not login_pwd or not is_valid_password(login_pwd):
                        st.error("Password must be at least 8 characters long.")
                    else:
                        demo_code = generate_otp()
                        st.session_state["otp_code"] = demo_code
                        st.session_state["otp_target"] = login_email.strip()
                        name_guess = login_email.split("@")[0].replace(".", " ").title()
                        st.session_state["user"] = {
                            "name": name_guess,
                            "email": login_email.strip(),
                        }
                        st.session_state["screen"] = "otp"
                        st.rerun()

            with tab_phone:
                p_col1, p_col2 = st.columns([1, 3.2])
                with p_col1:
                    st.text_input("Prefix", value="+91", disabled=True, key="login_prefix_fixed")
                with p_col2:
                    login_phone = st.text_input(
                        "Phone Number",
                        placeholder="9876543210",
                        max_chars=10,
                        key="login_phone_input",
                    )

                if st.button("Send OTP", key="login_phone_submit", type="primary", use_container_width=True):
                    if not login_phone or not is_valid_phone(login_phone):
                        st.error("Please enter a valid 10-digit mobile number.")
                    else:
                        clean_digits = re.sub(r"\D", "", login_phone.strip())
                        demo_code = generate_otp()
                        st.session_state["otp_code"] = demo_code
                        st.session_state["otp_target"] = f"+91 {clean_digits}"
                        st.session_state["user"] = {
                            "name": "Student",
                            "phone": f"+91 {clean_digits}",
                        }
                        st.session_state["screen"] = "otp"
                        st.rerun()

            # Link-style navigation to Signup
            inject('<span class="auth-link-marker"></span>')
            if st.button("New here? Create an account", key="go_to_signup", use_container_width=True):
                st.session_state["screen"] = "signup"
                st.rerun()

        # Small privacy note under the card
        inject(
            """
            <div style="text-align: center; color: #9CA3AF; font-size: 0.85rem; margin-top: 1rem;">
                🔒 Your data stays private
            </div>
            """
        )


def render_signup():
    """Renders the warm, welcoming two-column Sunrise signup screen."""
    col_hero, col_card = st.columns([1.1, 1], gap="large")

    with col_hero:
        inject(
            """
            <div class="auth-hero-panel">
                <div>
                    <div class="auth-hero-floating-logo">🚀</div>
                    <h1 class="auth-hero-title">Begin your journey today 🌟</h1>
                    <p class="auth-hero-desc">Join thousands of students and educators transforming academic potential into measurable future achievements.</p>
                    <div class="auth-feature-cards">
                        <div class="auth-feature-item">
                            <div class="auth-feature-icon">🎓</div>
                            <div class="auth-feature-text">
                                <h4>Accurate Academic Forecasting</h4>
                                <p>Gain foresight on exam performance before grades are finalized.</p>
                            </div>
                        </div>
                        <div class="auth-feature-item">
                            <div class="auth-feature-icon">🔍</div>
                            <div class="auth-feature-text">
                                <h4>Actionable Skill Roadmaps</h4>
                                <p>Build industry-ready competencies in Python, SQL, and Machine Learning.</p>
                            </div>
                        </div>
                        <div class="auth-feature-item">
                            <div class="auth-feature-icon">🌱</div>
                            <div class="auth-feature-text">
                                <h4>Continuous Growth Tracking</h4>
                                <p>Transform study habits into consistent semester-long success.</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div style="font-size: 0.86rem; color: rgba(255, 255, 255, 0.92); margin-top: 2rem;">✨ Zero setup friction. Start exploring insights in seconds.</div>
            </div>
            """
        )

    with col_card:
        with st.container(border=True):
            inject('<span class="auth-card-marker"></span>')
            inject(
                """
                <div class="auth-card-header">
                    <h2>Join us today ✨</h2>
                    <p>Create your free student account in seconds</p>
                </div>
                """
            )

            # Continue with Google button
            inject('<span class="google-btn-marker"></span>')
            if st.button("Continue with Google", key="signup_google_btn", use_container_width=True):
                st.info("Google sign-in will be connected in the next stage")

            # Divider with "or"
            inject(
                """
                <div class="auth-divider">
                    <span>or continue with</span>
                </div>
                """
            )

            # Name input field
            signup_name = st.text_input(
                "Full Name",
                placeholder="e.g. Alex Sharma",
                key="signup_name_input",
            )

            # Tabs: Email vs Phone
            tab_email, tab_phone = st.tabs(["Email", "Phone"])

            with tab_email:
                signup_email = st.text_input(
                    "Email Address",
                    placeholder="student@example.com",
                    key="signup_email_input",
                )
                signup_pwd = st.text_input(
                    "Password",
                    type="password",
                    placeholder="At least 8 characters",
                    key="signup_pwd_input",
                )
                signup_confirm = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-type your password",
                    key="signup_confirm_input",
                )

                if st.button("Create account", key="signup_email_submit", type="primary", use_container_width=True):
                    if not signup_name or not signup_name.strip():
                        st.error("Please provide your full name.")
                    elif not signup_email or not is_valid_email(signup_email):
                        st.error("Please enter a valid email address.")
                    elif not signup_pwd or not is_valid_password(signup_pwd):
                        st.error("Password must be at least 8 characters long.")
                    elif signup_pwd != signup_confirm:
                        st.error("Passwords do not match. Please verify and re-enter.")
                    else:
                        demo_code = generate_otp()
                        st.session_state["otp_code"] = demo_code
                        st.session_state["otp_target"] = signup_email.strip()
                        st.session_state["user"] = {
                            "name": signup_name.strip(),
                            "email": signup_email.strip(),
                        }
                        st.session_state["screen"] = "otp"
                        st.rerun()

            with tab_phone:
                p_col1, p_col2 = st.columns([1, 3.2])
                with p_col1:
                    st.text_input("Prefix", value="+91", disabled=True, key="signup_prefix_fixed")
                with p_col2:
                    signup_phone = st.text_input(
                        "Phone Number",
                        placeholder="9876543210",
                        max_chars=10,
                        key="signup_phone_input",
                    )

                if st.button("Create account", key="signup_phone_submit", type="primary", use_container_width=True):
                    if not signup_name or not signup_name.strip():
                        st.error("Please provide your full name.")
                    elif not signup_phone or not is_valid_phone(signup_phone):
                        st.error("Please enter a valid 10-digit mobile number.")
                    else:
                        clean_digits = re.sub(r"\D", "", signup_phone.strip())
                        demo_code = generate_otp()
                        st.session_state["otp_code"] = demo_code
                        st.session_state["otp_target"] = f"+91 {clean_digits}"
                        st.session_state["user"] = {
                            "name": signup_name.strip(),
                            "phone": f"+91 {clean_digits}",
                        }
                        st.session_state["screen"] = "otp"
                        st.rerun()

            # Link-style navigation back to Login
            inject('<span class="auth-link-marker"></span>')
            if st.button("Already have an account? Log in", key="go_to_login", use_container_width=True):
                st.session_state["screen"] = "login"
                st.rerun()

        # Small privacy note under the card
        inject(
            """
            <div style="text-align: center; color: #9CA3AF; font-size: 0.85rem; margin-top: 1rem;">
                🔒 Your data stays private
            </div>
            """
        )


def render_otp():
    """Renders the centered, responsive verification OTP card."""
    col_l, col_center, col_r = st.columns([1, 1.6, 1])

    with col_center:
        with st.container(border=True):
            inject('<span class="auth-card-marker otp-card-marker"></span>')

            target_display = st.session_state.get("otp_target") or "your registered device"
            current_otp = st.session_state.get("otp_code")
            if not current_otp:
                current_otp = generate_otp()
                st.session_state["otp_code"] = current_otp

            inject(
                f"""
                <div style="text-align: center; margin-bottom: 1.25rem;">
                    <div style="font-size: 2.8rem; margin-bottom: 0.5rem;">📩</div>
                    <h2 style="font-size: 1.85rem; font-weight: 700; color: #1F2937; margin-bottom: 0.4rem;">Check your inbox/phone 📩</h2>
                    <p style="color: #6B7280; font-size: 0.94rem; margin: 0; line-height: 1.5;">We have dispatched a 6-digit verification code to:<br><strong style="color: #1F2937; font-size: 1.02rem;">{target_display}</strong></p>
                </div>
                """
            )

            # Clearly labeled Demo Mode box
            inject(
                f"""
                <div class="demo-otp-box">
                    <div class="demo-otp-badge">DEMO MODE</div>
                    <div class="demo-otp-code">{current_otp}</div>
                    <div class="demo-otp-note">Demo mode: your OTP is <strong>{current_otp}</strong><br>(real SMS/email delivery comes in the next stage)</div>
                </div>
                """
            )

            # Large centered text input
            inject('<p style="text-align: center; font-weight: 600; color: #374151; margin-bottom: 0.4rem;">Enter 6-digit Code</p>')
            with st.container():
                inject('<span class="otp-input-marker"></span>')
                user_otp = st.text_input(
                    "6-Digit Code",
                    max_chars=6,
                    placeholder="• • • • • •",
                    key="otp_user_entry",
                    label_visibility="collapsed",
                )

            # Verify Button
            if st.button("Verify", key="otp_verify_btn", type="primary", use_container_width=True):
                cleaned_input = user_otp.strip() if user_otp else ""
                if cleaned_input == str(current_otp):
                    st.balloons()
                    st.success("Verification successful! Welcome aboard! 🎉")
                    time.sleep(0.8)
                    st.session_state["screen"] = "onboarding"
                    st.rerun()
                else:
                    st.error("That verification code is incorrect. Please check the demo code above and try again.")

            # Resend and Back Buttons
            st.write("")
            col_resend, col_back = st.columns(2)
            with col_resend:
                if st.button("🔄 Resend code", key="otp_resend_btn", use_container_width=True):
                    new_code = generate_otp()
                    st.session_state["otp_code"] = new_code
                    st.success("A fresh verification code was generated!")
                    st.rerun()
            with col_back:
                if st.button("⬅️ Back to Login", key="otp_back_to_login", use_container_width=True):
                    st.session_state["screen"] = "login"
                    st.rerun()


# Re-export render_onboarding from app.views.onboarding
from app.views.onboarding import render_onboarding

