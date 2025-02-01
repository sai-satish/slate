from django.urls import path
from .views import (
    dashboard,
    school_dashboard,
    parent_dashboard,
    student_dashboard,
)

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("school/", school_dashboard, name="school_dashboard"),
    path("parent/", parent_dashboard, name="parent_dashboard"),
    path("student/", student_dashboard, name="student_dashboard"),
]
