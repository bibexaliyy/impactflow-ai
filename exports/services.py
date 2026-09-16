"""
Export services for generated reports.

DOCX: built directly with python-docx — best tool for structured,
section-based Word documents.

PDF: rendered from the same HTML template used for the on-screen
report preview (via weasyprint), so the web view, the PDF, and the
DOCX all show identical content — one source of truth, three outputs.
"""

import io

from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from docx import Document
from docx.shared import Pt
from weasyprint import HTML


def export_report_to_docx(report) -> None:
    document = Document()

    title = document.add_heading(report.project.project_title, level=0)
    subtitle = document.add_paragraph(report.get_report_type_display())
    subtitle.runs[0].italic = True

    for label, content in report.sections():
        document.add_heading(label, level=1)
        paragraph = document.add_paragraph(content or "Not provided.")
        for run in paragraph.runs:
            run.font.size = Pt(11)

    buffer = io.BytesIO()
    document.save(buffer)
    buffer.seek(0)

    filename = f"{report.project.project_title}-{report.pk}.docx"
    report.docx_file.save(filename, ContentFile(buffer.read()), save=True)


def export_report_to_pdf(report) -> None:
    html_string = render_to_string("reports/_report_pdf.html", {"report": report})
    pdf_bytes = HTML(string=html_string).write_pdf()

    filename = f"{report.project.project_title}-{report.pk}.pdf"
    report.pdf_file.save(filename, ContentFile(pdf_bytes), save=True)
