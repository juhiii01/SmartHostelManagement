
from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Branch, StaffProfile, Complaint


@admin.register(Branch)
class BranchAdmin(ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(StaffProfile)
class StaffProfileAdmin(ModelAdmin):
    list_display = ("user", "branch")
    list_filter = ("branch",)


@admin.register(Complaint)
class ComplaintAdmin(ModelAdmin):
    list_display = (
        "id",
        "title",
        "branch",
        "location",
        "student",
        "status",
        "priority",
        "created_at",
    )
    list_filter = (
        "branch",
        "status",
        "priority",
        "location",
        "category",
    )
    search_fields = (
        "title",
        "description",
        "student__username",
        "room_number",
    )
