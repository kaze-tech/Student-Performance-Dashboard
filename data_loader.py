from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st


APP_DIR = Path(__file__).parent


@st.cache_data
def load_data() -> dict[str, pd.DataFrame]:
    """Load the CSV files used by the dashboard."""
    return {
        "students": pd.read_csv(APP_DIR / "students.csv"),
        "marks": pd.read_csv(APP_DIR / "marks.csv"),
        "behavior": pd.read_csv(APP_DIR / "behavior.csv"),
        "attendance": pd.read_csv(APP_DIR / "attendance.csv"),
    }


def save_attendance_records(
    students: pd.DataFrame,
    class_name: str,
    attendance_date: date,
    attendance_map: dict[str, str],
) -> None:
    """Append one attendance record per student to attendance.csv."""
    new_rows = []
    for _, student in students.iterrows():
        new_rows.append(
            {
                "student_id": student["student_id"],
                "class_name": class_name,
                "date": attendance_date.isoformat(),
                "attendance_status": attendance_map[student["student_id"]],
            }
        )

    attendance_path = APP_DIR / "attendance.csv"
    current_attendance = pd.read_csv(attendance_path)
    updated_attendance = pd.concat([current_attendance, pd.DataFrame(new_rows)], ignore_index=True)
    updated_attendance.to_csv(attendance_path, index=False)
    load_data.clear()
