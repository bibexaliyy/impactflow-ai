from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Organization, User


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "plan", "created_at")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "organization", "role", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Organization", {"fields": ("organization", "role")}),
    )
