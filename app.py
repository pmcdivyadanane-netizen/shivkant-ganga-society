import os
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.utils import secure_filename
from openpyxl import load_workbook

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

UPLOAD_FOLDER = "uploads"
WORKBOOK_NAME = "monthly_report.xlsx"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ===================================
# HOME
# ===================================

@app.route("/")
def home():
    return render_template("index.html")


# ===================================
# LOGIN
# ===================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if session.get("admin"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if (
            email == app.config["ADMIN_EMAIL"]
            and password == app.config["ADMIN_PASSWORD"]
        ):

            session["admin"] = True
            flash("Login Successful", "success")

            return redirect(url_for("dashboard"))

        flash("Invalid Email or Password", "danger")

    return render_template("login.html")


# ===================================
# DASHBOARD
# ===================================

@app.route("/dashboard")
def dashboard():

    if not session.get("admin"):
        return redirect(url_for("login"))

    workbook = None
    last_updated = None
    sheets = []

    workbook_path = os.path.join(
        UPLOAD_FOLDER,
        WORKBOOK_NAME
    )

    if os.path.exists(workbook_path):

        workbook = WORKBOOK_NAME

        modified_time = os.path.getmtime(workbook_path)

        last_updated = datetime.fromtimestamp(
            modified_time
        ).strftime("%d %B %Y %I:%M %p")

        wb = load_workbook(workbook_path)

        for sheet in wb.sheetnames:

            name = sheet.strip()

            if "Residents" in name:
                continue

            if "Ongoing" in name:
                continue

            sheets.append(name)

    return render_template(
        "dashboard.html",
        workbook=workbook,
        last_updated=last_updated,
        sheets=sheets
    )


# ===================================
# UPLOAD
# ===================================

@app.route("/upload", methods=["POST"])
def upload():

    if not session.get("admin"):
        return redirect(url_for("login"))

    if "excel_file" not in request.files:

        flash("Please select an Excel file.")

        return redirect(url_for("dashboard"))

    file = request.files["excel_file"]

    if file.filename == "":

        flash("Please select an Excel file.")

        return redirect(url_for("dashboard"))

    filename = secure_filename(WORKBOOK_NAME)

    save_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(save_path)

    flash("Workbook uploaded successfully.", "success")

    return redirect(url_for("dashboard"))


# ===================================
# LOGOUT
# ===================================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "success")

    return redirect(url_for("home"))


# ===================================
# START APP
# ===================================

if __name__ == "__main__":
    app.run(debug=True)