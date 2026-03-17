from __future__ import annotations

import base64
import html
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st


APP_DIR = Path(__file__).parent
IMAGES_DIR = APP_DIR / "images"
CLASS_OPTIONS = [
    "III BSc AI and ML",
    "III BSc Data Science",
    "III BSc Computer Science",
    "III BCA",
    "III BSc IT",
]
TEACHER_NAME = "Dr. Priya Raman"
CALENDAR_ICON = "\U0001F4C5"
CHART_ICON = "\U0001F4CA"
STUDENTS_ICON = "\U0001F465"
ATTENDANCE_ICON = "\U0001F4CB"
GPA_ICON = "\U0001F393"
RISK_ICON = "\u26A0"
SEARCH_ICON = "\U0001F50D"


# i added these theme tokens so the whole app can switch looks without changing page flow.
def get_theme_tokens() -> dict[str, str]:
    if st.session_state.get("dark_mode", False):
        return {
            "app_bg": "radial-gradient(circle at top left, rgba(16, 185, 129, 0.18), transparent 24%), radial-gradient(circle at bottom right, rgba(59, 130, 246, 0.22), transparent 20%), linear-gradient(135deg, #0f172a 0%, #111827 42%, #1e293b 100%)",
            "surface": "rgba(15, 23, 42, 0.78)",
            "surface_strong": "rgba(15, 23, 42, 0.92)",
            "surface_soft": "rgba(30, 41, 59, 0.60)",
            "text": "#e2e8f0",
            "muted": "#94a3b8",
            "border": "rgba(148, 163, 184, 0.18)",
            "shadow": "0 22px 48px rgba(2, 6, 23, 0.34)",
            "button_bg": "rgba(15, 23, 42, 0.86)",
            "button_hover": "#34d399",
            "good_bg": "rgba(34, 197, 94, 0.16)",
            "good_text": "#86efac",
            "warn_bg": "rgba(249, 115, 22, 0.18)",
            "warn_text": "#fdba74",
            "danger_bg": "rgba(239, 68, 68, 0.20)",
            "danger_text": "#fca5a5",
            "accent": "#34d399",
            "accent_alt": "#38bdf8",
            "disabled_bg": "rgba(51, 65, 85, 0.70)",
            "disabled_text": "#94a3b8",
            "chart_track": "rgba(148, 163, 184, 0.16)",
        }

    return {
        "app_bg": "radial-gradient(circle at top left, rgba(245, 158, 11, 0.22), transparent 24%), radial-gradient(circle at bottom right, rgba(59, 130, 246, 0.16), transparent 18%), linear-gradient(135deg, #fff8ef 0%, #f8fbff 52%, #eef6f3 100%)",
        "surface": "rgba(255, 255, 255, 0.82)",
        "surface_strong": "rgba(255, 255, 255, 0.94)",
        "surface_soft": "rgba(255, 255, 255, 0.60)",
        "text": "#0f172a",
        "muted": "#5b6b7f",
        "border": "rgba(148, 163, 184, 0.22)",
        "shadow": "0 20px 42px rgba(15, 23, 42, 0.08)",
        "button_bg": "rgba(255, 255, 255, 0.94)",
        "button_hover": "#059669",
        "good_bg": "rgba(34, 197, 94, 0.14)",
        "good_text": "#166534",
        "warn_bg": "rgba(249, 115, 22, 0.16)",
        "warn_text": "#9a3412",
        "danger_bg": "rgba(239, 68, 68, 0.16)",
        "danger_text": "#991b1b",
        "accent": "#10b981",
        "accent_alt": "#2563eb",
        "disabled_bg": "rgba(226, 232, 240, 0.82)",
        "disabled_text": "#64748b",
        "chart_track": "rgba(148, 163, 184, 0.18)",
    }


def svg_to_data_uri(svg: str) -> str:
    return f"data:image/svg+xml;base64,{base64.b64encode(svg.encode('utf-8')).decode('utf-8')}"


def load_teacher_avatar() -> str:
    """Return a fallback inline SVG avatar when teacher.jpg is not present."""
    svg = """
    <svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96">
      <defs>
        <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#10b981"/>
          <stop offset="100%" stop-color="#2563eb"/>
        </linearGradient>
      </defs>
      <rect width="96" height="96" rx="48" fill="url(#g)"/>
      <circle cx="48" cy="35" r="17" fill="#fff7ed"/>
      <path d="M22 76c4-15 17-23 26-23s22 8 26 23" fill="#fff7ed"/>
    </svg>
    """
    return svg_to_data_uri(svg)


def load_student_placeholder() -> str:
    """Return a fallback inline SVG avatar when pic_N.jpg is missing."""
    svg = """
    <svg xmlns="http://www.w3.org/2000/svg" width="144" height="144" viewBox="0 0 144 144">
      <defs>
        <linearGradient id="studentGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#cbd5e1"/>
          <stop offset="100%" stop-color="#94a3b8"/>
        </linearGradient>
      </defs>
      <rect width="144" height="144" rx="72" fill="url(#studentGrad)"/>
      <circle cx="72" cy="54" r="24" fill="#f8fafc"/>
      <path d="M38 112c6-21 24-33 34-33s28 12 34 33" fill="#f8fafc"/>
    </svg>
    """
    return svg_to_data_uri(svg)


