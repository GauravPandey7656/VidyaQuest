# 🏫 VidyaQuest — Gamified Learning Platform for Rural Education

**VidyaQuest** is a web-based gamified learning platform designed to make digital education more engaging and accessible for students in rural communities.

The platform combines **learning content, quizzes, progress tracking, XP, levels, badges, leaderboards, and teacher management tools** in a single application.

> Built as a capstone project using Flask, SQLite, HTML, CSS, and JavaScript.

---

## ✨ Features

### 👨‍🎓 Student Features

- 🔐 Student registration and login
- 📚 Browse subjects and lessons
- 📝 Interactive lesson quizzes
- 📊 Track learning progress
- ⭐ Earn XP by completing quizzes
- 🆙 Level-up system based on XP
- 🏆 Achievement badges
- 🔥 Learning streak tracking
- 🥇 Village leaderboard
- 📈 Recent learning activity
- 📜 Certificate functionality

### 👨‍🏫 Teacher Features

- 🔐 Teacher authentication
- 📊 Teacher dashboard
- 👥 View student information
- 📈 View student performance statistics
- 📊 Weekly score analytics
- 📚 Manage lessons
- ➕ Add new lessons
- ❓ Add quiz questions
- 👀 View teacher-created lessons

### 🎮 Gamification

| Achievement | Reward |
|---|---|
| Complete a quiz | XP based on performance |
| Score 100% | Perfect Score badge |
| Earn 500 XP | Scholar badge |
| Earn 1000 XP | Champion badge |
| Complete 10 lessons | Village Hero badge |
| Maintain a 7-day streak | Week Warrior badge |

**Level System:** Students level up based on accumulated XP, with a new level every 200 XP.

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- SQLite

### Frontend
- HTML5
- CSS3
- JavaScript
- Fetch API

### Development & Testing
- Git
- GitHub
- Pytest

---

## 📁 Project Structure

```text
VidyaQuest/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── PRESENTATION_SLIDES.md
│
├── database/
│   ├── placeholder.txt
│   └── vidyaquest.db
│
├── static/
│   ├── css/
│   │   ├── dashboard.css
│   │   ├── style.css
│   │   └── teacher.css
│   │
│   └── js/
│       ├── dashboard.js
│       ├── main.js
│       └── teacher.js
│
└── templates/
    ├── base.html
    ├── index.html
    ├── dashboard.html
    ├── teacher.html
    ├── subject.html
    ├── chapter.html
    ├── lesson.html
    ├── lesson_quiz.html
    ├── quiz.html
    ├── quiz_result.html
    ├── explorer.html
    └── certificate.html
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/GauravPandey7656/VidyaQuest.git
cd VidyaQuest
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open the application

Visit:

```text
http://localhost:5000
```

---

## 🔑 Demo Accounts

The application includes demo accounts for testing the student and teacher workflows.

| Role | Email | Password |
|---|---|---|
| Student | `student@demo.com` | `demo123` |
| Teacher | `teacher@demo.com` | `teacher123` |

> For production deployment, replace demo credentials and use secure password handling and environment-based configuration.

---

## 🔄 Application Flow

```text
                    ┌──────────────────┐
                    │   User visits /  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Login / Register │
                    └────────┬─────────┘
                             │
                       Flask Session
                             │
                  ┌──────────┴──────────┐
                  │                     │
                  ▼                     ▼
          ┌──────────────┐      ┌──────────────┐
          │   Student    │      │   Teacher    │
          │   Dashboard  │      │   Dashboard  │
          └──────┬───────┘      └──────┬───────┘
                 │                     │
                 ▼                     ▼
          Subjects & Lessons     Student Analytics
                 │                     │
                 ▼                     ▼
              Quizzes             Lesson Management
                 │                     │
                 ▼                     ▼
          Score + XP + Badges     Quiz Management
                 │
                 ▼
          Progress & Leaderboard
```

---

## 🧠 Student Learning Flow

1. Student logs into the platform.
2. The dashboard loads the student's XP, level, badges, rank, and progress.
3. The student selects a subject.
4. Available chapters and lessons are displayed.
5. The student studies a lesson.
6. The student attempts the associated quiz.
7. The quiz result is submitted to the Flask backend.
8. The score and progress are stored in SQLite.
9. XP and applicable badges are awarded.
10. The student's progress and leaderboard position are updated.

---

## 👨‍🏫 Teacher Workflow

Teachers can use the management dashboard to:

1. View student statistics.
2. Review student performance.
3. View weekly score information.
4. Create lessons.
5. Add quiz questions.
6. Manage educational content stored in the application database.

---

## 🗄️ Database

VidyaQuest uses **SQLite** for local data persistence.

Main database entities include:

| Table | Purpose |
|---|---|
| `users` | Student and teacher accounts, XP, levels, and streaks |
| `subjects` | Educational subjects |
| `lessons` | Lesson content and XP rewards |
| `quizzes` | Quiz questions and answer options |
| `user_progress` | Student lesson completion and scores |
| `badges` | Available achievement definitions |
| `user_badges` | Badges earned by students |

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/register` | Register a new user |
| POST | `/api/login` | Authenticate a user |
| GET | `/api/me` | Get current user information |
| GET | `/logout` | Log out |

### Student

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/subjects` | Get subjects and progress |
| GET | `/api/subjects/<id>/lessons` | Get lessons for a subject |
| GET | `/api/lessons/<id>/quiz` | Get quiz questions |
| POST | `/api/lessons/<id>/submit` | Submit quiz results |
| GET | `/api/leaderboard` | Get leaderboard |
| GET | `/api/activity` | Get recent activity |

### Teacher

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/teacher/stats` | Get dashboard statistics |
| GET | `/api/teacher/students` | Get student information |
| GET | `/api/teacher/lessons` | Get teacher lessons |
| POST | `/api/teacher/lessons` | Create a lesson |
| POST | `/api/teacher/quiz` | Create a quiz question |
| GET | `/api/teacher/weekly_scores` | Get weekly score data |

---

## 🧪 Testing

The project is structured to support automated testing with **Pytest**.

Run:

```bash
pytest
```

---

## 🔒 Security Notes

This project is intended as an educational/capstone application.

Before deploying it publicly in a production environment, additional security work should be performed, including:

- Secure secret-key configuration
- Environment variables for sensitive configuration
- Strong password hashing
- CSRF protection
- Production database configuration
- Input validation and sanitization
- Secure session configuration
- Production-grade deployment configuration

---

## 🚀 Future Improvements

Potential improvements include:

- 🌐 Multi-language learning support
- 📱 Improved mobile responsiveness
- 🤖 AI-assisted personalized learning
- 📊 More advanced learning analytics
- ☁️ Cloud database integration
- 🔔 Student and teacher notifications
- 🎥 Rich multimedia lessons
- 🏫 School-level administration
- 🌍 Deployment for real-world users

---

## 🎓 Project Purpose

VidyaQuest was developed to explore how **gamification and technology can make learning more engaging and accessible**, particularly for students who may have limited access to traditional educational resources.

The project demonstrates practical experience with:

- Full-stack web development
- Flask backend development
- REST-style API design
- SQLite database management
- Frontend development
- Authentication and sessions
- CRUD operations
- Data visualization
- Gamification logic
- Automated testing
- Git and GitHub

---

## 👨‍💻 Author

**Gaurav Pandey**

B.Tech — Computer Science & Engineering  
Cybersecurity Domain

GitHub: [@GauravPandey7656](https://github.com/GauravPandey7656)

---

## 📄 License

This project is available for educational and portfolio purposes.