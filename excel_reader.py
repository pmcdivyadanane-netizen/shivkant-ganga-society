import os
from datetime import datetime

REPORTS_FOLDER = os.path.join("static", "reports")


def _report_sort_key(name):
    """Parse 'Month YYYY' into a sortable date. Non-matching names sort last."""
    try:
        return datetime.strptime(name, "%B %Y")
    except ValueError:
        return datetime.min


def get_report_sheets():
    """Return all report images as report names."""

    if not os.path.exists(REPORTS_FOLDER):
        return []

    reports = []

    for file in os.listdir(REPORTS_FOLDER):

        if not file.lower().endswith(".png"):
            continue

        name = os.path.splitext(file)[0]

        reports.append(name)

    reports.sort(key=_report_sort_key, reverse=True)

    if "Total Pending Final" in reports:
        reports.remove("Total Pending Final")
        reports.insert(0, "Total Pending Final")

    return reports