def get_image_data_uri(image_path: Path) -> str | None:
    """Convert a local image into a data URI so Streamlit can embed it safely in HTML."""
    if not image_path.exists() or not image_path.is_file():
        return None

    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }
    mime_type = mime_types.get(image_path.suffix.lower())
    if mime_type is None:
        return None

    encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def get_teacher_image_source() -> str:
    """Use images/teacher.jpg when available, otherwise fall back to the SVG avatar."""
    teacher_image = get_image_data_uri(IMAGES_DIR / "teacher.jpg")
    return teacher_image or load_teacher_avatar()


def get_student_image_source(image_index: int) -> str:
    """Map first student -> pic_1.jpg, second -> pic_2.jpg, and so on."""
    student_image = get_image_data_uri(IMAGES_DIR / f"pic_{int(image_index)}.jpg")
    return student_image or load_student_placeholder()


def inject_styles() -> None:
    """Add a polished theme layer with light and dark variants using CSS variables."""
    tokens = get_theme_tokens()
    st.markdown(
        f"""
        <style>
            :root {{
                --app-bg: {tokens['app_bg']};
                --surface: {tokens['surface']};
                --surface-strong: {tokens['surface_strong']};
                --surface-soft: {tokens['surface_soft']};
                --text: {tokens['text']};
                --muted: {tokens['muted']};
                --border: {tokens['border']};
                --shadow: {tokens['shadow']};
                --button-bg: {tokens['button_bg']};
                --button-hover: {tokens['button_hover']};
                --good-bg: {tokens['good_bg']};
                --good-text: {tokens['good_text']};
                --warn-bg: {tokens['warn_bg']};
                --warn-text: {tokens['warn_text']};
                --danger-bg: {tokens['danger_bg']};
                --danger-text: {tokens['danger_text']};
                --accent: {tokens['accent']};
                --accent-alt: {tokens['accent_alt']};
                --disabled-bg: {tokens['disabled_bg']};
                --disabled-text: {tokens['disabled_text']};
                --chart-track: {tokens['chart_track']};
            }}
            .stApp {{
                background: var(--app-bg);
                color: var(--text);
            }}
            .block-container {{
                padding-top: 3rem;
                padding-bottom: 2.5rem;
                max-width: 1180px;
            }}
            .teacher-shell,
            .panel-card,
            .metric-card,
            .detail-card,
            .summary-card,
            .analytics-card,
            .student-directory-card,
            .search-result-card,
            .class-card,
            .side-panel,
            .alert-item,
            .theme-switch-wrap,
            .attendance-row,
            .attendance-help {{
                background: var(--surface);
                border: 1px solid var(--border);
                box-shadow: var(--shadow);
                backdrop-filter: blur(14px);
            }}
            .teacher-shell {{
                display: flex;
                align-items: center;
                gap: 1rem;
                border-radius: 28px;
                padding: 1.25rem 1.35rem;
                margin-bottom: 1.35rem;
            }}
            .teacher-avatar {{
                width: 78px;
                height: 78px;
                object-fit: cover;
                border-radius: 50%;
                flex-shrink: 0;
                box-shadow: 0 18px 38px rgba(37, 99, 235, 0.18);
            }}
            .teacher-name {{
                font-size: 1.35rem;
                font-weight: 800;
                color: var(--text);
                margin-bottom: 0.25rem;
            }}
            .welcome-title {{
                font-size: 1.7rem;
                font-weight: 800;
                color: var(--text);
                margin-bottom: 0.2rem;
            }}
            .welcome-subtitle {{
                color: var(--muted);
                font-size: 0.98rem;
                line-height: 1.5;
                max-width: 34rem;
            }}
            .page-title {{
                font-size: 1.72rem;
                font-weight: 800;
                color: var(--text);
                margin-bottom: 0.2rem;
            }}
            .page-subtitle {{
                color: var(--muted);
                font-size: 0.96rem;
            }}
            .section-title {{
                font-size: 1.12rem;
                font-weight: 800;
                color: var(--text);
                margin: 0.35rem 0 0.3rem;
            }}
            .section-note {{
                color: var(--muted);
                font-size: 0.92rem;
                margin-bottom: 0.85rem;
            }}
            .section-gap {{
                margin-top: 1.4rem;
            }}
            .metric-card {{
                border-radius: 22px;
                padding: 1rem 1.05rem;
                min-height: 8rem;
                margin-bottom: 0.7rem;
            }}
            .metric-card.good {{
                border-color: rgba(34, 197, 94, 0.24);
            }}
            .metric-card.warn {{
                border-color: rgba(249, 115, 22, 0.24);
            }}
            .metric-card.danger {{
                border-color: rgba(239, 68, 68, 0.24);
            }}
            .metric-card.primary {{
                border-color: rgba(59, 130, 246, 0.24);
            }}
            .metric-icon {{
                font-size: 1.2rem;
                margin-bottom: 0.75rem;
            }}
            .summary-label,
            .detail-label,
            .metric-label {{
                font-size: 0.82rem;
                color: var(--muted);
                margin-bottom: 0.25rem;
            }}
            .metric-value,
            .summary-value {{
                font-size: 1.75rem;
                line-height: 1.15;
                font-weight: 800;
                color: var(--text);
            }}
            .metric-caption {{
                margin-top: 0.35rem;
                color: var(--muted);
                font-size: 0.84rem;
            }}
            .detail-card,
            .summary-card,
            .analytics-card,
            .panel-card,
            .student-directory-card,
            .search-result-card,
            .side-panel {{
                border-radius: 22px;
                padding: 1rem 1.1rem;
                margin-bottom: 0.8rem;
            }}
            .detail-value {{
                font-size: 1rem;
                font-weight: 600;
                color: var(--text);
            }}
            .risk-badge,
            .status-tag,
            .class-state {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                border-radius: 999px;
                padding: 0.35rem 0.8rem;
                font-size: 0.84rem;
                font-weight: 700;
            }}
            .risk-low,
            .tag-good {{
                background: var(--good-bg);
                color: var(--good-text);
            }}
            .risk-medium,
            .tag-warning {{
                background: var(--warn-bg);
                color: var(--warn-text);
            }}
            .risk-high,
            .tag-risk {{
                background: var(--danger-bg);
                color: var(--danger-text);
            }}
            .student-hero {{
                display: flex;
                align-items: center;
                gap: 1rem;
                background: var(--surface);
                border: 1px solid var(--border);
                border-radius: 24px;
                padding: 1rem 1.15rem;
                box-shadow: var(--shadow);
                margin-bottom: 1rem;
            }}
            .student-hero-avatar {{
                width: 84px;
                height: 84px;
                object-fit: cover;
                border-radius: 50%;
                box-shadow: 0 18px 35px rgba(15, 23, 42, 0.14);
                flex-shrink: 0;
            }}
            .student-hero-name {{
                font-size: 1.45rem;
                font-weight: 800;
                color: var(--text);
                margin-bottom: 0.18rem;
            }}
            .student-hero-meta {{
                color: var(--muted);
                font-size: 0.95rem;
                font-weight: 600;
            }}
            .ring-wrap {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 18rem;
                text-align: center;
            }}
            .ring-caption {{
                margin-top: 0.8rem;
                color: var(--text);
                font-size: 0.96rem;
                font-weight: 700;
            }}
            .ring-subtext {{
                color: var(--muted);
                font-size: 0.86rem;
                margin-top: 0.25rem;
            }}
            .chart-stack {{
                display: flex;
                flex-direction: column;
                gap: 0.85rem;
                margin-top: 0.4rem;
            }}
            .mini-bar-row {{
                display: grid;
                grid-template-columns: 7.2rem 1fr 2rem;
                gap: 0.85rem;
                align-items: center;
            }}
            .mini-bar-label {{
                color: var(--text);
                font-size: 0.92rem;
                font-weight: 700;
            }}
            .mini-bar-track {{
                width: 100%;
                height: 0.72rem;
                border-radius: 999px;
                background: var(--chart-track);
                overflow: hidden;
            }}
            .mini-bar-fill {{
                height: 100%;
                border-radius: 999px;
            }}
            .mini-bar-fill.low {{
                background: linear-gradient(90deg, #22c55e, #4ade80);
            }}
            .mini-bar-fill.medium {{
                background: linear-gradient(90deg, #fb923c, #f59e0b);
            }}
            .mini-bar-fill.high {{
                background: linear-gradient(90deg, #f87171, #ef4444);
            }}
            .mini-bar-value {{
                text-align: right;
                color: var(--muted);
                font-weight: 700;
                font-size: 0.88rem;
            }}
            .alert-item {{
                border-radius: 18px;
                padding: 0.95rem 1rem;
                margin-bottom: 0.7rem;
            }}
            .alert-head {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 0.7rem;
                margin-bottom: 0.3rem;
            }}
            .alert-name {{
                color: var(--text);
                font-size: 0.98rem;
                font-weight: 800;
            }}
            .alert-meta,
            .alert-reason {{
                color: var(--muted);
                font-size: 0.88rem;
                line-height: 1.45;
            }}
            .directory-head {{
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 0.8rem;
                margin-bottom: 0.4rem;
            }}
            .directory-name {{
                font-size: 1rem;
                font-weight: 800;
                color: var(--text);
                margin-bottom: 0.18rem;
            }}
            .directory-roll {{
                color: var(--muted);
                font-size: 0.88rem;
                font-weight: 600;
            }}
            .directory-grid {{
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 0.75rem;
                margin-top: 0.85rem;
            }}
            .directory-stat-label {{
                font-size: 0.75rem;
                color: var(--muted);
                margin-bottom: 0.1rem;
            }}
            .directory-stat-value {{
                font-size: 0.95rem;
                font-weight: 700;
                color: var(--text);
            }}
            .rank-chip {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-width: 3.3rem;
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.20), rgba(37, 99, 235, 0.20));
                border: 1px solid rgba(59, 130, 246, 0.18);
                color: var(--text);
                border-radius: 999px;
                padding: 0.35rem 0.7rem;
                font-size: 0.82rem;
                font-weight: 800;
            }}
            .theme-switch-card {{
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(37, 99, 235, 0.10));
                border: 1px solid rgba(16, 185, 129, 0.24);
                border-radius: 18px;
                padding: 0.8rem 0.9rem 0.6rem;
                margin-bottom: 0.45rem;
            }}
            .theme-switch-title {{
                color: var(--muted);
                font-size: 0.78rem;
                font-weight: 700;
                margin-bottom: 0.15rem;
                text-transform: uppercase;
                letter-spacing: 0.04em;
            }}
            .theme-switch-caption {{
                color: var(--text);
                font-size: 0.88rem;
                font-weight: 700;
                margin-top: 0.2rem;
            }}
            div[data-testid="stToggleSwitch"] {{
                margin-top: 0.05rem;
                margin-bottom: 0.25rem;
            }}
            div[data-testid="stToggleSwitch"] label {{
                gap: 0.45rem;
            }}
            div[data-testid="stToggleSwitch"] [data-testid="stWidgetLabel"] {{
                display: none;
            }}
            .class-card {{
                border-radius: 22px;
                padding: 1rem 1.1rem;
                margin-bottom: 0.85rem;
            }}
            .class-card.active {{
                border: 1px solid rgba(16, 185, 129, 0.48);
                box-shadow: 0 0 0 1px rgba(16, 185, 129, 0.10), 0 18px 42px rgba(16, 185, 129, 0.14);
            }}
            .class-card.disabled {{
                background: var(--disabled-bg);
                color: var(--disabled-text);
                border: 1px solid rgba(148, 163, 184, 0.20);
                opacity: 0.82;
            }}
            .class-name {{
                font-size: 1.02rem;
                font-weight: 800;
                color: var(--text);
                margin-bottom: 0.3rem;
            }}
            .class-card.disabled .class-name {{
                color: var(--disabled-text);
            }}
            .class-note {{
                color: var(--muted);
                font-size: 0.89rem;
                line-height: 1.45;
            }}
            .class-card.disabled .class-note {{
                color: var(--disabled-text);
            }}
            .side-panel-title {{
                font-size: 1rem;
                font-weight: 800;
                color: var(--text);
                margin-bottom: 0.2rem;
            }}
            .side-panel-note {{
                color: var(--muted);
                font-size: 0.88rem;
                margin-bottom: 0.9rem;
            }}
            .attendance-row {{
                border-radius: 18px;
                padding: 1rem 1rem 0.25rem;
                margin-bottom: 0.8rem;
            }}
            .student-line {{
                font-size: 1rem;
                font-weight: 700;
                color: var(--text);
                margin-bottom: 0.4rem;
            }}
            .attendance-help {{
                border-radius: 16px;
                padding: 0.85rem 1rem;
                margin: 0.75rem 0 1rem;
                color: var(--text);
                font-size: 0.95rem;
            }}
            .empty-state {{
                color: var(--muted);
                font-size: 0.92rem;
                padding: 0.2rem 0 0.1rem;
            }}
            div[data-testid="stButton"] > button {{
                border-radius: 18px;
                border: 1px solid var(--border);
                background: var(--button-bg);
                color: var(--text);
                font-weight: 700;
                min-height: 3.4rem;
                box-shadow: var(--shadow);
            }}
            div[data-testid="stButton"] > button:hover {{
                border-color: var(--button-hover);
                color: var(--button-hover);
            }}
            .home-button div[data-testid="stButton"] > button {{
                min-height: 5rem;
                font-size: 1.15rem;
            }}
            div[data-testid="stTextInput"] input,
            div[data-testid="stDateInput"] input {{
                background: var(--surface-strong) !important;
                color: var(--text) !important;
                border-radius: 16px !important;
            }}
            div[data-testid="stTextInput"] label,
            div[data-testid="stToggleSwitch"] label,
            div[data-testid="stDateInput"] label,
            div[data-testid="stRadio"] > label p,
            div[data-testid="stAlertContainer"] p,
            div[data-testid="stMarkdownContainer"] p,
            div[data-testid="stMarkdownContainer"] li {{
                color: var(--text) !important;
            }}
            div[data-testid="stRadio"] div[role="radiogroup"] label {{
                background: var(--surface-strong);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 0.35rem 0.85rem;
                margin-right: 0.5rem;
            }}
            div[data-testid="stRadio"] div[role="radiogroup"] label p,
            div[data-testid="stRadio"] div[role="radiogroup"] label span,
            div[data-testid="stCheckbox"] label,
            div[data-testid="stToggleSwitch"] p {{
                color: var(--text) !important;
            }}
            @media (max-width: 900px) {{
                .directory-grid,
                .mini-bar-row {{
                    grid-template-columns: 1fr;
                }}
                .teacher-shell,
                .student-hero {{
                    align-items: flex-start;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _apply_theme_toggle() -> None:
    # i keep the real theme state in one place so page navigation does not reset it.
    st.session_state["dark_mode"] = bool(st.session_state.get("theme_toggle_value", False))


def render_theme_switcher() -> None:
    if "theme_toggle_value" not in st.session_state:
        st.session_state["theme_toggle_value"] = st.session_state.get("dark_mode", False)

    st.markdown(
        f"""
        <div class="theme-switch-card">
            <div class="theme-switch-title">Theme</div>
            <div class="theme-switch-caption">Current: {'Dark Mode' if st.session_state.get('dark_mode', False) else 'Light Mode'}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.toggle(
        "Theme Toggle",
        key="theme_toggle_value",
        help="Switch between light and dark gradient themes.",
        on_change=_apply_theme_toggle,
        label_visibility="collapsed",
    )


def render_teacher_header(show_welcome: bool = False) -> None:
    teacher_source = get_teacher_image_source()
    left_col, right_col = st.columns([5.2, 1.2])
    with left_col:
        welcome_markup = ""
        if show_welcome:
            welcome_markup = (
                f'<div class="welcome-title">Welcome back, {html.escape(TEACHER_NAME)}</div>'
                '<div class="welcome-subtitle">Manage attendance and monitor student performance</div>'
            )
        st.markdown(
            f"""
            <div class="teacher-shell">
                <img class="teacher-avatar" src="{teacher_source}" alt="Teacher profile"/>
                <div>
                    <div class="teacher-name">{html.escape(TEACHER_NAME)}</div>
                    {welcome_markup}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right_col:
        render_theme_switcher()


def render_page_header(title: str, on_back) -> None:
    left_col, center_col, right_col = st.columns([1, 4.6, 1.2])
    with left_col:
        if st.button("Back", width="stretch"):
            on_back()
    with center_col:
        st.markdown(
            f"""
            <div class="page-title">{html.escape(title)}</div>
            <div class="page-subtitle">Use the same app flow with a cleaner, theme-aware layout.</div>
            """,
            unsafe_allow_html=True,
        )
    with right_col:
        render_theme_switcher()


# i keep the dashboard summary in one helper so the home cards and side panels stay in sync.
def build_dashboard_summary(students: pd.DataFrame) -> dict[str, float]:
    high_risk_count = int((students["risk_level"] == "High Risk").sum())
    return {
        "total_students": int(len(students)),
        "average_attendance": float(students["attendance_percentage"].mean()),
        "average_gpa": float(students["average_gpa"].mean()),
        "high_risk_count": high_risk_count,
    }


def get_status_meta(risk_level: str) -> tuple[str, str]:
    mapping = {
        "Low Risk": ("Good", "tag-good"),
        "Medium Risk": ("Warning", "tag-warning"),
        "High Risk": ("At Risk", "tag-risk"),
    }
    return mapping.get(risk_level, ("Warning", "tag-warning"))


def get_risk_badge(risk_level: str) -> str:
    risk_class = {
        "Low Risk": "risk-low",
        "Medium Risk": "risk-medium",
        "High Risk": "risk-high",
    }.get(risk_level, "risk-medium")
    return f'<span class="risk-badge {risk_class}">{html.escape(risk_level)}</span>'


def render_metric_card(icon: str, label: str, value: str, caption: str, tone: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card {tone}">
            <div class="metric-icon">{icon}</div>
            <div class="metric-label">{html.escape(label)}</div>
            <div class="metric-value">{html.escape(value)}</div>
            <div class="metric-caption">{html.escape(caption)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# i added this reason builder so the at-risk panel explains why a student needs attention.
def build_risk_reason(student: pd.Series) -> str:
    reasons: list[str] = []
    attendance = float(student["attendance_percentage"])
    average_gpa = float(student["average_gpa"])
    failures = int(student["past_failures_count"])

    if attendance < 65:
        reasons.append(f"Low attendance ({attendance:.0f}%)")
    if average_gpa < 5:
        reasons.append(f"Low GPA ({average_gpa:.2f})")
    if failures >= 3:
        reasons.append(f"{failures} past failures")
    if not reasons and student["risk_level"] == "Medium Risk":
        reasons.append(f"Needs support: {attendance:.0f}% attendance and {average_gpa:.2f} GPA")
    if not reasons:
        reasons.append("Stable progress with room to improve")

    return ", ".join(reasons[:2])


def build_risk_distribution(students: pd.DataFrame) -> list[tuple[str, int, str]]:
    counts = students["risk_level"].value_counts()
    return [
        ("Low Risk", int(counts.get("Low Risk", 0)), "low"),
        ("Medium Risk", int(counts.get("Medium Risk", 0)), "medium"),
        ("High Risk", int(counts.get("High Risk", 0)), "high"),
    ]


def filter_students(students: pd.DataFrame, query: str) -> pd.DataFrame:
    if not query.strip():
        return students
    normalized = query.strip().lower()
    mask = students["full_name"].str.lower().str.contains(normalized, na=False) | students[
        "roll_no"
    ].str.lower().str.contains(normalized, na=False)
    return students[mask]


def render_risk_distribution_chart(students: pd.DataFrame) -> None:
    distribution = build_risk_distribution(students)
    maximum = max((count for _, count, _ in distribution), default=1) or 1
    rows = []
    for label, count, tone in distribution:
        width = 0 if count == 0 else max(8, round((count / maximum) * 100))
        rows.append(
            f"""
            <div class="mini-bar-row">
                <div class="mini-bar-label">{html.escape(label)}</div>
                <div class="mini-bar-track">
                    <div class="mini-bar-fill {tone}" style="width:{width}%;"></div>
                </div>
                <div class="mini-bar-value">{count}</div>
            </div>
            """
        )

    st.markdown(
        f"""
        <div class="analytics-card">
            <div class="section-title">Risk Visualization</div>
            <div class="section-note">A quick bar view of how students are distributed across risk bands.</div>
            <div class="chart-stack">
                {''.join(rows)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_at_risk_panel(students: pd.DataFrame) -> None:
    prioritized = students[students["risk_level"] == "High Risk"].copy()
    if prioritized.empty:
        prioritized = students.sort_values(
            ["attendance_percentage", "average_gpa", "past_failures_count"],
            ascending=[True, True, False],
        ).head(3)
    else:
        prioritized = prioritized.sort_values(
            ["attendance_percentage", "average_gpa", "past_failures_count"],
            ascending=[True, True, False],
        ).head(3)

    items = []
    for _, student in prioritized.iterrows():
        items.append(
            f"""
            <div class="alert-item">
                <div class="alert-head">
                    <div class="alert-name">{html.escape(student['full_name'])}</div>
                    {get_risk_badge(str(student['risk_level']))}
                </div>
                <div class="alert-meta">{html.escape(student['roll_no'])} | Attendance {float(student['attendance_percentage']):.0f}% | GPA {float(student['average_gpa']):.2f}</div>
                <div class="alert-reason">{html.escape(build_risk_reason(student))}</div>
            </div>
            """
        )

    st.markdown(
        f"""
        <div class="panel-card">
            <div class="section-title">Top 3 Students Needing Attention</div>
            <div class="section-note">These students are ranked by attendance pressure, GPA pressure, and past failures.</div>
            {''.join(items)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_search_results(students: pd.DataFrame, query: str, on_select_student) -> None:
    filtered = filter_students(students, query).sort_values(
        ["average_gpa", "attendance_percentage"],
        ascending=[False, False],
    )
    if not query.strip():
        st.markdown(
            '<div class="empty-state">Start typing a student name or roll number to see quick matches.</div>',
            unsafe_allow_html=True,
        )
        return
    if filtered.empty:
        st.markdown('<div class="empty-state">No students matched that search.</div>', unsafe_allow_html=True)
        return

    st.caption(f"{len(filtered)} match(es) found")
    for _, student in filtered.head(5).iterrows():
        status_label, status_class = get_status_meta(str(student["risk_level"]))
        info_col, action_col = st.columns([5, 1.2])
        with info_col:
            st.markdown(
                f"""
                <div class="search-result-card">
                    <div class="directory-head">
                        <div>
                            <div class="directory-name">{html.escape(student['full_name'])}</div>
                            <div class="directory-roll">{html.escape(student['roll_no'])}</div>
                        </div>
                        <span class="status-tag {status_class}">{html.escape(status_label)}</span>
                    </div>
                    <div class="directory-grid">
                        <div>
                            <div class="directory-stat-label">Average GPA</div>
                            <div class="directory-stat-value">{float(student['average_gpa']):.2f}</div>
                        </div>
                        <div>
                            <div class="directory-stat-label">Attendance</div>
                            <div class="directory-stat-value">{float(student['attendance_percentage']):.0f}%</div>
                        </div>
                        <div>
                            <div class="directory-stat-label">Reason</div>
                            <div class="directory-stat-value">{html.escape(build_risk_reason(student))}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with action_col:
            if st.button("Open Profile", key=f"home_search_{student['student_id']}", width="stretch"):
                on_select_student(student["student_id"])


def render_home_page(students: pd.DataFrame, on_attendance_click, on_student_data_click, on_select_student) -> None:
    render_teacher_header(show_welcome=True)

    button_col_one, button_col_two = st.columns(2)
    with button_col_one:
        st.markdown('<div class="home-button">', unsafe_allow_html=True)
        if st.button(f"{CALENDAR_ICON} Attendance", width="stretch"):
            on_attendance_click()
        st.markdown('</div>', unsafe_allow_html=True)
    with button_col_two:
        st.markdown('<div class="home-button">', unsafe_allow_html=True)
        if st.button(f"{CHART_ICON} Student Data", width="stretch"):
            on_student_data_click()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    summary = build_dashboard_summary(students)
    metric_cols = st.columns(4)
    with metric_cols[0]:
        render_metric_card(STUDENTS_ICON, "Total Students", str(summary["total_students"]), "Students currently tracked in this class.", "primary")
    with metric_cols[1]:
        render_metric_card(ATTENDANCE_ICON, "Average Attendance", f"{summary['average_attendance']:.0f}%", "Overall attendance health across the cohort.", "good")
    with metric_cols[2]:
        render_metric_card(GPA_ICON, "Average GPA", f"{summary['average_gpa']:.2f}", "Mean GPA from the semester-based performance data.", "primary")
    with metric_cols[3]:
        render_metric_card(RISK_ICON, "High Risk Students", str(summary["high_risk_count"]), "Students currently flagged as high risk.", "danger")

    insight_col, alert_col = st.columns([1.15, 1])
    with insight_col:
        render_risk_distribution_chart(students)
    with alert_col:
        render_at_risk_panel(students)

    section_header(
        "Quick Student Search",
        "Search by student name or roll number and jump to the existing detail view.",
    )
    query = st.text_input(
        "Search students",
        key="home_search_query",
        placeholder=f"{SEARCH_ICON} Search by name or roll number",
    )
    render_search_results(students, query, on_select_student)


def render_class_selection(
    title: str,
    key_prefix: str,
    on_back,
    on_select_class,
    students: pd.DataFrame,
) -> None:
    render_page_header(title, on_back)
    summary = build_dashboard_summary(students)

    class_col, side_col = st.columns([1.7, 1])
    with class_col:
        section_header(
            "Available Classes",
            "Only the first class is active right now, while the remaining rows stay visible but disabled.",
        )
        for index, class_name in enumerate(CLASS_OPTIONS):
            if index == 0:
                st.markdown(
                    f"""
                    <div class="class-card active">
                        <div class="alert-head">
                            <div class="class-name">{html.escape(class_name)}</div>
                            <span class="class-state tag-good">Active</span>
                        </div>
                        <div class="class-note">This class is ready for attendance entry and student analysis.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("Open Active Class", key=f"{key_prefix}_{index}", width="stretch"):
                    on_select_class(class_name)
            else:
                st.markdown(
                    f"""
                    <div class="class-card disabled">
                        <div class="alert-head">
                            <div class="class-name">{html.escape(class_name)}</div>
                            <span class="class-state">Disabled</span>
                        </div>
                        <div class="class-note">This row is visible for layout consistency and future class activation.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with side_col:
        st.markdown(
            """
            <div class="side-panel">
                <div class="side-panel-title">Class Snapshot</div>
                <div class="side-panel-note">This summary stays visible so the selection page feels informative, not empty.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_metric_card(STUDENTS_ICON, "Total Students", str(summary["total_students"]), "Students assigned to the active dataset.", "primary")
        render_metric_card(GPA_ICON, "Average GPA", f"{summary['average_gpa']:.2f}", "A quick academic health indicator for the class.", "good")
        render_metric_card(ATTENDANCE_ICON, "Average Attendance", f"{summary['average_attendance']:.0f}%", "Attendance consistency across the group.", "warn")


def render_attendance_page(
    selected_class: str,
    students: pd.DataFrame,
    saved_message: str,
    is_locked: bool,
    on_back,
    on_save,
) -> None:
    render_page_header(f"{selected_class} Attendance", on_back)

    attendance_date = st.date_input("Date", value=date.today(), disabled=is_locked)
    st.markdown(
        '<div class="attendance-help">Use <strong>\u2713</strong> for Present and <strong>\u2717</strong> for Absent for each student below.</div>',
        unsafe_allow_html=True,
    )

    if is_locked:
        st.warning("Attendance closed")

    for _, student in students.iterrows():
        st.markdown('<div class="attendance-row">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="student-line">{html.escape(str(student["roll_no"]))} - {html.escape(str(student["full_name"]))}</div>',
            unsafe_allow_html=True,
        )
        st.radio(
            label="Attendance Status",
            options=["\u2713", "\u2717"],
            horizontal=True,
            key=f"attendance_{student['student_id']}",
            label_visibility="visible",
            disabled=is_locked,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Save Attendance", width="stretch", type="primary", disabled=is_locked):
        on_save(attendance_date)

    if saved_message:
        st.success(saved_message)


def summary_card(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-label">{html.escape(label)}</div>
            <div class="summary-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def detail_card(label: str, value: object) -> None:
    st.markdown(
        f"""
        <div class="detail-card">
            <div class="detail-label">{html.escape(str(label))}</div>
            <div class="detail-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, note: str | None = None) -> None:
    st.markdown(f'<div class="section-title">{html.escape(title)}</div>', unsafe_allow_html=True)
    if note:
        st.markdown(f'<div class="section-note">{html.escape(note)}</div>', unsafe_allow_html=True)


def render_student_list(
    selected_class: str,
    students: pd.DataFrame,
    on_back,
    on_select_student,
) -> None:
    render_page_header(f"{selected_class} Students", on_back)
    section_header(
        "Student Directory",
        "Use the search bar to narrow results, and keep ranking on when you want GPA-based ordering.",
    )

    control_col, ranking_col = st.columns([4.5, 1.4])
    with control_col:
        query = st.text_input(
            "Search students",
            key="student_list_query",
            placeholder=f"{SEARCH_ICON} Search by name or roll number",
        )
    with ranking_col:
        show_ranking = st.toggle("Show Ranking", value=True, key="show_student_ranking")

    ranked_students = students.sort_values(
        ["average_gpa", "attendance_percentage", "full_name"],
        ascending=[False, False, True],
    ).reset_index(drop=True)
    ranked_students["rank"] = ranked_students.index + 1
    filtered_students = filter_students(ranked_students, query)

    if filtered_students.empty:
        st.markdown('<div class="empty-state">No student matches the current filter.</div>', unsafe_allow_html=True)
        return

    for _, student in filtered_students.iterrows():
        status_label, status_class = get_status_meta(str(student["risk_level"]))
        info_col, button_col = st.columns([5.2, 1.2])
        with info_col:
            rank_chip = (
                f'<span class="rank-chip">Rank #{int(student["rank"]):02d}</span>' if show_ranking else ""
            )
            st.markdown(
                f"""
                <div class="student-directory-card">
                    <div class="directory-head">
                        <div>
                            <div class="directory-name">{html.escape(student['full_name'])}</div>
                            <div class="directory-roll">{html.escape(student['roll_no'])}</div>
                        </div>
                        <div>
                            {rank_chip}
                            <span class="status-tag {status_class}">{html.escape(status_label)}</span>
                        </div>
                    </div>
                    <div class="directory-grid">
                        <div>
                            <div class="directory-stat-label">Average GPA</div>
                            <div class="directory-stat-value">{float(student['average_gpa']):.2f}</div>
                        </div>
                        <div>
                            <div class="directory-stat-label">Attendance</div>
                            <div class="directory-stat-value">{float(student['attendance_percentage']):.0f}%</div>
                        </div>
                        <div>
                            <div class="directory-stat-label">Support Reason</div>
                            <div class="directory-stat-value">{html.escape(build_risk_reason(student))}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with button_col:
            if st.button("View Profile", key=f"student_{student['student_id']}", width="stretch"):
                on_select_student(student["student_id"])


def render_attendance_indicator(attendance_percentage: float) -> None:
    percent = max(0.0, min(float(attendance_percentage), 100.0))
    radius = 52
    circumference = 2 * 3.14159 * radius
    offset = circumference * (1 - (percent / 100.0))
    tokens = get_theme_tokens()

    svg = f"""
    <svg width="180" height="180" viewBox="0 0 180 180" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="attendanceGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="{tokens['accent']}"/>
          <stop offset="100%" stop-color="{tokens['accent_alt']}"/>
        </linearGradient>
      </defs>
      <circle cx="90" cy="90" r="52" fill="none" stroke="rgba(148, 163, 184, 0.28)" stroke-width="12"/>
      <circle
        cx="90"
        cy="90"
        r="52"
        fill="none"
        stroke="url(#attendanceGradient)"
        stroke-width="12"
        stroke-linecap="round"
        stroke-dasharray="{circumference:.2f}"
        stroke-dashoffset="{offset:.2f}"
        transform="rotate(-90 90 90)"
      />
      <text x="90" y="88" text-anchor="middle" font-size="28" font-weight="800" fill="{tokens['text']}">{percent:.0f}%</text>
      <text x="90" y="110" text-anchor="middle" font-size="12" font-weight="600" fill="{tokens['muted']}">Attendance</text>
    </svg>
    """
    svg_data = svg_to_data_uri(svg)
    st.markdown(
        f"""
        <div class="analytics-card ring-wrap">
            <img src="{svg_data}" alt="Attendance indicator" />
            <div class="ring-caption">Attendance Percentage</div>
            <div class="ring-subtext">A quick visual of current attendance consistency.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_detail_section(title: str, details: list[tuple[str, object]], note: str | None = None) -> None:
    section_header(title, note)
    first_col, second_col = st.columns(2)
    for index, (label, value) in enumerate(details):
        with first_col if index % 2 == 0 else second_col:
            detail_card(label, value)


def render_student_detail(student: pd.Series, on_back) -> None:
    render_page_header("Student Detail", on_back)

    student_image = get_student_image_source(int(student.get("image_index", 1)))
    risk_badge = get_risk_badge(str(student["risk_level"]))

    st.markdown(
        f"""
        <div class="student-hero">
            <img class="student-hero-avatar" src="{student_image}" alt="Student profile"/>
            <div>
                <div class="student-hero-name">{html.escape(student['full_name'])}</div>
                <div class="student-hero-meta">{html.escape(student['roll_no'])} | {html.escape(student['department'])}</div>
                <div style="margin-top: 0.6rem;">{risk_badge}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    summary_columns = st.columns(4)
    with summary_columns[0]:
        summary_card("CGPA", f"{float(student['cgpa']):.2f}")
    with summary_columns[1]:
        summary_card("Attendance Percentage", f"{float(student['attendance_percentage']):.0f}%")
    with summary_columns[2]:
        summary_card("Average GPA", f"{float(student['average_gpa']):.2f}")
    with summary_columns[3]:
        summary_card("Risk Level", risk_badge)

    section_header(
        "Performance Overview",
        "Visual analytics for semester trend, attendance, and current academic standing.",
    )
    chart_col, attendance_col = st.columns([2.2, 1.1])

    semester_data = pd.DataFrame(
        {
            "Semester": ["Semester 1", "Semester 2", "Semester 3", "Semester 4", "Semester 5"],
            "GPA": [
                float(student["sem1_gpa"]),
                float(student["sem2_gpa"]),
                float(student["sem3_gpa"]),
                float(student["sem4_gpa"]),
                float(student["sem5_gpa"]),
            ],
        }
    ).set_index("Semester")

    with chart_col:
        st.markdown('<div class="detail-label">Semester-wise GPA Trend</div>', unsafe_allow_html=True)
        st.line_chart(semester_data, height=260, width="stretch")
    with attendance_col:
        render_attendance_indicator(float(student["attendance_percentage"]))

    personal_information = [
        ("Student ID", student["student_id"]),
        ("Roll Number", student["roll_no"]),
        ("Full Name", student["full_name"]),
        ("Gender", student["gender"]),
        ("Date of Birth", student["date_of_birth"]),
        ("Age", student["age"]),
        ("Department", student["department"]),
        ("Academic Batch", student["academic_batch"]),
        ("Current Semester", student["current_semester"]),
    ]

    academic_performance = [
        ("Semester 1 GPA", student["sem1_gpa"]),
        ("Semester 2 GPA", student["sem2_gpa"]),
        ("Semester 3 GPA", student["sem3_gpa"]),
        ("Semester 4 GPA", student["sem4_gpa"]),
        ("Semester 5 GPA", student["sem5_gpa"]),
        ("CGPA", student["cgpa"]),
        ("Average GPA", student["average_gpa"]),
        ("Performance Change Rate", student["performance_change_rate"]),
        ("Consistency Index", student["consistency_index"]),
        ("Assignment Submission Rate", f"{student['assignment_submission_rate']}%"),
    ]

    behavior_and_engagement = [
        ("Suspended", student["suspended"]),
        ("Interaction Level", student["interaction_level"]),
        ("Class Behavior", student["class_behavior"]),
        ("Peer Behavior", student["peer_behavior"]),
    ]

    risk_analysis = [
        ("Risk Level", risk_badge),
        ("Attendance Percentage", f"{student['attendance_percentage']}%"),
        ("Past Failures Count", student["past_failures_count"]),
    ]

    render_detail_section(
        "Personal Information",
        personal_information,
        "Student identity, class placement, and profile basics.",
    )
    render_detail_section(
        "Academic Performance",
        academic_performance,
        "Semester scores and derived academic indicators used in the dashboard.",
    )
    render_detail_section(
        "Behavior and Engagement",
        behavior_and_engagement,
        "Behavioral and interaction indicators from the behavior dataset.",
    )
    render_detail_section(
        "Risk Analysis",
        risk_analysis,
        "Rule-based academic risk is derived from GPA, attendance, and past failures.",
    )





