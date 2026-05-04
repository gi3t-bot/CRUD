# 🗂️ TeamTask — Team Task Manager

A clean, full-stack Team Task Manager built with **Django REST Framework** (backend) and **Vanilla HTML/CSS/JS** (frontend). Supports role-based access, JWT authentication, project management, task tracking, and dark mode.

---

## ✨ Features

- **Authentication** — JWT-based login/signup, password hashing
- **Role-Based Access** — Admin (create/assign) vs Member (view/update own tasks)
- **Project Management** — Create projects, add team members
- **Task Management** — Create tasks, assign to members, set due dates and status
- **Dashboard** — Stats: total, completed, overdue, in-progress, assigned to me
- **Dark Mode** — Smooth toggle, persisted across sessions, no flicker

---

## 🛠️ Tech Stack

| Layer     | Technology                            |
|-----------|---------------------------------------|
| Backend   | Django 4.2 + Django REST Framework    |
| Auth      | JWT via `djangorestframework-simplejwt` |
| Database  | SQLite (dev) / PostgreSQL (prod)      |
| Frontend  | HTML5, CSS3 (Variables), Vanilla JS   |
| Deployment| Railway                               |

---

## 📁 Project Structure

```
etah/
├── backend/
│   ├── core/           # Django settings, URLs, WSGI
│   ├── users/          # Custom user model + auth
│   ├── projects/       # Project CRUD
│   ├── tasks/          # Task CRUD + dashboard stats
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── index.html      # Login / Signup
│   ├── dashboard.html  # Dashboard
│   ├── projects.html   # Projects
│   ├── tasks.html      # Tasks
│   ├── css/style.css   # Full design system
│   └── js/             # auth.js, dashboard.js, projects.js, tasks.js, api.js, utils.js
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Local Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd etah
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Python dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
# Copy the example file
cp ../.env.example .env
# Edit .env and set SECRET_KEY
```

### 5. Run migrations and start server
```bash
python manage.py migrate
python manage.py createsuperuser   # Create an admin account
python manage.py runserver
```

### 6. Open the frontend
Open `frontend/index.html` using **VS Code Live Server** (port 5500).

> Backend runs on `http://127.0.0.1:8000`  
> Frontend runs on `http://127.0.0.1:5500`

---

## 🌐 API Endpoints

| Method | Endpoint                  | Description              | Auth Required |
|--------|---------------------------|--------------------------|---------------|
| POST   | `/api/auth/login/`        | Login → returns JWT      | No            |
| POST   | `/api/users/register/`    | Create account           | No            |
| GET    | `/api/users/me/`          | Logged-in user profile   | Yes           |
| GET    | `/api/projects/`          | List user's projects     | Yes           |
| POST   | `/api/projects/`          | Create project (admin)   | Admin         |
| GET    | `/api/projects/<id>/`     | Project detail           | Yes           |
| PUT    | `/api/projects/<id>/`     | Update project (owner)   | Admin         |
| GET    | `/api/tasks/`             | List tasks               | Yes           |
| POST   | `/api/tasks/`             | Create task (admin)      | Admin         |
| PATCH  | `/api/tasks/<id>/`        | Update status (member)   | Yes           |
| DELETE | `/api/tasks/<id>/`        | Delete task (admin)      | Admin         |
| GET    | `/api/tasks/dashboard/`   | Dashboard stats          | Yes           |

---

## ☁️ Railway Deployment

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-url>
git push origin main
```

### 2. Create Railway project
- Go to [railway.app](https://railway.app)
- New Project → Deploy from GitHub → select your repo

### 3. Add PostgreSQL
- In Railway: `+ New` → `Database` → `PostgreSQL`
- Copy the `DATABASE_URL` from the database's Variables tab

### 4. Set environment variables in Railway
```
SECRET_KEY=<generate a strong key>
DEBUG=False
ALLOWED_HOSTS=<your-app>.railway.app
DATABASE_URL=<from Railway PostgreSQL>
CORS_ALLOWED_ORIGINS=https://<your-frontend-url>
```

### 5. Add Procfile (Railway uses this to start the app)
```
web: cd backend && python manage.py migrate && gunicorn core.wsgi
```
Install gunicorn: add `gunicorn` to `requirements.txt`

---

## 🔑 Default Test Accounts

After running `createsuperuser`, log in at `/admin` to manage users.
Or register via the signup page and set role via admin panel.

---

## 📝 License

MIT — built for educational purposes.
