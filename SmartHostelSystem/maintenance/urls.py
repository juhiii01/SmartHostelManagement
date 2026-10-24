from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("complaint/new/", views.new_complaint, name="new_complaint"),
    path("complaint/<int:pk>/", views.complaint_detail, name="complaint_detail"),
    path("staff/", views.staff_portal, name="staff_portal"),
    path("staff-portal/", views.staff_portal, name="staff_portal"),
]
