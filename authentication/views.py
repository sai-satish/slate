from django.contrib.auth import login as auth_login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import jwt
import datetime
import bcrypt


# User Registration with Role
def register(request):
    token = request.COOKIES.get('jwt')
    if token:
        return redirect("dashboard")
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if not name or not email or not password or not role:
            messages.error(request, "All fields are required.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken.")
            return redirect("register")

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        #creating user
        user = User(name=name, email=email, role=role, password=hashed_password)
        user.save()

        messages.success(request, f"Account created for {name} as {role}.")
        return redirect("login")

    return render(request, "register.html")

def login_redirect(request):
    return redirect('login')

def login(request):
    token = request.COOKIES.get('jwt')
    if token:
        return redirect("dashboard")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password").encode("utf-8")  # Encode password for bcrypt comparison


        try:
            user = User.objects.get(email=email)
            #print(f"User found: {user.email} - {user.role}")

            # Check the password using bcrypt
            if bcrypt.checkpw(password, user.password.encode("utf-8")):
                #print(f"Passwords match for user {email}")
                auth_login(request, user)

                # Create JWT payload
                payload = { 
                    'id': user.id, 
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60), 
                    'iat': datetime.datetime.utcnow() 
                } 

            
                token = jwt.encode(payload, 'secret', algorithm="HS256")
                response = redirect("dashboard")  # Redirect to the dashboard

                # Set the JWT token as a cookie
                response.set_cookie(key='jwt', value=token, httponly=True)
                return response

            else:
                print("Invalid credentials - passwords don't match.")
                messages.error(request, "Invalid credentials.")

        except User.DoesNotExist:
            print("User not found.")
            messages.error(request, "Invalid credentials.")

    return render(request, "login.html")

# User Logout
def logout_view(request):
    logout(request)
    response = redirect("login")
    response.delete_cookie("jwt")
    return response
