from django.db import models


class Report(models.Model):
    """
    The AI-generated output. One Project can have multiple Reports
    over time (e.g. regenerated after edits to the project inputs).
    """

    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="reports"
    )

    REPORT_TYPE_CHOICES = [
        ("activity", "Activity Report"),
        ("donor", "Donor Report"),
        ("monitoring", "Monitoring Report"),
        ("completion", "Project Completion Report"),
    ]
    report_type = models.CharField(
        max_length=20, choices=REPORT_TYPE_CHOICES, default="donor"
    )

    # The 9 sections from the project brief
    executive_summary = models.TextField(blank=True)
    background = models.TextField(blank=True)
    objectives = models.TextField(blank=True)
    activities = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    lessons_learned = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    conclusion = models.TextField(blank=True)

    # Export tracking
    docx_file = models.FileField(upload_to="reports/docx/", null=True, blank=True)
    pdf_file = models.FileField(upload_to="reports/pdf/", null=True, blank=True)

    generation_seconds = models.FloatField(
        null=True, blank=True, help_text="How long generation took — feeds the <10min metric."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Report for {self.project.project_title} ({self.created_at:%Y-%m-%d})"

    SECTION_ORDER = [
        ("executive_summary", "Executive Summary"),
        ("background", "Background"),
        ("objectives", "Project Objectives"),
        ("activities", "Activities Implemented"),
        ("achievements", "Key Achievements"),
        ("challenges", "Challenges"),
        ("lessons_learned", "Lessons Learned"),
        ("recommendations", "Recommendations"),
        ("conclusion", "Conclusion"),
    ]

    def sections(self):
        """Ordered (label, content) pairs — used by templates and exporters."""
        return [(label, getattr(self, field)) for field, label in self.SECTION_ORDER]
