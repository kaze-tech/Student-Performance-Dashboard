from __future__ import annotations

import math

import pandas as pd


def calculate_consistency(gpas: list[float]) -> float:
    """Lower semester variation means higher consistency."""
    mean_gpa = sum(gpas) / len(gpas)
    variance = sum((gpa - mean_gpa) ** 2 for gpa in gpas) / len(gpas)
    std_dev = math.sqrt(variance)
    return round(max(0.0, 10 - (std_dev * 4)), 2)


def calculate_risk_level(average_gpa: float, attendance_percentage: float, failures: int) -> str:
    """Apply the simple rule-based risk logic requested for the project."""
    if average_gpa < 5 or attendance_percentage < 65 or failures >= 3:
        return "High Risk"
    if 5 <= average_gpa <= 7 or 65 <= attendance_percentage <= 75:
        return "Medium Risk"
    return "Low Risk"


def build_student_dataset(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Merge source CSVs and compute the derived values shown in the detail page."""
    merged = (
        data["students"]
        .merge(data["marks"], on="student_id", how="left")
        .merge(data["behavior"], on="student_id", how="left")
    )

    semester_columns = ["sem1_gpa", "sem2_gpa", "sem3_gpa", "sem4_gpa", "sem5_gpa"]

    # Student images are mapped by row order from students.csv: first row -> pic_1.jpg, etc.
    merged["image_index"] = merged.index + 1

    # Derived academic values are calculated in code instead of being stored in CSV.
    merged["average_gpa"] = merged[semester_columns].mean(axis=1).round(2)
    merged["performance_change_rate"] = (merged["sem5_gpa"] - merged["sem1_gpa"]).round(2)
    merged["consistency_index"] = merged[semester_columns].apply(
        lambda row: calculate_consistency(row.tolist()),
        axis=1,
    )
    merged["risk_level"] = merged.apply(
        lambda row: calculate_risk_level(
            row["average_gpa"],
            row["attendance_percentage"],
            int(row["past_failures_count"]),
        ),
        axis=1,
    )
    return merged
