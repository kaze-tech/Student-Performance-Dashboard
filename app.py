from __future__ import annotations

import streamlit as st

from data_loader import load_data, save_attendance_records
from ui_helpers import (
    inject_styles,
    render_attendance_page,
    render_class_selection,
    render_home_page,
    render_student_detail,
    render_student_list,
)
from utils import build_student_dataset


st.set_page_config(page_title="Student Performance Dashboard", layout="wide")


def initialize_state() -> None:
    """Use session state to control page navigation inside one Streamlit file."""
    defaults = {
        "page": "home",
        "selected_class": None,
        "selected_student_id": None,
        "attendance_saved_message": "",
        "attendance_locked": False,
        "dark_mode": False,
        "theme_toggle_value": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def go_to(page: str, class_name: str | None = None, student_id: str | None = None) -> None:
    """Update the page target and rerun the app."""
    st.session_state.page = page
    if class_name is not None:
        st.session_state.selected_class = class_name
    if student_id is not None:
        st.session_state.selected_student_id = student_id
    st.rerun()


def reset_attendance_state() -> None:
    st.session_state.attendance_saved_message = ""
    st.session_state.attendance_locked = False


def open_attendance_classes() -> None:
    reset_attendance_state()
    go_to("attendance_classes")


def open_student_classes() -> None:
    reset_attendance_state()
    go_to("student_classes")


def back_to_classes(page: str) -> None:
    reset_attendance_state()
    go_to(page)


def handle_attendance_save(students, attendance_date) -> None:
    """Collect the selected attendance values and append them to the CSV file."""
    symbol_to_status = {"\u2713": "Present", "\u2717": "Absent"}
    attendance_map = {
        student["student_id"]: symbol_to_status[
            st.session_state[f"attendance_{student['student_id']}"]
        ]
        for _, student in students.iterrows()
    }
    save_attendance_records(
        students=students,
        class_name=st.session_state.selected_class,
        attendance_date=attendance_date,
        attendance_map=attendance_map,
    )
    st.session_state.attendance_saved_message = (
        f"Attendance saved for {attendance_date.isoformat()}. Attendance closed."
    )
    st.session_state.attendance_locked = True


def main() -> None:
    # i initialize state before styling so the CSS can read the active theme right away.
    initialize_state()
    inject_styles()

    data = load_data()
    student_dataset = build_student_dataset(data)

    # i keep this compact view for attendance because only roll number and name are needed there.
    class_students = student_dataset[["student_id", "roll_no", "full_name"]].copy()
    page = st.session_state.page

    if page == "home":
        render_home_page(
            students=student_dataset,
            on_attendance_click=open_attendance_classes,
            on_student_data_click=open_student_classes,
            on_select_student=lambda student_id: go_to("student_detail", student_id=student_id),
        )
    elif page == "attendance_classes":
        render_class_selection(
            title="Select Class",
            key_prefix="attendance_marking",
            on_back=lambda: go_to("home"),
            on_select_class=lambda class_name: go_to("attendance_marking", class_name=class_name),
            students=student_dataset,
        )
    elif page == "attendance_marking":
        render_attendance_page(
            selected_class=st.session_state.selected_class,
            students=class_students,
            saved_message=st.session_state.attendance_saved_message,
            is_locked=st.session_state.attendance_locked,
            on_back=lambda: back_to_classes("attendance_classes"),
            on_save=lambda attendance_date: handle_attendance_save(class_students, attendance_date),
        )
    elif page == "student_classes":
        render_class_selection(
            title="Select Class",
            key_prefix="student_list",
            on_back=lambda: go_to("home"),
            on_select_class=lambda class_name: go_to("student_list", class_name=class_name),
            students=student_dataset,
        )
    elif page == "student_list":
        # i pass the full dataset here so the search, status tags, and ranking stay read-only extras.
        render_student_list(
            selected_class=st.session_state.selected_class,
            students=student_dataset,
            on_back=lambda: go_to("student_classes"),
            on_select_student=lambda student_id: go_to("student_detail", student_id=student_id),
        )
    elif page == "student_detail":
        student_row = student_dataset[
            student_dataset["student_id"] == st.session_state.selected_student_id
        ]
        if student_row.empty:
            st.error("Selected student was not found.")
        else:
            render_student_detail(
                student=student_row.iloc[0],
                on_back=lambda: go_to("student_list"),
            )
    else:
        go_to("home")


if __name__ == "__main__":
    main()

