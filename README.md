# 🏫 VidyaQuest – Gamified Rural Learning Platform
## Full Stack: Flask + SQLite + HTML/CSS/JS

---

## 📁 Project Structure

```
vidyaquest/
├── app.py                  ← Flask backend (all routes + DB logic)
├── requirements.txt        ← Python dependencies
├── vidyaquest.db           ← SQLite database (auto-created on first run)
└── templates/
    ├── index.html          ← Login & Register page
    ├── dashboard.html      ← Student gamified dashboard
    └── teacher.html        ← Teacher management dashboard
```

---

## ⚙️ Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the server
```bash
python app.py
```

### 3. Open browser
```
http://localhost:5000
```

Database (`vidyaquest.db`) is **auto-created** with all tables and seed data on first run.

---

## 🔑 Demo Accounts

| Role    | Email                | Password    |
|---------|----------------------|-------------|
| Student | student@demo.com     | demo123     |
| Teacher | teacher@demo.com     | teacher123  |

---

## 🗺️ How It All Works

```
User visits /
    ↓
index.html (Login / Register)
    ↓ POST /api/login or /api/register
Flask checks SQLite → sets session
    ↓
Student → /dashboard  (dashboard.html)
Teacher → /teacher    (teacher.html)
```

### Student Dashboard Flow
1. Page loads → `fetch('/api/me')` → gets XP, level, badges, rank
2. `fetch('/api/subjects')` → shows subject cards with real progress %
3. Click a subject → `fetch('/api/subjects/:id/lessons')` → shows lessons list
4. Click a lesson → `fetch('/api/lessons/:id/quiz')` → shows quiz questions
5. Submit quiz → `POST /api/lessons/:id/submit` → saves score, awards XP & badges to DB

### Teacher Dashboard Flow
1. Page loads → `fetch('/api/teacher/stats')` → real student counts from DB
2. `fetch('/api/teacher/students')` → table of all students with avg scores
3. `fetch('/api/teacher/weekly_scores')` → chart data from DB
4. Add lesson → `POST /api/teacher/lessons` → saved to SQLite lessons table
5. Add quiz question → `POST /api/teacher/quiz` → saved to SQLite quizzes table

---

## 🗄️ Database Tables

| Table | Purpose |
|-------|---------|
| `users` | Students, teachers, admins (name, email, role, xp, level, streak) |
| `subjects` | Math, Science, English, SST, Hindi |
| `lessons` | Lesson title, content, XP reward, order |
| `quizzes` | Questions with 4 options and correct answer |
| `user_progress` | Which student completed which lesson + score |
| `badges` | Badge definitions (XP/lesson/streak requirements) |
| `user_badges` | Which badges each student has earned |

---

## 🎮 Gamification System

| Action | Result |
|--------|--------|
| Register | Account created, session started |
| Login | Streak updated automatically |
| Complete a quiz | Score saved, XP awarded proportionally |
| Score 100% | "Perfect Score" badge awarded |
| Earn 500 XP | "Scholar" badge awarded |
| Earn 1000 XP | "Champion" badge awarded |
| Complete 10 lessons | "Village Hero" badge awarded |
| 7-day streak | "Week Warrior" badge awarded |

**Level System:** Level = XP ÷ 200 (level up every 200 XP)

---

## 🔌 All API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/register` | None | Register new user |
| POST | `/api/login` | None | Login, get session |
| GET | `/api/me` | Session | Get current user data |
| GET | `/api/subjects` | Session | All subjects + progress |
| GET | `/api/subjects/<id>/lessons` | Session | Lessons for a subject |
| GET | `/api/lessons/<id>/quiz` | Session | Quiz questions (no answers) |
| POST | `/api/lessons/<id>/submit` | Session | Submit quiz, earn XP |
| GET | `/api/leaderboard` | Session | Village leaderboard |
| GET | `/api/activity` | Session | Recent activity feed |
| GET | `/api/teacher/stats` | Teacher | Dashboard stats |
| GET | `/api/teacher/students` | Teacher | All students data |
| GET | `/api/teacher/lessons` | Teacher | Teacher's lessons |
| POST | `/api/teacher/lessons` | Teacher | Add new lesson |
| POST | `/api/teacher/quiz` | Teacher | Add quiz question |
| GET | `/api/teacher/weekly_scores` | Teacher | Chart data |
| GET | `/logout` | Session | Logout |
