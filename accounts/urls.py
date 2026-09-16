from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.ImpactFlowLoginView.as_view(), name="login"),
    path("logout/", views.ImpactFlowLogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
]
