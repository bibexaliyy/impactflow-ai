from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ai_engine.services import ReportGenerationError, generate_report_for_project
from reports.models import Report

from .forms import ProjectForm
from .models import Project


@login_required
def project_list(request):
    projects = Project.objects.filter(organization=request.user.organization)
    return render(request, "projects/list.html", {"projects": projects})


@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.organization = request.user.organization
            project.created_by = request.user
            project.save()
            return redirect("projects:detail", pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, "projects/form.html", {"form": form})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(
        Project, pk=pk, organization=request.user.organization
    )
    report = Report.objects.filter(project=project).first()
    return render(
        request, "projects/detail.html", {"project": project, "report": report}
    )


@login_required
def generate_report(request, pk):
    """
    Triggered from the project detail page (htmx post). Calls the AI
    engine, saves the Report, and returns the rendered report partial
    so it can be swapped into the page without a full reload.
    """
    project = get_object_or_404(
        Project, pk=pk, organization=request.user.organization
    )
    try:
        report = generate_report_for_project(project)
    except ReportGenerationError as exc:
        return render(
            request, "reports/_generation_error.html", {"error": str(exc)}
        )
    return render(request, "reports/_report_preview.html", {"report": report})
