from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404

from exports.services import export_report_to_docx, export_report_to_pdf

from .models import Report


def _get_owned_report(request, pk):
    return get_object_or_404(
        Report, pk=pk, project__organization=request.user.organization
    )


@login_required
def download_docx(request, pk):
    report = _get_owned_report(request, pk)
    if not report.docx_file:
        export_report_to_docx(report)
    if not report.docx_file:
        raise Http404("Could not generate the Word document.")
    return FileResponse(
        report.docx_file.open("rb"),
        as_attachment=True,
        filename=f"{report.project.project_title}-report.docx",
    )


@login_required
def download_pdf(request, pk):
    report = _get_owned_report(request, pk)
    if not report.pdf_file:
        export_report_to_pdf(report)
    if not report.pdf_file:
        raise Http404("Could not generate the PDF.")
    return FileResponse(
        report.pdf_file.open("rb"),
        as_attachment=True,
        filename=f"{report.project.project_title}-report.pdf",
    )
