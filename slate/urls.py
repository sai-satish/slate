"""
URL configuration for slate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from achievements.views import student_achievements, edit_student,add_achievement, edit_achievement
from authentication.views import login_redirect


urlpatterns = [
    path('', login_redirect),
    path('auth/', include("authentication.urls")),
    path("dashboard/", include("achievements.urls")),
    path("student/achievements/<uuid:student_id>/", student_achievements, name="student_achievements"),
    path("student/edit/<uuid:student_id>/", edit_student, name="edit_student"),
    path('student/achievements/<uuid:student_id>/add/', add_achievement, name='add_achievement'),
    path('student/achievements/edit/<int:achievement_id>/', edit_achievement, name='edit_achievement'),
    path('admin/', admin.site.urls),
]
