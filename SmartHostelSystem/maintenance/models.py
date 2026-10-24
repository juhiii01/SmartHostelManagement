from django.db import models
from django.contrib.auth.models import User

class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.user.username} (staff)"

class Complaint(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
    ]
    LOCATION_CHOICES = [
        ("Hostel Room", "Hostel Room"),
        ("Canteen", "Canteen"),
        ("College Ground", "College Ground"),
        ("College Campus / Corridor", "College Campus / Corridor"),
        ("Classroom", "Classroom"),
        ("Washroom", "Washroom"),
        ("Library", "Library"),
        ("Hostel Common Area", "Hostel Common Area"),
        ("Other", "Other"),
    ]
    CATEGORY_CHOICES = [
        ("Electrical", "Electrical"),
        ("Plumbing / Water", "Plumbing / Water"),
        ("Cleaning", "Cleaning"),
        ("Furniture", "Furniture"),
        ("Internet / Wi-Fi", "Internet / Wi-Fi"),
        ("Canteen", "Canteen"),
        ("Other", "Other"),
    ]
    PRIORITY_CHOICES = [("Low", "Low"), ("Medium", "Medium"), ("High", "High"), ("Urgent", "Urgent")]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hostel_complaints")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    room_number = models.CharField(max_length=20, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="Medium")
    title = models.CharField(max_length=120)
    description = models.TextField()
    photo = models.ImageField(upload_to="complaints/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    assigned_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_complaints")
    staff_remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"#{self.id} - {self.title}"
