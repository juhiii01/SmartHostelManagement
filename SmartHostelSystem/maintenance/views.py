from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Branch, Complaint, StaffProfile
from .forms import ComplaintForm, StatusForm

def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "home.html")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "form_page.html", {"form": form, "heading": "Student Registration", "button": "Create account"})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "form_page.html", {"form": form, "heading": "Login", "button": "Login"})

@login_required
def dashboard(request):
    complaints = Complaint.objects.select_related("branch", "student", "assigned_staff").order_by("-created_at")
    is_staff_user = request.user.is_staff or request.user.is_superuser
    if not is_staff_user:
        complaints = complaints.filter(student=request.user)
    else:
        profile = StaffProfile.objects.filter(user=request.user).select_related("branch").first()
        if not request.user.is_superuser and profile and profile.branch:
            complaints = complaints.filter(branch=profile.branch)
    tab = request.GET.get("status", "All")
    if tab in ["Pending", "In Progress", "Resolved"]:
        complaints = complaints.filter(status=tab)
    all_base = Complaint.objects.all()
    if not is_staff_user:
        all_base = all_base.filter(student=request.user)
    else:
        profile = StaffProfile.objects.filter(user=request.user).select_related("branch").first()
        if not request.user.is_superuser and profile and profile.branch:
            all_base = all_base.filter(branch=profile.branch)
    counts = {
        "total": all_base.count(),
        "pending": all_base.filter(status="Pending").count(),
        "progress": all_base.filter(status="In Progress").count(),
        "resolved": all_base.filter(status="Resolved").count(),
    }
    return render(request, "dashboard.html", {
        "complaints": complaints, "counts": counts, "tab": tab,
        "is_staff_user": is_staff_user,
    })

@login_required
def new_complaint(request):
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Only student accounts can submit complaints.")
        return redirect("dashboard")
    if request.method == "POST":
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user
            if complaint.location != "Hostel Room":
                complaint.room_number = ""
            complaint.save()
            messages.success(request, f"Complaint #{complaint.id} submitted successfully.")
            return redirect("dashboard")
    else:
        form = ComplaintForm()
    return render(request, "form_page.html", {"form": form, "heading": "Submit a Complaint", "button": "Submit Complaint", "multipart": True})

@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint.objects.select_related("branch", "student", "assigned_staff"), pk=pk)
    if not (request.user.is_staff or request.user.is_superuser) and complaint.student_id != request.user.id:
        messages.error(request, "You do not have permission to view this complaint.")
        return redirect("dashboard")
    status_form = None
    if request.user.is_staff or request.user.is_superuser:
        if request.method == "POST":
            status_form = StatusForm(request.POST, instance=complaint)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, "Complaint updated.")
                return redirect("complaint_detail", pk=complaint.pk)
        else:
            status_form = StatusForm(instance=complaint)
    return render(request, "complaint_detail.html", {"complaint": complaint, "status_form": status_form})

@login_required
def staff_portal(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(
            request,
            "Staff access only. Ask admin to enable staff access."
        )
        return redirect("dashboard")

    complaints = Complaint.objects.all().order_by("-created_at")

    pending_count = complaints.filter(status="Pending").count()
    in_progress_count = complaints.filter(status="In Progress").count()
    solved_count = complaints.filter(status="Solved").count()
    total_count = complaints.count()

    context = {
        "complaints": complaints,
        "pending_count": pending_count,
        "in_progress_count": in_progress_count,
        "solved_count": solved_count,
        "total_count": total_count,
    }

    return render(request, "staff_portal.html", context)