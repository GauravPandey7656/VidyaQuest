"""
VidyaQuest - Fully Integrated Flask + SQLite Application
=========================================================
Install:  pip install flask flask-jwt-extended werkzeug
Run:      python app.py
Open:     http://localhost:5000
"""

from flask import (
    Flask, request, jsonify, render_template,
    redirect, url_for, session, make_response
)
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os, datetime, functools

app = Flask(__name__)
app.secret_key = "vidyaquest-super-secret-2024"
DB_PATH = os.path.join(os.path.dirname(__file__), "vidyaquest.db")

# ─────────────────────────────────────────────────────
#  DATABASE HELPERS
# ─────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def query(sql, params=(), one=False):
    conn = get_db()
    cur  = conn.execute(sql, params)
    rv   = cur.fetchone() if one else cur.fetchall()
    conn.close()
    return rv

def mutate(sql, params=()):
    conn = get_db()
    cur  = conn.execute(sql, params)
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id

# ─────────────────────────────────────────────────────
#  DATABASE INIT & SEED
# ─────────────────────────────────────────────────────
def init_db():
    conn = get_db()
    c    = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        email       TEXT    UNIQUE NOT NULL,
        password    TEXT    NOT NULL,
        role        TEXT    NOT NULL DEFAULT 'student',
        village     TEXT    DEFAULT '',
        grade       TEXT    DEFAULT '',
        xp          INTEGER DEFAULT 0,
        level       INTEGER DEFAULT 1,
        streak      INTEGER DEFAULT 0,
        last_login  TEXT    DEFAULT '',
        created_at  TEXT    DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS subjects (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        icon        TEXT    DEFAULT '📚',
        description TEXT    DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS lessons (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id  INTEGER NOT NULL REFERENCES subjects(id),
        title       TEXT    NOT NULL,
        content     TEXT    DEFAULT '',
        xp_reward   INTEGER DEFAULT 20,
        order_num   INTEGER DEFAULT 1,
        created_by  INTEGER REFERENCES users(id),
        created_at  TEXT    DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS quizzes (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_id   INTEGER NOT NULL REFERENCES lessons(id),
        question    TEXT    NOT NULL,
        option_a    TEXT    NOT NULL,
        option_b    TEXT    NOT NULL,
        option_c    TEXT    NOT NULL,
        option_d    TEXT    NOT NULL,
        answer      TEXT    NOT NULL
    );

    CREATE TABLE IF NOT EXISTS user_progress (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id      INTEGER NOT NULL REFERENCES users(id),
        lesson_id    INTEGER NOT NULL REFERENCES lessons(id),
        completed    INTEGER DEFAULT 0,
        score        INTEGER DEFAULT 0,
        xp_earned    INTEGER DEFAULT 0,
        completed_at TEXT    DEFAULT '',
        UNIQUE(user_id, lesson_id)
    );

    CREATE TABLE IF NOT EXISTS badges (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT NOT NULL,
        description TEXT DEFAULT '',
        icon        TEXT DEFAULT '🏅',
        xp_required INTEGER DEFAULT 0,
        lessons_required INTEGER DEFAULT 0,
        streak_required  INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS user_badges (
        user_id   INTEGER NOT NULL REFERENCES users(id),
        badge_id  INTEGER NOT NULL REFERENCES badges(id),
        earned_at TEXT DEFAULT (datetime('now')),
        PRIMARY KEY(user_id, badge_id)
    );
    """)

    # ── Seed subjects ──
    c.executemany(
        "INSERT OR IGNORE INTO subjects (id,name,icon,description) VALUES (?,?,?,?)",
        [
            (1,"Mathematics","🔢","Numbers, algebra, geometry and more"),
            (2,"Science",    "🔬","Physics, chemistry, biology"),
            (3,"English",    "📖","Grammar, reading, writing"),
            (4,"Social Studies","🌍","History, geography, civics"),
            (5,"Hindi",     "🪔","Hindi language and literature"),
        ]
    )

    # ── Seed badges ──
    c.executemany(
        "INSERT OR IGNORE INTO badges (id,name,description,icon,xp_required,lessons_required,streak_required) VALUES (?,?,?,?,?,?,?)",
        [
            (1,"First Step",   "Complete your first lesson",   "🌟", 0,   1, 0),
            (2,"Scholar",      "Earn 500 XP",                  "🎓", 500, 0, 0),
            (3,"Champion",     "Earn 1000 XP",                 "🏆", 1000,0, 0),
            (4,"Week Warrior", "Maintain a 7-day streak",      "🔥", 0,   0, 7),
            (5,"Perfect Score","Score 100% on any quiz",       "💯", 0,   0, 0),
            (6,"Village Hero", "Complete 10 lessons",          "🌾", 0,  10, 0),
        ]
    )

    # ── Seed sample lessons ──
    c.executemany(
        "INSERT OR IGNORE INTO lessons (id,subject_id,title,content,xp_reward,order_num) VALUES (?,?,?,?,?,?)",
        [
            (1,1,"Introduction to Fractions",
             "A fraction represents a part of a whole. The top number is called the numerator and the bottom number is the denominator. For example, 3/4 means 3 parts out of 4 equal parts.",
             30,1),
            (2,1,"Adding Fractions",
             "To add fractions with the same denominator, simply add the numerators. Example: 1/4 + 2/4 = 3/4. For different denominators, first find the LCM.",
             30,2),
            (3,2,"Photosynthesis",
             "Photosynthesis is the process by which green plants make their own food using sunlight, water, and carbon dioxide. It happens in the chloroplasts of plant cells.",
             25,1),
            (4,2,"The Human Digestive System",
             "Digestion begins in the mouth and ends in the large intestine. Key organs include the stomach, small intestine, liver, and pancreas.",
             25,2),
            (5,3,"Parts of Speech",
             "The 8 parts of speech are: Noun, Pronoun, Verb, Adjective, Adverb, Preposition, Conjunction, and Interjection. Understanding these helps in constructing correct sentences.",
             20,1),
            (6,4,"Panchayati Raj System",
             "Panchayati Raj is India's system of rural self-governance. It has three tiers: Gram Panchayat (village), Panchayat Samiti (block), and Zila Parishad (district).",
             20,1),
            (7,5,"संज्ञा (Nouns in Hindi)",
             "संज्ञा वह शब्द है जो किसी व्यक्ति, वस्तु, स्थान या भाव का बोध कराती है। जैसे: राम, पुस्तक, दिल्ली, प्रेम।",
             20,1),
        ]
    )

    # ── Seed sample quiz questions ──
    c.executemany(
        "INSERT OR IGNORE INTO quizzes (id,lesson_id,question,option_a,option_b,option_c,option_d,answer) VALUES (?,?,?,?,?,?,?,?)",
        [
            (1,1,"What is the numerator in 3/4?","3","4","7","1","a"),
            (2,1,"What is 1/4 + 2/4?","1/4","2/4","3/4","4/4","c"),
            (3,1,"Which fraction is largest?","1/4","1/2","3/8","1/3","b"),
            (4,2,"What is 2/5 + 1/5?","3/10","3/5","2/5","1/5","b"),
            (5,3,"Where does photosynthesis take place?","Root","Stem","Leaf","Flower","c"),
            (6,3,"Which gas do plants take in for photosynthesis?","Oxygen","Nitrogen","CO₂","Hydrogen","c"),
            (7,4,"Where does digestion begin?","Stomach","Mouth","Intestine","Liver","b"),
            (8,5,"Which of these is a Noun?","Run","Beautiful","Delhi","Quickly","c"),
        ]
    )

    # ── Seed demo users ──
    demo_pass = generate_password_hash("demo123")
    teacher_pass = generate_password_hash("teacher123")
    c.executemany(
        "INSERT OR IGNORE INTO users (id,name,email,password,role,village,grade,xp,level,streak) VALUES (?,?,?,?,?,?,?,?,?,?)",
        [
            (1,"Ravi Kumar",    "student@demo.com", demo_pass,    "student","Rampur","Class 9",  340,2,5),
            (2,"Savita Sharma", "teacher@demo.com", teacher_pass, "teacher","Rampur","",         0,  1,0),
            (3,"Priya Sharma",  "priya@demo.com",   demo_pass,    "student","Rampur","Class 9",  680,4,12),
            (4,"Arjun Singh",   "arjun@demo.com",   demo_pass,    "student","Rampur","Class 9",  510,3,8),
        ]
    )

    # ── Seed some progress for demo student ──
    c.executemany(
        "INSERT OR IGNORE INTO user_progress (user_id,lesson_id,completed,score,xp_earned) VALUES (?,?,?,?,?)",
        [
            (1,1,1,80,24),(1,2,1,100,30),(1,3,1,70,17),(1,5,1,90,18),
            (3,1,1,100,30),(3,2,1,100,30),(3,3,1,90,22),(3,4,1,85,21),
            (3,5,1,100,20),(3,6,1,80,16),(4,1,1,75,22),(4,3,1,85,21),
        ]
    )

    # ── Seed badges for demo student ──
    c.executemany(
        "INSERT OR IGNORE INTO user_badges (user_id,badge_id) VALUES (?,?)",
        [(1,1),(1,5),(3,1),(3,2),(3,5),(3,6),(4,1)]
    )

    conn.commit()
    conn.close()
    print("✅ Database ready: vidyaquest.db")


# ─────────────────────────────────────────────────────
#  AUTH HELPERS
# ─────────────────────────────────────────────────────
def login_required(role=None):
    """Decorator: redirect to login if not authenticated."""
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("index"))
            if role and session.get("user_role") != role:
                return redirect(url_for("index"))
            return f(*args, **kwargs)
        return wrapped
    return decorator

def xp_to_level(xp):
    return max(1, xp // 200 + 1)

def level_title(level):
    titles = {1:"Beginner",2:"Explorer",3:"Scholar",4:"Champion",5:"Legend"}
    return titles.get(min(level, 5), "Legend")

def award_badges(user_id, conn):
    """Check and award any newly earned badges. Returns list of new badge names."""
    c   = conn.cursor()
    u   = c.execute("SELECT xp, streak FROM users WHERE id=?", (user_id,)).fetchone()
    lessons_done = c.execute(
        "SELECT COUNT(*) FROM user_progress WHERE user_id=? AND completed=1", (user_id,)
    ).fetchone()[0]

    all_badges = c.execute("SELECT * FROM badges").fetchall()
    new_badges = []

    for b in all_badges:
        already = c.execute(
            "SELECT 1 FROM user_badges WHERE user_id=? AND badge_id=?", (user_id, b["id"])
        ).fetchone()
        if already:
            continue
        earned = (
            (b["xp_required"]      > 0 and u["xp"]      >= b["xp_required"]) or
            (b["lessons_required"] > 0 and lessons_done >= b["lessons_required"]) or
            (b["streak_required"]  > 0 and u["streak"]  >= b["streak_required"])
        )
        if earned:
            c.execute("INSERT OR IGNORE INTO user_badges (user_id,badge_id) VALUES (?,?)", (user_id, b["id"]))
            new_badges.append({"name": b["name"], "icon": b["icon"]})

    conn.commit()
    return new_badges


# ─────────────────────────────────────────────────────
#  PAGE ROUTES
# ─────────────────────────────────────────────────────
@app.route("/")
def index():
    if "user_id" in session:
        if session.get("user_role") == "teacher":
            return redirect(url_for("teacher_dashboard"))
        return redirect(url_for("student_dashboard"))
    return render_template("index.html")

@app.route("/dashboard")
@login_required()
def student_dashboard():
    if session.get("user_role") == "teacher":
        return redirect(url_for("teacher_dashboard"))
    return render_template("dashboard.html")

@app.route("/teacher")
@login_required(role="teacher")
def teacher_dashboard():
    return render_template("teacher.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ─────────────────────────────────────────────────────
#  AUTH API
# ─────────────────────────────────────────────────────
@app.route("/api/register", methods=["POST"])
def api_register():
    d = request.json or {}
    name    = d.get("name","").strip()
    email   = d.get("email","").strip().lower()
    pw      = d.get("password","")
    role    = d.get("role","student")
    village = d.get("village","").strip()
    grade   = d.get("grade","").strip()

    if not all([name, email, pw]):
        return jsonify(success=False, message="Name, email and password are required"), 400

    conn = get_db()
    try:
        uid = conn.execute(
            "INSERT INTO users (name,email,password,role,village,grade) VALUES (?,?,?,?,?,?)",
            (name, email, generate_password_hash(pw), role, village, grade)
        ).lastrowid
        conn.commit()
        session["user_id"]   = uid
        session["user_role"] = role
        session["user_name"] = name
        return jsonify(
            success=True,
            message=f"Welcome to VidyaQuest, {name}! 🎉",
            redirect="/teacher" if role == "teacher" else "/dashboard"
        ), 201
    except sqlite3.IntegrityError:
        return jsonify(success=False, message="Email already registered!"), 409
    finally:
        conn.close()


@app.route("/api/login", methods=["POST"])
def api_login():
    d     = request.json or {}
    email = d.get("email","").strip().lower()
    pw    = d.get("password","")

    if not email or not pw:
        return jsonify(success=False, message="Email and password required"), 400

    user = query("SELECT * FROM users WHERE email=?", (email,), one=True)
    if not user or not check_password_hash(user["password"], pw):
        return jsonify(success=False, message="Invalid email or password"), 401

    # Update streak
    today = datetime.date.today().isoformat()
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    streak = user["streak"]
    if user["last_login"] == yesterday:
        streak += 1
    elif user["last_login"] != today:
        streak = 1

    mutate("UPDATE users SET last_login=?, streak=?, level=? WHERE id=?",
           (today, streak, xp_to_level(user["xp"]), user["id"]))

    session["user_id"]   = user["id"]
    session["user_role"] = user["role"]
    session["user_name"] = user["name"]

    return jsonify(
        success=True,
        message=f"Welcome back, {user['name']}! 🔥 {streak}-day streak!",
        redirect="/teacher" if user["role"] == "teacher" else "/dashboard"
    )


# ─────────────────────────────────────────────────────
#  STUDENT API
# ─────────────────────────────────────────────────────
@app.route("/api/me")
def api_me():
    if "user_id" not in session:
        return jsonify(success=False, message="Not logged in"), 401
    uid  = session["user_id"]
    user = query("SELECT id,name,email,role,village,grade,xp,level,streak FROM users WHERE id=?", (uid,), one=True)
    if not user:
        return jsonify(success=False), 404

    badges = query("""
        SELECT b.name, b.icon FROM user_badges ub
        JOIN badges b ON ub.badge_id=b.id WHERE ub.user_id=?
    """, (uid,))

    lessons_done = query(
        "SELECT COUNT(*) as c FROM user_progress WHERE user_id=? AND completed=1", (uid,), one=True
    )["c"]

    rank = query("""
        SELECT COUNT(*)+1 as r FROM users
        WHERE role='student' AND village=? AND xp>?
    """, (user["village"], user["xp"]), one=True)["r"]

    xp        = user["xp"]
    lvl       = xp_to_level(xp)
    xp_in_lvl = xp % 200
    xp_pct    = round((xp_in_lvl / 200) * 100)

    return jsonify(
        success=True,
        user=dict(user),
        badges=[dict(b) for b in badges],
        lessons_done=lessons_done,
        rank=rank,
        xp_pct=xp_pct,
        xp_in_level=xp_in_lvl,
        level_title=level_title(lvl)
    )


@app.route("/api/subjects")
def api_subjects():
    if "user_id" not in session:
        return jsonify(success=False), 401
    uid  = session["user_id"]
    rows = query("SELECT * FROM subjects ORDER BY id")
    result = []
    for s in rows:
        total   = query("SELECT COUNT(*) as c FROM lessons WHERE subject_id=?", (s["id"],), one=True)["c"]
        done    = query("""
            SELECT COUNT(*) as c FROM user_progress up
            JOIN lessons l ON up.lesson_id=l.id
            WHERE l.subject_id=? AND up.user_id=? AND up.completed=1
        """, (s["id"], uid), one=True)["c"]
        pct = round((done/total)*100) if total else 0
        result.append({**dict(s), "total_lessons": total, "done_lessons": done, "pct": pct})
    return jsonify(success=True, subjects=result)


@app.route("/api/subjects/<int:sid>/lessons")
def api_lessons(sid):
    if "user_id" not in session:
        return jsonify(success=False), 401
    uid  = session["user_id"]
    rows = query("""
        SELECT l.*, COALESCE(up.completed,0) as completed,
               COALESCE(up.score,0) as score,
               COALESCE(up.xp_earned,0) as xp_earned
        FROM lessons l
        LEFT JOIN user_progress up ON l.id=up.lesson_id AND up.user_id=?
        WHERE l.subject_id=? ORDER BY l.order_num
    """, (uid, sid))
    return jsonify(success=True, lessons=[dict(r) for r in rows])


@app.route("/api/lessons/<int:lid>/quiz")
def api_quiz(lid):
    if "user_id" not in session:
        return jsonify(success=False), 401
    rows = query("SELECT * FROM quizzes WHERE lesson_id=?", (lid,))
    # Don't send the answer to the frontend
    qs = []
    for r in rows:
        qs.append({
            "id": r["id"], "question": r["question"],
            "options": [r["option_a"], r["option_b"], r["option_c"], r["option_d"]]
        })
    lesson = query("SELECT * FROM lessons WHERE id=?", (lid,), one=True)
    return jsonify(success=True, questions=qs, lesson=dict(lesson) if lesson else {})


@app.route("/api/lessons/<int:lid>/submit", methods=["POST"])
def api_submit(lid):
    if "user_id" not in session:
        return jsonify(success=False), 401
    uid     = session["user_id"]
    answers = request.json.get("answers", {})  # {"qid": "a/b/c/d"}

    questions = query("SELECT * FROM quizzes WHERE lesson_id=?", (lid,))
    if not questions:
        return jsonify(success=False, message="No quiz for this lesson"), 404

    correct = sum(1 for q in questions if answers.get(str(q["id"])) == q["answer"])
    total   = len(questions)
    score   = round((correct / total) * 100)

    lesson    = query("SELECT * FROM lessons WHERE id=?", (lid,), one=True)
    xp_earned = round((lesson["xp_reward"] if lesson else 20) * (score / 100))

    # Check perfect score badge
    conn = get_db()
    if score == 100:
        perfect_badge = conn.execute("SELECT id FROM badges WHERE name='Perfect Score'").fetchone()
        if perfect_badge:
            conn.execute("INSERT OR IGNORE INTO user_badges (user_id,badge_id) VALUES (?,?)",
                         (uid, perfect_badge["id"]))

    # Upsert progress
    conn.execute("""
        INSERT INTO user_progress (user_id,lesson_id,completed,score,xp_earned,completed_at)
        VALUES (?,?,1,?,?,datetime('now'))
        ON CONFLICT(user_id,lesson_id) DO UPDATE SET
            completed=1,
            score=MAX(score, excluded.score),
            xp_earned=MAX(xp_earned, excluded.xp_earned),
            completed_at=excluded.completed_at
    """, (uid, lid, score, xp_earned))

    # Award XP
    conn.execute("UPDATE users SET xp=xp+?, level=? WHERE id=?",
                 (xp_earned, xp_to_level(
                     conn.execute("SELECT xp FROM users WHERE id=?", (uid,)).fetchone()["xp"] + xp_earned
                 ), uid))
    conn.commit()

    new_badges = award_badges(uid, conn)
    updated    = conn.execute("SELECT xp,level FROM users WHERE id=?", (uid,)).fetchone()
    conn.close()

    return jsonify(
        success=True,
        score=score, correct=correct, total=total,
        xp_earned=xp_earned,
        total_xp=updated["xp"],
        level=updated["level"],
        new_badges=new_badges,
        message=f"Score: {score}%! +{xp_earned} XP 🎉" if score >= 50 else f"Score: {score}%. Keep trying! 💪"
    )


@app.route("/api/leaderboard")
def api_leaderboard():
    if "user_id" not in session:
        return jsonify(success=False), 401
    uid     = session["user_id"]
    village = query("SELECT village FROM users WHERE id=?", (uid,), one=True)["village"]
    rows    = query("""
        SELECT id, name, village, grade, xp, level, streak
        FROM users WHERE role='student' AND village=?
        ORDER BY xp DESC LIMIT 15
    """, (village,))
    board = []
    for i, r in enumerate(rows):
        board.append({**dict(r), "rank": i+1, "is_me": r["id"] == uid})
    return jsonify(success=True, leaderboard=board)


@app.route("/api/activity")
def api_activity():
    if "user_id" not in session:
        return jsonify(success=False), 401
    uid  = session["user_id"]
    rows = query("""
        SELECT up.completed_at, up.score, up.xp_earned,
               l.title as lesson_title,
               s.name as subject_name, s.icon as subject_icon
        FROM user_progress up
        JOIN lessons l ON up.lesson_id=l.id
        JOIN subjects s ON l.subject_id=s.id
        WHERE up.user_id=? AND up.completed=1
        ORDER BY up.completed_at DESC LIMIT 8
    """, (uid,))
    return jsonify(success=True, activity=[dict(r) for r in rows])


# ─────────────────────────────────────────────────────
#  TEACHER API
# ─────────────────────────────────────────────────────
@app.route("/api/teacher/stats")
@login_required(role="teacher")
def api_teacher_stats():
    uid  = session["user_id"]
    teacher = query("SELECT village FROM users WHERE id=?", (uid,), one=True)
    village = teacher["village"] if teacher else ""

    students     = query("SELECT COUNT(*) as c FROM users WHERE role='student' AND village=?", (village,), one=True)["c"]
    lessons      = query("SELECT COUNT(*) as c FROM lessons WHERE created_by=?", (uid,), one=True)["c"]
    at_risk      = query("""
        SELECT COUNT(DISTINCT u.id) as c FROM users u
        WHERE u.role='student' AND u.village=?
        AND (SELECT COALESCE(AVG(up.score),0) FROM user_progress up WHERE up.user_id=u.id AND up.completed=1) < 50
    """, (village,), one=True)["c"]
    avg_score_row = query("""
        SELECT ROUND(AVG(up.score),1) as avg FROM user_progress up
        JOIN users u ON up.user_id=u.id
        WHERE u.village=? AND up.completed=1
    """, (village,), one=True)
    avg_score = avg_score_row["avg"] or 0

    return jsonify(success=True, stats={
        "students": students, "lessons": lessons,
        "at_risk": at_risk, "avg_score": avg_score
    })


@app.route("/api/teacher/students")
@login_required(role="teacher")
def api_teacher_students():
    uid     = session["user_id"]
    village = query("SELECT village FROM users WHERE id=?", (uid,), one=True)["village"]

    students = query("""
        SELECT u.id, u.name, u.grade, u.xp, u.level, u.streak,
               COALESCE(AVG(up.score),0) as avg_score,
               COUNT(up.id) as lessons_done
        FROM users u
        LEFT JOIN user_progress up ON u.id=up.user_id AND up.completed=1
        WHERE u.role='student' AND u.village=?
        GROUP BY u.id ORDER BY u.xp DESC
    """, (village,))
    return jsonify(success=True, students=[dict(s) for s in students])


@app.route("/api/teacher/lessons")
@login_required(role="teacher")
def api_teacher_lessons():
    uid  = session["user_id"]
    rows = query("""
        SELECT l.*, s.name as subject_name, s.icon as subject_icon,
               COUNT(up.id) as completions
        FROM lessons l
        JOIN subjects s ON l.subject_id=s.id
        LEFT JOIN user_progress up ON l.id=up.lesson_id AND up.completed=1
        WHERE l.created_by=?
        GROUP BY l.id ORDER BY l.created_at DESC
    """, (uid,))
    return jsonify(success=True, lessons=[dict(r) for r in rows])


@app.route("/api/teacher/lessons", methods=["POST"])
@login_required(role="teacher")
def api_add_lesson():
    uid = session["user_id"]
    d   = request.json or {}
    subject_id = d.get("subject_id")
    title      = d.get("title","").strip()
    content    = d.get("content","").strip()
    xp_reward  = int(d.get("xp_reward", 20))
    order_num  = int(d.get("order_num", 1))

    if not title or not content or not subject_id:
        return jsonify(success=False, message="Subject, title and content are required"), 400

    lid = mutate(
        "INSERT INTO lessons (subject_id,title,content,xp_reward,order_num,created_by) VALUES (?,?,?,?,?,?)",
        (subject_id, title, content, xp_reward, order_num, uid)
    )
    return jsonify(success=True, message="Lesson published! ✅", lesson_id=lid), 201


@app.route("/api/teacher/quiz", methods=["POST"])
@login_required(role="teacher")
def api_add_quiz():
    d = request.json or {}
    lesson_id = d.get("lesson_id")
    question  = d.get("question","").strip()
    options   = d.get("options", [])
    answer    = d.get("answer","").strip().lower()

    if not all([lesson_id, question, len(options)==4, answer in ["a","b","c","d"]]):
        return jsonify(success=False, message="All fields required. Answer must be a/b/c/d"), 400

    qid = mutate(
        "INSERT INTO quizzes (lesson_id,question,option_a,option_b,option_c,option_d,answer) VALUES (?,?,?,?,?,?,?)",
        (lesson_id, question, options[0], options[1], options[2], options[3], answer)
    )
    return jsonify(success=True, message="Quiz question added! ✅", quiz_id=qid), 201


@app.route("/api/teacher/weekly_scores")
@login_required(role="teacher")
def api_weekly_scores():
    uid     = session["user_id"]
    village = query("SELECT village FROM users WHERE id=?", (uid,), one=True)["village"]
    result  = []
    for i in range(6, -1, -1):
        day = (datetime.date.today() - datetime.timedelta(days=i)).isoformat()
        label = (datetime.date.today() - datetime.timedelta(days=i)).strftime("%a")
        scores = {}
        for sid, sname in [(1,"math"),(2,"sci"),(3,"eng")]:
            row = query("""
                SELECT ROUND(AVG(up.score),1) as avg
                FROM user_progress up
                JOIN lessons l ON up.lesson_id=l.id
                JOIN users u ON up.user_id=u.id
                WHERE l.subject_id=? AND u.village=?
                AND DATE(up.completed_at)=?
            """, (sid, village, day), one=True)
            scores[sname] = row["avg"] if row and row["avg"] else 0
        result.append({"day": label, **scores})
    return jsonify(success=True, data=result)


# ─────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print("\n🚀 VidyaQuest running at http://localhost:5000")
    print("━" * 45)
    print("  Demo Student  → student@demo.com / demo123")
    print("  Demo Teacher  → teacher@demo.com / teacher123")
    print("━" * 45 + "\n")
    app.run(debug=True, port=5000)
