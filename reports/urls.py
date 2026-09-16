from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("<int:pk>/download/docx/", views.download_docx, name="download_docx"),
    path("<int:pk>/download/pdf/", views.download_pdf, name="download_pdf"),
]
