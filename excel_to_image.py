import os
import pythoncom
import win32com.client


UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "generated"
WORKBOOK_NAME = "monthly_report.xlsx"


def export_monthly_reports():
    pythoncom.CoInitialize()

    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    workbook_path = os.path.abspath(
        os.path.join(UPLOAD_FOLDER, WORKBOOK_NAME)
    )

    workbook = excel.Workbooks.Open(workbook_path)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Delete old images
    for file in os.listdir(OUTPUT_FOLDER):
        if file.lower().endswith(".png"):
            os.remove(os.path.join(OUTPUT_FOLDER, file))

    for sheet in workbook.Worksheets:

        name = sheet.Name.strip()

        if name.lower() == "residents":
            continue

        if "ongoing" in name.lower():
            continue

        if name.lower() == "total pending final":
            continue

        safe_name = (
            name.replace("/", "-")
                .replace("\\", "-")
                .replace(":", "")
        )

        image_path = os.path.abspath(
            os.path.join(
                OUTPUT_FOLDER,
                f"{safe_name}.png"
            )
        )

        sheet.Activate()

        sheet.Range(sheet.UsedRange.Address).CopyPicture(
            Appearance=1,
            Format=2
        )

        chart = workbook.Charts.Add()
        chart.Paste()

        chart.Export(image_path)

        chart.Delete()

    workbook.Close(False)
    excel.Quit()

    pythoncom.CoUninitialize()