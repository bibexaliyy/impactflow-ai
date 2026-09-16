from django.contrib.auth.models import AbstractUser
from django.db import models


class Organization(models.Model):
    """
    One row per NGO/CSO/CBO customer.
    This is the multi-tenancy boundary: every Project and Report
    belongs to an Organization, and users only see data scoped to
    their own org.
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Plan/billing fields — left simple now, wire up Stripe later
    # without touching the rest of the schema.
    plan = models.CharField(
        max_length=20,
        choices=[("free", "Free"), ("pro", "Pro"), ("enterprise", "Enterprise")],
        default="free",
    )

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Custom user model from Day 1 (swapping this in later is painful,
    doing it now costs nothing).
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="members",
        null=True,
        blank=True,
    )
    role = models.CharField(
        max_length=20,
        choices=[
            ("owner", "Owner"),
            ("admin", "Admin"),
            ("member", "Member"),
        ],
        default="member",
    )

    def __str__(self):
        return self.username
