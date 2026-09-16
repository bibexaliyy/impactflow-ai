from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.text import slugify

from .forms import SignUpForm
from .models import Organization


class ImpactFlowLoginView(LoginView):
    template_name = "accounts/login.html"


class ImpactFlowLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


def signup(request):
    """
    Signup creates the user's Organization at the same time — this is
    the entry point for a new NGO/CSO onboarding onto the platform.
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            org_name = form.cleaned_data["organization_name"]
            org = Organization.objects.create(
                name=org_name,
                slug=slugify(org_name),
            )
            user = form.save(commit=False)
            user.organization = org
            user.role = "owner"
            user.save()
            login(request, user)
            return redirect("projects:list")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})
