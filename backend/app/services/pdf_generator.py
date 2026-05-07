# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet
# from io import BytesIO


# def generate_samples_pdf(samples: list):
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer)

#     styles = getSampleStyleSheet()
#     elements = []

#     title = Paragraph("Samples Distributed Report", styles["Title"])
#     elements.append(title)
#     elements.append(Spacer(1, 12))

#     data = [["Medicine Name", "Sample Name", "Quantity"]]

#     for s in samples:
#         data.append([
#             s.get("medicine_name", ""),
#             s.get("sample_name", ""),
#             str(s.get("quantity", ""))
#         ])

#     table = Table(data)

#     table.setStyle(TableStyle([
#         ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
#         ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
#         ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
#         ("ALIGN", (0, 0), (-1, -1), "CENTER"),
#     ]))

#     elements.append(table)

#     doc.build(elements)

#     buffer.seek(0)
#     return buffer


from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def generate_samples_pdf(samples: list):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    elements = []


    title = Paragraph("Samples Distributed Report", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

# table data
    data = [["Medicine Name", "Sample Name", "Quantity"]]

    for s in samples or []:

        if not isinstance(s, dict):
            print("WARNING: skipping invalid sample:", s)
            continue

        data.append([
            s.get("medicine_name", ""),
            s.get("sample_name", ""),
            str(s.get("quantity", ""))
        ])

# table styling
    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ]))

    elements.append(table)

# create pdf
    doc.build(elements)

    buffer.seek(0)
    return buffer