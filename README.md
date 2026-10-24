# Taskflow: Project Management System

**Live Demo:** [https://taskflow-api-1t8g.onrender.com/](https://taskflow-api-1t8g.onrender.com/) Due to usage of free tier deployment web service, it may take a minute to load the website.

## Project Overview
Taskflow is a full-stack, role-based project management application designed to streamline team collaboration. It heavily leverages a robust backend API connected to a dynamic frontend interface. The system operates on a dual-role architecture:
*   **Managers:** Have full administrative control. They can create new projects, generate tasks, set deadlines, and assign these tasks to specific team members.
*   **Team Members:** Have focused, execution-based access. They can view tasks exclusively assigned to them and update their progress status (e.g., To Do -> In Progress -> Done).

## Salient Features
*   **Secure Authentication:** Complete Login and Sign-Up flows using secure cryptographic hashing.
*   **Role-Based Access Control (RBAC):** UI elements and backend API endpoints dynamically adapt based on whether the logged-in user is a Manager or a Team Member.
*   **Single-Page Dashboard:** A highly interactive frontend that fetches and submits data asynchronously without requiring page reloads.
*   **Cloud Deployment:** Fully deployed and hosted on Render with a persistent cloud database.

## Tech Stack Used
*   **Backend:** Python, Django, Django REST Framework (DRF)
*   **Database:** PostgreSQL (Production on Render) / SQLite (Local Development)
*   **Frontend:** HTML5, Vanilla JavaScript, Bootstrap (CSS)
*   **Security:** JSON Web Tokens (JWT) via `djangorestframework-simplejwt`
*   **Deployment:** Render

## Core Concepts Used

### 1. Django ORM (Object-Relational Mapping)
The project utilizes Django's ORM to interact with the PostgreSQL database using pure Python code. Complex relationships, such as Foreign Keys mapping `Tasks` to `Projects` and `Users` (for both `assigned_to` and `assigned_by`), are handled seamlessly without writing raw SQL.

### 2. Django REST Framework (DRF) & Serializing
DRF is the backbone of the API layer. **Serializers** (`ModelSerializer`) act as the critical bridge, translating complex Python database models into standard JSON format for the frontend to consume, and validating incoming JSON payloads before saving them to the database.

### 3. JWT Authentication & Security
Instead of traditional stateful session cookies, the backend uses **JSON Web Tokens (JWT)**. Upon login, the server issues an encrypted access token. The frontend includes this token in the HTTP `Authorization` header for all subsequent API requests. DRF's permission classes (like `IsAuthenticated`) intercept requests and instantly reject unauthorized users.

### 4. API Views & ViewSets
The backend utilizes DRF's `ModelViewSet` to automatically generate standard CRUD (Create, Read, Update, Delete) endpoints. Custom logic is injected via `get_queryset()` to ensure users only fetch data relevant to their specific role, securing data at the database query level.

### 5. Pagination
To ensure scalability and fast loading times, DRF's **PageNumberPagination** is implemented globally. Instead of returning hundreds of tasks at once, the API chunks the data, sending manageable subsets along with metadata for frontend handling.

## Project Structure

```text
Taskflow_Task_Manager/
|_ taskflow/                 # Core Django project settings
|  |_ __init__.py
|  |_ asgi.py
|  |_ settings.py            # Configured for PostgreSQL & Render
|  |_ urls.py
|  |_ wsgi.py
|_ api/                      # Main API application logic
|  |_ migrations/
|  |_ __init__.py
|  |_ admin.py
|  |_ apps.py
|  |_ models.py              # Database schema (User, Project, Task)
|  |_ serializers.py         # JSON serialization & validation logic
|  |_ urls.py                # API endpoint routing
|  |_ views.py               # ViewSets and RBAC business logic
|_ templates/                # Frontend UI
|  |_ index.html             # Main Single-Page Application (HTML + JS)
|_ manage.py                 # Django command-line utility
|_ requirements.txt          # Python dependencies (Gunicorn, DRF, psycopg2)
```
