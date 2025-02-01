# 🎓 Student Management System (Django)

## 📌 Overview
This is a Django-based Student Management System that provides role-based access for students, parents, and schools. The system allows schools to manage student profiles, track achievements, and associate students with parents and institutions.

# 🚀 Features
🔹 Authentication & Role-Based Access:
User authentication with email login.
Roles: Student, Parent, School.
Schools can edit student details.

🔹 Parent & School Association:
Parents can add students to their account.
Schools can enroll students in their system.

🔹 Student Achievements:
Schools can add and edit student achievements.
Achievements are linked to students with a School ID.

🔹 Dashboard & UI:
Separate Student Dashboard, Parent Dashboard and School Dashboard.



# 🏗️ Technologies Used
- Django (Backend)
- MySQL (Database)
- Bootstrap 5 (Frontend)
- JWT Authentication
- Role-Based Access Control (RBAC)

🗂️ Project Structure

    📂 project_root/
    │-- 📂 authentication/          # User  authentication & role management  
    │-- 📂 achievements/            # Student achievements management  
    │-- 📂 templates/               # HTML templates  
        |-- add_achievement.html
        |-- dashboard.html
        |-- edit_achievement.html
        |-- edit_student.html
        |-- login.html
        |-- parent_dashboard.html
        |-- register.html
        |-- school_dashboard.html
        |-- student_achievements.html 
        |-- student_dashboard.html
    │-- 📜 manage.py                # Django entry point  
    │-- 📜 requirements.txt         # Dependencies  
    │-- 📜 .env                     # Environment variables  
    │-- 📜 README.md                # Documentation  

## 🔧 Setup Instructions

### 1️⃣ Clone the Repository
    > git clone https://github.com/sai-satish/slate.git 
    > cd slate  

### 2️⃣ Set Up Virtual Environment
    > python -m venv venv  
    > source venv/bin/activate   # On Windows: venv\Scripts\activate  

### 3️⃣ Install Dependencies
    pip install -r requirements.txt  

### 4️⃣ Configure Environment Variables (.env)

Create a .env file in the project root and add:

    DB_NAME=your_db_name  
    DB_USER=your_db_user  
    DB_PASSWORD=your_db_password  
    DB_HOST=your_db_host  
    DB_PORT=your_db_port  
 

### 5️⃣ Apply Migrations & Run Server
    > python manage.py makemigrations
    > python manage.py migrate  
    > python manage.py runserver  

### 6️⃣ Access the App
    Visit: http://127.0.0.1:8000/

📜 API Endpoints
| Endpoint                                    | Method | Description                        |
|---------------------------------------------|--------|------------------------------------|
| /auth/login/                                | POST   | User login                         |
| /auth/register/                               | GET    | User logout                        |
| /dashboard/                                 | GET    | Parent/School/student Dashboard auto redirect            |
| /student/achievements/<uuid:student_id>/     | GET    | View student achievements          |
| /student/achievements/<uuid:student_id>/add/ | POST   | Add achievement (School only)      |
| /student/achievements/edit/<int:achievement_id>/ | GET | Edit achievement                   |


Pull requests are welcome! Please follow best practices and submit issues if you encounter any problems.