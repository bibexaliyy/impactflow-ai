from django.conf import settings
from django.db import models


class Project(models.Model):
    """
    Raw structured input a user fills in about a field activity/project.
    This is what gets fed to the AI engine to generate a Report.
    """

    organization = models.ForeignKey(
        "accounts.Organization",
        on_delete=models.CASCADE,
        related_name="projects",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="projects_created",
    )

    project_title = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    project_date = models.DateField(null=True, blank=True)

    # Structured input fields — these map directly to what the AI
    # prompt uses to generate each report section.
    objectives = models.TextField(help_text="What was this project trying to achieve?")
    activities = models.TextField(help_text="What activities were carried out?")
    participants = models.TextField(
        help_text="Who was reached — numbers, demographics, groups."
    )
    outcomes = models.TextField(help_text="What changed as a result?")
    challenges = models.TextField(blank=True)
    lessons = models.TextField(blank=True)
    success_story = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.project_title
