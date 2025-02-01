from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentEditForm
from authentication.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import ParentChild, SchoolStudent, StudentAchievement
from rest_framework.exceptions import AuthenticationFailed
import jwt


# Role-Based Dashboards
@login_required
def dashboard(request):

    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        #fetching from database
        user = User.objects.filter(id=payload['id']).first()
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    


    # Redirecting to dashboard based on Role
    if user.role == "school":
        return redirect("school_dashboard")
    elif user.role == "parent":
        return redirect("parent_dashboard")
    elif user.role == "student":
        return redirect("student_dashboard")

    # Default dashboard rendering
    return render(request, "dashboard.html")




@login_required
def student_dashboard(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    
    student = user
    if student.role != "student":
        return HttpResponse("<h2>You are not authorized for this route</h2>")


    parent = None
    school = None

    
    try:
        parent_relationship = ParentChild.objects.get(student=student)
        parent = parent_relationship.parent
    except ParentChild.DoesNotExist:
        parent = None

    try:
        school_relationship = SchoolStudent.objects.get(student=student)
        school = school_relationship.school
    except SchoolStudent.DoesNotExist:
        school = None

    return render(request, "student_dashboard.html", {
        "student": student,
        "parent": parent,
        "school": school
    })



@login_required
def parent_dashboard(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    
    if user.role != "parent":
        return HttpResponse("<h1> Unauthorized access </h1> <br> <a href='../../auth/logout'>Logout</a>")

    if request.method == "POST":
        email = request.POST.get("email")
        try:
            student = User.objects.get(email=email, role="student")
            if not ParentChild.objects.filter(parent=user, student=student).exists():
                ParentChild.objects.create(parent=user, student=student)
                messages.success(request, f"{student.name} has been added as your child.")
            else:
                messages.warning(request, f"{student.name} is already added.")
        except User.DoesNotExist:
            messages.error(request, "No student found with this email.")

    children = ParentChild.objects.filter(parent=user).select_related("student")
    return render(request, "parent_dashboard.html", {"children": children})


@login_required
def school_dashboard(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    
    if user.role != "school":
        return HttpResponse("<h1>Unauthorized access</h1><br><a href='../../auth/logout'>Logout</a>")

    if request.method == "POST":
        email = request.POST.get("email")
        try:
            student = User.objects.get(email=email, role="student")
            if not SchoolStudent.objects.filter(school=user, student=student).exists():
                SchoolStudent.objects.create(school=user, student=student)
                messages.success(request, f"{student.name} has been added to your school.")
            else:
                messages.warning(request, f"{student.name} is already added.")
        except User.DoesNotExist:
            messages.error(request, "No student found with this email.")

    students = SchoolStudent.objects.filter(school=user).select_related("student")
    return render(request, "school_dashboard.html", {"students": students})


@login_required
def search_student(request):
    
    if request.method == "GET":
        email = request.GET.get("email")
        if not email:
            return JsonResponse({"error": "No email provided"}, status=400)

        try:
            student = User.objects.get(email=email, role="student")
            return JsonResponse({"exists": True, "name": student.name, "email": student.email})
        except User.DoesNotExist:
            return JsonResponse({"exists": False})

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def add_child(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:        
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    
    if request.method == "POST":
        email = request.POST.get("email")
        
        if not email:
            return JsonResponse({"error": "No email provided"}, status=400)

        try:
            student = User.objects.get(email=email, role="student")
            if user.role != "parent":
                return JsonResponse({"error": "Unauthorized action"}, status=403)

            user.children.add(student)
            user.save()

            return JsonResponse({"success": f"{student.name} added as your child."})
        except User.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def student_achievements(request, student_id):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:        
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    if user.role=='student':
        return HttpResponse("<h1>You are unauthorized for this route</h1>")

    student_id = str(student_id).replace("-", "")
    student = get_object_or_404(User, student_id=student_id, role="student")
    
    parents = ParentChild.objects.filter(student=student).select_related("parent")
    school_relation = SchoolStudent.objects.filter(student=student).select_related("school").first()
    achievements = StudentAchievement.objects.filter(student=student)

    return render(request, "student_achievements.html", {
        "student": student,
        "parents": [rel.parent for rel in parents], 
        "school": school_relation.school if school_relation else None,
        "achievements": achievements
    })



@login_required
def edit_student(request, student_id):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:        
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    if user.role!='school':
        return HttpResponse("<h1>You are unauthorized for this route</h1>")
    
    
    # Convert the UUID string to a UUID object
    student_id = str(student_id).replace("-", "")
    student = get_object_or_404(User, student_id=student_id, role="student")

    if request.method == "POST":
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student details updated successfully!")
            return redirect("student_achievements", student_id=student.student_id)
    else:
        form = StudentEditForm(instance=student)

    return render(request, "edit_student.html", {"form": form, "student": student})

@login_required
def add_achievement(request, student_id):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:        
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    if user.role!='school':
        return HttpResponse("<h1>You are unauthorized for this route</h1>")
        
    student = get_object_or_404(User, student_id=student_id, role="student")
    
    # Fetch the list of schools to display in the dropdown
    schools = User.objects.filter(role="school")  # Adjust this based on how your school model is structured
    
    if request.method == "POST":
        achievement_name = request.POST["achievement_name"]
        school_id = request.POST["school_id"]
        
        achievement = StudentAchievement.objects.create(
            student=student,
            achievement_name=achievement_name,
            school_id=school_id  # Assuming `school_id` is a valid field for the achievement
        )
        return redirect("student_achievements", student_id=student_id)
    
    return render(request, "add_achievement.html", {"student": student, "schools": schools})


@login_required
def edit_achievement(request, achievement_id):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:        
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    if user.role!='school':
        return HttpResponse("<h1>You are unauthorized for this route</h1>")
    achievement = get_object_or_404(StudentAchievement, id=achievement_id)

    if request.method == "POST":
        achievement_name = request.POST["achievement_name"]
        achievement.achievement_name = achievement_name
        achievement.save()
        return redirect("student_achievements", student_id=achievement.student.student_id)
    
    return render(request, "edit_achievement.html", {"achievement": achievement})
