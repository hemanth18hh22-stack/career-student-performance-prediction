import streamlit as st


def inject(html: str):
    """Strips all leading/trailing whitespace and blank lines before injecting raw HTML/CSS into Streamlit."""
    cleaned = "".join(line.strip() for line in html.splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)


def inject_base_styles():
    """Injects core sunrise palette typography and auth container styles."""
    inject(
        """
        <div class="auth-bg-blobs" aria-hidden="true">
            <div class="auth-blob blob-peach"></div>
            <div class="auth-blob blob-pink"></div>
            <div class="auth-blob blob-purple"></div>
        </div>
        """
    )
    inject(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        :root {
            --sunrise-peach: #FF8A65;
            --sunrise-coral: #FF7043;
            --sunrise-pink: #EC4899;
            --sunrise-soft-pink: #F472B6;
            --sunrise-lavender: #8B5CF6;
            --sunrise-soft-lavender: #DDD6FE;
            --sunrise-teal: #0D9488;
            --sunrise-soft-teal: #14B8A6;
            --sunrise-bg-soft: #FFF9F7;
        }

        /* ================= PAGE BACKGROUND & PASTEL BLOBS ================= */
        .stApp {
            background: linear-gradient(135deg, #FFF1E6 0%, #FDF2F8 50%, #F3E8FF 100%) !important;
            background-attachment: fixed !important;
        }

        [data-testid="stAppViewContainer"] > .main {
            position: relative;
            z-index: 1;
        }

        .auth-bg-blobs {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            z-index: 0;
            pointer-events: none;
        }

        .auth-blob {
            position: fixed;
            border-radius: 50%;
            filter: blur(85px);
            pointer-events: none;
            z-index: 0;
        }

        .blob-peach {
            width: 480px;
            height: 480px;
            background: radial-gradient(circle, rgba(255, 122, 69, 0.28) 0%, rgba(255, 241, 230, 0) 70%);
            top: -80px;
            left: -80px;
        }

        .blob-pink {
            width: 520px;
            height: 520px;
            background: radial-gradient(circle, rgba(236, 72, 153, 0.22) 0%, rgba(244, 114, 182, 0) 70%);
            bottom: -100px;
            left: 30%;
        }

        .blob-purple {
            width: 460px;
            height: 460px;
            background: radial-gradient(circle, rgba(139, 92, 246, 0.22) 0%, rgba(221, 214, 254, 0) 70%);
            top: 60px;
            right: -80px;
        }

        html, body, [class*="css"], .stMarkdown, .stText {
            font-family: 'Poppins', sans-serif !important;
        }

        /* ================= FLOATING SUNRISE LOGO ================= */
        @keyframes heroLogoFloat {
            0% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-8px);
            }
            100% {
                transform: translateY(0);
            }
        }

        .auth-hero-floating-logo {
            font-size: 2.4rem;
            margin-bottom: 0.6rem;
            display: inline-block;
            animation: heroLogoFloat 3.5s ease-in-out infinite;
            will-change: transform;
        }

        /* ================= HIDE STREAMLIT HEADING ANCHORS ================= */
        [data-testid="stHeaderActionElements"] { display: none !important; }
        a.anchor-link, h1 a, h2 a, h3 a { display: none !important; }

        /* Top header bar for active screen */
        .platform-nav-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.6rem 1.4rem;
            background: linear-gradient(90deg, #FFF7F5 0%, #FAF5FF 50%, #F0FDFA 100%);
            border: 1px solid #FCE7F3;
            border-radius: 14px;
            margin-bottom: 1.8rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
        }
        .platform-brand {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            font-size: 1.15rem;
            font-weight: 700;
            color: #1F2937;
        }
        .platform-badge {
            background: linear-gradient(135deg, #FF7043 0%, #EC4899 100%);
            color: #FFFFFF;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.2rem 0.6rem;
            border-radius: 8px;
            letter-spacing: 0.03em;
        }
        .platform-user-info {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            font-size: 0.9rem;
            color: #4B5563;
        }

        /* ================= AUTH HERO PANEL ================= */
        .auth-hero-panel {
            background: linear-gradient(140deg, #FF7043 0%, #EC4899 45%, #8B5CF6 100%);
            border-radius: 24px;
            padding: 2.8rem 2.2rem;
            color: #FFFFFF;
            box-shadow: 0 15px 35px rgba(236, 72, 153, 0.22);
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-sizing: border-box;
        }
        .auth-hero-title {
            font-size: 2.25rem;
            font-weight: 700;
            color: #FFFFFF !important;
            line-height: 1.25;
            margin-bottom: 0.75rem;
        }
        .auth-hero-desc {
            font-size: 1.05rem;
            color: rgba(255, 255, 255, 0.95) !important;
            line-height: 1.6;
            margin-bottom: 2rem;
        }
        .auth-feature-cards {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            box-sizing: border-box !important;
        }
        .auth-feature-item {
            display: flex;
            align-items: center;
            gap: 1rem;
            background: rgba(255, 255, 255, 0.16);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            margin: 0 !important;
            padding: 0.95rem 1.2rem !important;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.28);
            box-sizing: border-box !important;
            width: 100% !important;
            transition: transform 0.2s ease, background 0.2s ease;
        }
        .auth-feature-item:hover {
            transform: translateY(-2px);
            background: rgba(255, 255, 255, 0.24);
        }
        .auth-feature-icon {
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 44px;
            height: 44px;
            background: rgba(255, 255, 255, 0.25);
            border-radius: 12px;
            flex-shrink: 0;
        }
        .auth-feature-text h4 {
            color: #FFFFFF !important;
            font-size: 0.98rem;
            font-weight: 600;
            margin: 0 0 0.15rem 0;
        }
        .auth-feature-text p {
            color: rgba(255, 255, 255, 0.9) !important;
            font-size: 0.84rem;
            margin: 0;
            line-height: 1.35;
        }

        /* ================= AUTH CARD CONTAINER (:has) ================= */
        @keyframes authFadeUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.auth-card-marker),
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .auth-card-marker),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.onboarding-card-marker),
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .onboarding-card-marker) {
            border: 3px solid transparent !important;
            border-radius: 24px !important;
            background:
                linear-gradient(#FFFFFF, #FFFFFF) padding-box,
                linear-gradient(135deg, #FF7A45, #EC4899, #8B5CF6) border-box !important;
            box-shadow: 0 20px 60px rgba(236, 72, 153, 0.18) !important;
            padding: 2.6rem 2.4rem 2.2rem 2.4rem !important;
            animation: authFadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
            transition: box-shadow 0.3s ease !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.auth-card-marker):hover,
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .auth-card-marker):hover,
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.onboarding-card-marker):hover,
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .onboarding-card-marker):hover {
            box-shadow: 0 24px 70px rgba(236, 72, 153, 0.24) !important;
        }

        /* OTP Specific Centered Card */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.otp-card-marker),
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .otp-card-marker) {
            padding: 2.5rem 2.2rem 2rem 2.2rem !important;
        }

        /* Onboarding Specific Centered Card */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.onboarding-card-marker),
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .onboarding-card-marker) {
            padding: 2.4rem 2.2rem 2rem 2.2rem !important;
        }

        /* Card Inner Header */
        .auth-card-header {
            margin-bottom: 1.25rem;
        }
        .auth-card-header h2 {
            color: #1F2937 !important;
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
        }
        .auth-card-header p {
            color: #6B7280 !important;
            font-size: 0.92rem;
            margin: 0;
        }

        /* ================= GOOGLE BUTTON ================= */
        div.st-key-login_google_btn button,
        div.st-key-signup_google_btn button {
            background-color: #FFFFFF !important;
            color: #374151 !important;
            border: 1.5px solid #E9D5FF !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            padding: 0.68rem 1rem !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
            text-decoration: none !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        div.st-key-login_google_btn button p,
        div.st-key-signup_google_btn button p {
            color: #374151 !important;
            font-weight: 600 !important;
            text-decoration: none !important;
            margin: 0 !important;
        }
        div.st-key-login_google_btn button:hover,
        div.st-key-signup_google_btn button:hover {
            background-color: #FFF7F5 !important;
            border-color: #EC4899 !important;
            box-shadow: 0 4px 14px rgba(236, 72, 153, 0.12) !important;
            color: #111827 !important;
            transform: translateY(-1px) !important;
        }
        div.st-key-login_google_btn button::before,
        div.st-key-signup_google_btn button::before {
            content: "";
            display: inline-block;
            width: 18px;
            height: 18px;
            margin-right: 10px;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Cpath fill='%23EA4335' d='M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z'/%3E%3Cpath fill='%234285F4' d='M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z'/%3E%3Cpath fill='%23FBBC05' d='M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z'/%3E%3Cpath fill='%2334A853' d='M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z'/%3E%3C/svg%3E");
            background-size: contain;
            background-repeat: no-repeat;
            vertical-align: middle;
        }

        /* ================= AUTH DIVIDER ================= */
        .auth-divider {
            display: flex;
            align-items: center;
            text-align: center;
            margin: 1.25rem 0 1.35rem 0;
            color: #9CA3AF;
            font-size: 0.85rem;
            font-weight: 500;
        }
        .auth-divider::before {
            content: '';
            flex: 1;
            height: 1.5px;
            background: linear-gradient(90deg, rgba(236, 72, 153, 0) 0%, rgba(236, 72, 153, 0.35) 100%);
            border: none;
        }
        .auth-divider::after {
            content: '';
            flex: 1;
            height: 1.5px;
            background: linear-gradient(90deg, rgba(236, 72, 153, 0.35) 0%, rgba(236, 72, 153, 0) 100%);
            border: none;
        }
        .auth-divider span {
            padding: 0 0.85rem;
            color: #9CA3AF;
            text-transform: lowercase;
            font-size: 0.82rem;
            letter-spacing: 0.04em;
            font-weight: 500;
        }

        /* ================= STREAMLIT TABS STYLING ================= */
        div[data-testid="stTabs"] div[role="tablist"],
        div[data-baseweb="tab-list"] {
            gap: 0.65rem !important;
            border-bottom: none !important;
            background: transparent !important;
            padding: 0.25rem 0 !important;
            margin-bottom: 1rem !important;
        }
        div[data-testid="stTabs"] div[role="tablist"]::after,
        div[data-baseweb="tab-highlight"],
        div[data-baseweb="tab-border"],
        .react-aria-SelectionIndicator {
            display: none !important;
            content: none !important;
        }
        div[data-testid="stTabs"] div[role="tab"],
        div[data-testid="stTab"],
        button[data-baseweb="tab"] {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            padding: 0.55rem 1.4rem !important;
            border-radius: 999px !important;
            border: none !important;
            box-shadow: none !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            height: auto !important;
        }
        div[data-testid="stTabs"] div[role="tab"]:not([aria-selected="true"]):not([data-selected="true"]),
        div[data-testid="stTab"]:not([aria-selected="true"]):not([data-selected="true"]),
        button[data-baseweb="tab"]:not([aria-selected="true"]) {
            background-color: #F3E8FF !important;
            color: #374151 !important;
        }
        div[data-testid="stTabs"] div[role="tab"]:not([aria-selected="true"]):not([data-selected="true"]) p,
        div[data-testid="stTab"]:not([aria-selected="true"]):not([data-selected="true"]) p,
        button[data-baseweb="tab"]:not([aria-selected="true"]) p,
        button[data-baseweb="tab"]:not([aria-selected="true"]) div,
        button[data-baseweb="tab"]:not([aria-selected="true"]) span {
            color: #374151 !important;
            font-weight: 600 !important;
            margin: 0 !important;
        }
        div[data-testid="stTabs"] div[role="tab"]:not([aria-selected="true"]):not([data-selected="true"]):hover,
        div[data-testid="stTab"]:not([aria-selected="true"]):not([data-selected="true"]):hover,
        button[data-baseweb="tab"]:not([aria-selected="true"]):hover {
            background-color: #EDE9FE !important;
            color: #1F2937 !important;
        }
        div[data-testid="stTabs"] div[role="tab"]:not([aria-selected="true"]):not([data-selected="true"]):hover p,
        div[data-testid="stTab"]:not([aria-selected="true"]):not([data-selected="true"]):hover p,
        button[data-baseweb="tab"]:not([aria-selected="true"]):hover p {
            color: #1F2937 !important;
        }
        div[data-testid="stTabs"] div[role="tab"][aria-selected="true"],
        div[data-testid="stTabs"] div[role="tab"][data-selected="true"],
        div[data-testid="stTab"][aria-selected="true"],
        div[data-testid="stTab"][data-selected="true"],
        button[data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #FF7A45 0%, #EC4899 50%, #8B5CF6 100%) !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 14px rgba(236, 72, 153, 0.3) !important;
            border: none !important;
        }
        div[data-testid="stTabs"] div[role="tab"][aria-selected="true"] p,
        div[data-testid="stTabs"] div[role="tab"][data-selected="true"] p,
        div[data-testid="stTab"][aria-selected="true"] p,
        div[data-testid="stTab"][data-selected="true"] p,
        button[data-baseweb="tab"][aria-selected="true"] p,
        button[data-baseweb="tab"][aria-selected="true"] div,
        button[data-baseweb="tab"][aria-selected="true"] span {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            margin: 0 !important;
        }

        /* ================= PRIMARY BUTTONS (SUNRISE GRADIENT) ================= */
        button[kind="primary"],
        button[data-testid="stBaseButton-primary"],
        div.st-key-login_email_submit button,
        div.st-key-login_phone_submit button,
        div.st-key-signup_email_submit button,
        div.st-key-signup_phone_submit button,
        div.st-key-otp_verify_btn button,
        div.st-key-onboard_continue_btn button {
            background: linear-gradient(135deg, #FF7043 0%, #EC4899 50%, #8B5CF6 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 1.6rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3) !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100% !important;
            margin-top: 0.8rem !important;
            text-decoration: none !important;
        }
        button[kind="primary"] p,
        button[data-testid="stBaseButton-primary"] p,
        div.st-key-login_email_submit button p,
        div.st-key-login_phone_submit button p,
        div.st-key-signup_email_submit button p,
        div.st-key-signup_phone_submit button p,
        div.st-key-otp_verify_btn button p,
        div.st-key-onboard_continue_btn button p {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            text-decoration: none !important;
            margin: 0 !important;
        }
        button[kind="primary"]::before,
        button[data-testid="stBaseButton-primary"]::before,
        div.st-key-login_email_submit button::before,
        div.st-key-login_phone_submit button::before,
        div.st-key-signup_email_submit button::before,
        div.st-key-signup_phone_submit button::before,
        div.st-key-otp_verify_btn button::before,
        div.st-key-onboard_continue_btn button::before {
            display: none !important;
        }
        button[kind="primary"]:hover,
        button[data-testid="stBaseButton-primary"]:hover,
        div.st-key-login_email_submit button:hover,
        div.st-key-login_phone_submit button:hover,
        div.st-key-signup_email_submit button:hover,
        div.st-key-signup_phone_submit button:hover,
        div.st-key-otp_verify_btn button:hover,
        div.st-key-onboard_continue_btn button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 28px rgba(236, 72, 153, 0.48) !important;
            color: #FFFFFF !important;
        }
        button[kind="primary"]:hover p,
        button[data-testid="stBaseButton-primary"]:hover p,
        div.st-key-login_email_submit button:hover p,
        div.st-key-login_phone_submit button:hover p,
        div.st-key-signup_email_submit button:hover p,
        div.st-key-signup_phone_submit button:hover p,
        div.st-key-otp_verify_btn button:hover p,
        div.st-key-onboard_continue_btn button:hover p {
            color: #FFFFFF !important;
        }
        div.st-key-login_phone_submit button,
        div.st-key-signup_email_submit button,
        div.st-key-signup_phone_submit button,
        div.st-key-otp_verify_btn button,
        div.st-key-onboard_continue_btn button {
            background: linear-gradient(135deg, #FF7043 0%, #EC4899 50%, #8B5CF6 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 1.6rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3) !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100% !important;
            margin-top: 0.8rem !important;
            text-decoration: none !important;
        }
        button[kind="primary"] p,
        button[data-testid="stBaseButton-primary"] p,
        div.st-key-login_email_submit button p,
        div.st-key-login_phone_submit button p,
        div.st-key-signup_email_submit button p,
        div.st-key-signup_phone_submit button p,
        div.st-key-otp_verify_btn button p,
        div.st-key-onboard_continue_btn button p {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            text-decoration: none !important;
            margin: 0 !important;
        }
        button[kind="primary"]::before,
        button[data-testid="stBaseButton-primary"]::before,
        div.st-key-login_email_submit button::before,
        div.st-key-login_phone_submit button::before,
        div.st-key-signup_email_submit button::before,
        div.st-key-signup_phone_submit button::before,
        div.st-key-otp_verify_btn button::before,
        div.st-key-onboard_continue_btn button::before {
            display: none !important;
        }
        button[kind="primary"]:hover,
        button[data-testid="stBaseButton-primary"]:hover,
        div.st-key-login_email_submit button:hover,
        div.st-key-login_phone_submit button:hover,
        div.st-key-signup_email_submit button:hover,
        div.st-key-signup_phone_submit button:hover,
        div.st-key-otp_verify_btn button:hover,
        div.st-key-onboard_continue_btn button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(236, 72, 153, 0.45) !important;
            color: #FFFFFF !important;
        }
        button[kind="primary"]:hover p,
        button[data-testid="stBaseButton-primary"]:hover p,
        div.st-key-login_email_submit button:hover p,
        div.st-key-login_phone_submit button:hover p,
        div.st-key-signup_email_submit button:hover p,
        div.st-key-signup_phone_submit button:hover p,
        div.st-key-otp_verify_btn button:hover p,
        div.st-key-onboard_continue_btn button:hover p {
            color: #FFFFFF !important;
        }

        /* ================= LINK-STYLE BUTTONS ================= */
        div.st-key-go_to_signup button,
        div.st-key-go_to_login button,
        div.st-key-otp_back_to_login button,
        div.st-key-onboard_back_login button {
            background: transparent !important;
            color: #8B5CF6 !important;
            border: none !important;
            box-shadow: none !important;
            font-weight: 600 !important;
            font-size: 0.93rem !important;
            padding: 0.5rem 0.8rem !important;
            text-decoration: underline !important;
            text-underline-offset: 4px !important;
            width: 100% !important;
            transition: all 0.2s ease !important;
            margin-top: 0.6rem !important;
        }
        div.st-key-go_to_signup button p,
        div.st-key-go_to_login button p,
        div.st-key-otp_back_to_login button p,
        div.st-key-onboard_back_login button p {
            color: #8B5CF6 !important;
            font-weight: 600 !important;
            text-decoration: underline !important;
            margin: 0 !important;
        }
        div.st-key-go_to_signup button:hover,
        div.st-key-go_to_login button:hover,
        div.st-key-otp_back_to_login button:hover,
        div.st-key-onboard_back_login button:hover {
            color: #EC4899 !important;
            background: rgba(236, 72, 153, 0.06) !important;
            border: none !important;
        }
        div.st-key-go_to_signup button:hover p,
        div.st-key-go_to_login button:hover p,
        div.st-key-otp_back_to_login button:hover p,
        div.st-key-onboard_back_login button:hover p {
            color: #EC4899 !important;
        }
        div.st-key-go_to_signup button::before,
        div.st-key-go_to_login button::before,
        div.st-key-otp_back_to_login button::before,
        div.st-key-onboard_back_login button::before {
            display: none !important;
        }

        /* Resend button */
        div.st-key-otp_resend_btn button {
            border: 1.5px solid #DDD6FE !important;
            color: #7C3AED !important;
            background: #FAF5FF !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
        }
        div.st-key-otp_resend_btn button p {
            color: #7C3AED !important;
            font-weight: 600 !important;
        }
        div.st-key-otp_resend_btn button::before {
            display: none !important;
        }

        /* ================= OTP LARGE INPUT & DEMO BOX ================= */
        div[data-testid="stVerticalBlock"]:has(.otp-input-marker) input {
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.75rem !important;
            text-align: center !important;
            color: #1F2937 !important;
            border: 2px solid #DDD6FE !important;
            border-radius: 14px !important;
            background: #FAF5FF !important;
            height: 64px !important;
        }
        div[data-testid="stVerticalBlock"]:has(.otp-input-marker) input:focus {
            border-color: #8B5CF6 !important;
            box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.18) !important;
            background: #FFFFFF !important;
        }

        .demo-otp-box {
            background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
            border: 1.5px dashed #F59E0B;
            border-radius: 14px;
            padding: 1.1rem;
            text-align: center;
            margin: 1.25rem 0 1.5rem 0;
        }
        .demo-otp-badge {
            display: inline-block;
            background: #F59E0B;
            color: #FFFFFF;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
        }
        .demo-otp-code {
            font-size: 1.8rem;
            font-weight: 700;
            color: #B45309;
            letter-spacing: 0.2em;
            font-family: monospace;
        }
        .demo-otp-note {
            font-size: 0.83rem;
            color: #92400E;
            margin-top: 0.35rem;
        }

        /* ================= INPUTS STYLING ================= */
        div[data-baseweb="input"],
        div[data-baseweb="base-input"] {
            background-color: #FFFFFF !important;
            border: 1.5px solid #E9D5FF !important;
            border-radius: 12px !important;
            box-shadow: none !important;
            transition: all 0.2s ease !important;
        }
        div[data-baseweb="input"] input,
        div[data-baseweb="base-input"] input {
            background-color: #FFFFFF !important;
            border-radius: 10px !important;
            color: #1F2937 !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 0.95rem !important;
        }
        div[data-baseweb="input"]:focus-within,
        div[data-baseweb="base-input"]:focus-within {
            border-color: #8B5CF6 !important;
            box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.15) !important;
        }
        div[data-baseweb="input"]:has(input:disabled) {
            background-color: #FAF5FF !important;
            border-color: #E9D5FF !important;
        }

        /* ================= SELECTBOX STYLING ================= */
        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            border: 1.5px solid #E9D5FF !important;
            border-radius: 12px !important;
            box-shadow: none !important;
            transition: all 0.2s ease !important;
        }
        div[data-baseweb="select"]:focus-within > div {
            border-color: #8B5CF6 !important;
            box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.15) !important;
        }

        /* ================= PROGRESS BAR & SLIDER STYLING ================= */
        div[data-testid="stProgressBar"] > div {
            background-color: #F3E8FF !important;
            border-radius: 999px !important;
            height: 10px !important;
        }
        div[data-testid="stProgressBar"] > div > div {
            background: linear-gradient(90deg, #FF7A45 0%, #EC4899 50%, #8B5CF6 100%) !important;
            border-radius: 999px !important;
        }
        div[data-testid="stSlider"] div[role="slider"] {
            background-color: #EC4899 !important;
            border: 2px solid #FFFFFF !important;
            box-shadow: 0 2px 8px rgba(236, 72, 153, 0.4) !important;
        }

        /* ================= ONBOARDING BUTTONS ================= */
        div.st-key-onb_back_btn button,
        div.st-key-onb_step2_back_btn button,
        div.st-key-onb_step3_back_btn button {
            background-color: #F3E8FF !important;
            color: #6B21A8 !important;
            border: 1.5px solid #E9D5FF !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            padding: 0.72rem 1.4rem !important;
            transition: all 0.2s ease !important;
            margin-top: 0.8rem !important;
        }
        div.st-key-onb_back_btn button p,
        div.st-key-onb_step2_back_btn button p,
        div.st-key-onb_step3_back_btn button p {
            color: #6B21A8 !important;
            font-weight: 600 !important;
            margin: 0 !important;
        }
        div.st-key-onb_back_btn button:hover,
        div.st-key-onb_step2_back_btn button:hover,
        div.st-key-onb_step3_back_btn button:hover {
            background-color: #EDE9FE !important;
            border-color: #C084FC !important;
            color: #581C87 !important;
            transform: translateY(-1px) !important;
        }
        div.st-key-onb_next_btn button,
        div.st-key-onb_step2_next_btn button,
        div.st-key-onb_finish_btn button {
            background: linear-gradient(135deg, #FF7043 0%, #EC4899 50%, #8B5CF6 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.72rem 1.4rem !important;
            font-weight: 600 !important;
            font-size: 0.98rem !important;
            box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3) !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            margin-top: 0.8rem !important;
        }
        div.st-key-onb_next_btn button p,
        div.st-key-onb_step2_next_btn button p,
        div.st-key-onb_finish_btn button p {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            margin: 0 !important;
        }
        div.st-key-onb_next_btn button:hover,
        div.st-key-onb_step2_next_btn button:hover,
        div.st-key-onb_finish_btn button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(236, 72, 153, 0.45) !important;
            color: #FFFFFF !important;
        }

        /* ================= DOMAIN CARDS (st.radio styled as cards) ================= */
        div:has(> div[data-testid="stElementContainer"] .domain-cards-marker) div[role="radiogroup"],
        div[data-testid="stVerticalBlock"]:has(.domain-cards-marker) div[role="radiogroup"] {
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 0.75rem !important;
        }
        div:has(> div[data-testid="stElementContainer"] .domain-cards-marker) div[role="radiogroup"] label,
        div[data-testid="stVerticalBlock"]:has(.domain-cards-marker) div[role="radiogroup"] label {
            background: #FFFFFF !important;
            border: 1.5px solid #E9D5FF !important;
            border-radius: 14px !important;
            padding: 0.8rem 1rem !important;
            margin: 0 !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02) !important;
        }
        div:has(> div[data-testid="stElementContainer"] .domain-cards-marker) div[role="radiogroup"] label:hover,
        div[data-testid="stVerticalBlock"]:has(.domain-cards-marker) div[role="radiogroup"] label:hover {
            background: #FFF7F5 !important;
            border-color: #EC4899 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(236, 72, 153, 0.12) !important;
        }
        div:has(> div[data-testid="stElementContainer"] .domain-cards-marker) div[role="radiogroup"] label:has(input:checked),
        div[data-testid="stVerticalBlock"]:has(.domain-cards-marker) div[role="radiogroup"] label:has(input:checked) {
            background: linear-gradient(135deg, #FFF1EE 0%, #FDF2F8 100%) !important;
            border-color: #EC4899 !important;
            border-width: 2px !important;
            box-shadow: 0 4px 15px rgba(236, 72, 153, 0.18) !important;
        }

        /* ================= MULTISELECT TAGS ================= */
        div[data-baseweb="tag"] {
            background: linear-gradient(135deg, #FFE4E6 0%, #F3E8FF 100%) !important;
            border: 1px solid #F472B6 !important;
            border-radius: 8px !important;
            color: #831843 !important;
            font-weight: 600 !important;
        }
        div[data-baseweb="tag"] span {
            color: #831843 !important;
            font-weight: 600 !important;
        }
        </style>
        """
    )


def inject_analyzer_styles():
    """Injects styles for the prediction analyzer (preserved completely from original app)."""
    inject(
        """
        <style>
        /* Header Banner */
        .header-banner {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2.5rem 2rem;
            border-radius: 20px;
            color: #FFFFFF;
            text-align: center;
            margin-top: 0.5rem;
            margin-bottom: 2.5rem;
            box-shadow: 0 10px 25px rgba(118, 75, 162, 0.25);
        }
        .header-banner h1 {
            color: #FFFFFF !important;
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        .header-banner p {
            font-size: 1.15rem;
            opacity: 0.95;
            margin: 0;
            color: #F3F4F6 !important;
        }
        
        /* Marker Container Cards Styling using scoped CSS :has() */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div .academic-marker),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(> div .academic-marker),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.academic-marker) {
            border: 1.5px solid #BFDBFE !important;
            border-left: 6px solid #3B82F6 !important;
            background: linear-gradient(180deg, #EFF6FF 0%, #FFFFFF 140px) !important;
            border-radius: 16px !important;
            padding: 1.8rem !important;
            margin-bottom: 2.2rem !important;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.08) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.academic-marker):hover {
            box-shadow: 0 12px 32px rgba(59, 130, 246, 0.15) !important;
            transform: translateY(-3px) !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div .skills-marker),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(> div .skills-marker),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.skills-marker) {
            border: 1.5px solid #A7F3D0 !important;
            border-left: 6px solid #10B981 !important;
            background: linear-gradient(180deg, #ECFDF5 0%, #FFFFFF 140px) !important;
            border-radius: 16px !important;
            padding: 1.8rem !important;
            margin-bottom: 2.2rem !important;
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.08) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.skills-marker):hover {
            box-shadow: 0 12px 32px rgba(16, 185, 129, 0.15) !important;
            transform: translateY(-3px) !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div .habits-marker),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(> div .habits-marker),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.habits-marker) {
            border: 1.5px solid #FED7AA !important;
            border-left: 6px solid #F97316 !important;
            background: linear-gradient(180deg, #FFF7ED 0%, #FFFFFF 140px) !important;
            border-radius: 16px !important;
            padding: 1.8rem !important;
            margin-bottom: 2.2rem !important;
            box-shadow: 0 8px 25px rgba(249, 115, 22, 0.08) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.habits-marker):hover {
            box-shadow: 0 12px 32px rgba(249, 115, 22, 0.15) !important;
            transform: translateY(-3px) !important;
        }
        
        .card-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #1F2937;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1.25rem;
        }
        
        .icon-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 42px;
            height: 42px;
            border-radius: 50%;
            font-size: 1.25rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        }
        
        .icon-blue { background-color: #DBEAFE; color: #1D4ED8; }
        .icon-green { background-color: #D1FAE5; color: #047857; }
        .icon-orange { background-color: #FFEDD5; color: #C2410C; }
        
        /* Native Input Widgets Styling */
        div[data-baseweb="input"], div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            border: 1.5px solid #E5E7EB !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02) !important;
            transition: all 0.2s ease-in-out !important;
        }
        
        div[data-baseweb="input"]:hover, div[data-baseweb="select"] > div:hover {
            border-color: #A78BFA !important;
            box-shadow: 0 3px 8px rgba(139, 92, 246, 0.12) !important;
        }
        
        div[data-baseweb="input"]:focus-within, div[data-baseweb="select"] > div:focus-within {
            border-color: #8B5CF6 !important;
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2) !important;
        }
        
        input[type="number"] {
            color: #1F2937 !important;
            font-weight: 500 !important;
            font-family: 'Poppins', sans-serif !important;
        }
        
        div[data-baseweb="select"] span {
            color: #1F2937 !important;
            font-weight: 500 !important;
            font-family: 'Poppins', sans-serif !important;
        }
        
        /* Stepper buttons (+/-) */
        button[data-testid="stNumberInputStepDown"], button[data-testid="stNumberInputStepUp"] {
            background-color: #F3F4F6 !important;
            border: none !important;
            border-radius: 8px !important;
            color: #374151 !important;
            transition: background-color 0.2s ease !important;
        }
        
        button[data-testid="stNumberInputStepDown"]:hover, button[data-testid="stNumberInputStepUp"]:hover {
            background-color: #DDD6FE !important;
            color: #6D28D9 !important;
        }
        
        /* Widget Labels */
        label[data-testid="stWidgetLabel"], label[data-testid="stWidgetLabel"] p {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
            color: #374151 !important;
            font-size: 0.95rem !important;
            margin-bottom: 0.4rem !important;
        }
        
        /* Form Container & Submit Button */
        div[data-testid="stForm"] {
            border: none !important;
            padding: 0 !important;
            background: transparent !important;
        }
        
        div.stFormSubmitButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: #FFFFFF !important;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 0.9rem 2.5rem !important;
            font-size: 1.15rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100% !important;
            cursor: pointer !important;
            box-shadow: 0 4px 15px rgba(118, 75, 162, 0.35) !important;
            margin-top: 1rem !important;
        }
        
        div.stFormSubmitButton > button:hover {
            transform: translateY(-3px) scale(1.005) !important;
            box-shadow: 0 10px 30px rgba(118, 75, 162, 0.5) !important;
            color: #FFFFFF !important;
        }
        
        /* Result Cards */
        .result-card {
            border-radius: 20px;
            padding: 2.2rem;
            text-align: center;
            color: #FFFFFF;
            margin-top: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.12);
        }
        .result-card-good {
            background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        }
        .result-card-average {
            background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        }
        .result-card-poor {
            background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        }
        .result-title {
            font-size: 2.3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .result-subtitle {
            font-size: 1.2rem;
            opacity: 0.95;
        }
        
        /* Metrics Styling */
        div[data-testid="stMetric"] {
            background-color: #FFFFFF !important;
            border-radius: 14px !important;
            padding: 1rem 1.2rem !important;
            border: 1px solid #E5E7EB !important;
            box-shadow: 0 3px 10px rgba(0,0,0,0.03) !important;
        }
        
        div[data-testid="stMetricLabel"] p {
            color: #6B7280 !important;
            font-weight: 500 !important;
        }
        
        div[data-testid="stMetricValue"] div {
            color: #1F2937 !important;
            font-weight: 700 !important;
        }
        </style>
        """
    )
