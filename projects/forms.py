from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "project_title",
            "location",
            "project_date",
            "objectives",
            "activities",
            "participants",
            "outcomes",
            "challenges",
            "lessons",
            "success_story",
        ]
        widgets = {
            "project_date": forms.DateInput(attrs={"type": "date"}),
            "objectives": forms.Textarea(attrs={"rows": 3}),
            "activities": forms.Textarea(attrs={"rows": 4}),
            "participants": forms.Textarea(attrs={"rows": 2}),
            "outcomes": forms.Textarea(attrs={"rows": 3}),
            "challenges": forms.Textarea(attrs={"rows": 3}),
            "lessons": forms.Textarea(attrs={"rows": 3}),
            "success_story": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Applied here rather than per-widget above so every field
        # (including the plain CharField/DateField ones) gets the
        # same Tailwind styling with no repetition.
        base_classes = "w-full border border-gray-300 rounded px-3 py-2 text-sm"
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base_classes}".strip()
