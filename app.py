from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

# -----------------------------
# Flask setup
# -----------------------------
app = Flask(__name__)
app.secret_key = "secret123"   # for session

# -----------------------------
# Database initialization
# -----------------------------
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS leaves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        from_date TEXT,
        to_date TEXT,
        days INTEGER,
        reason TEXT,
        status TEXT,
        remark TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

# -----------------------------
# Helper function
# -----------------------------
def get_db():
    return sqlite3.connect('database.db')

# -----------------------------
# Home page
# -----------------------------
@app.route('/')
def index():
    return render_template('index.html')

# -----------------------------
# Staff login
# -----------------------------
@app.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=? AND role='staff'",
            (u, p)
        )
        user = cur.fetchone()

        if user:
            session['user'] = u
            return redirect('/staff_dashboard')

    return render_template('staff_login.html')

# -----------------------------
# Staff dashboard
# -----------------------------
@app.route('/staff_dashboard')
def staff_dashboard():
    if 'user' not in session:
        return redirect('/staff_login')

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM leaves WHERE username=?", (session['user'],))
    leaves = cur.fetchall()

    return render_template('staff_dashboard.html', leaves=leaves)

# -----------------------------
# Apply leave
# -----------------------------
@app.route('/apply_leave', methods=['GET', 'POST'])
def apply_leave():
    if 'user' not in session:
        return redirect('/staff_login')

    if request.method == 'POST':
        from_date = request.form['from_date']
        to_date = request.form['to_date']
        reason = request.form['reason']

        days = (datetime.strptime(to_date, '%Y-%m-%d') -
                datetime.strptime(from_date, '%Y-%m-%d')).days + 1

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO leaves VALUES (NULL, ?, ?, ?, ?, ?, 'Pending', '')",
            (session['user'], from_date, to_date, days, reason)
        )
        db.commit()

        return redirect('/staff_dashboard')

    return render_template('apply_leave.html')

# -----------------------------
# Admin login
# -----------------------------
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=? AND role='admin'",
            (u, p)
        )
        admin = cur.fetchone()

        if admin:
            session['admin'] = u
            return redirect('/admin_dashboard')

    return render_template('admin_login.html')

# -----------------------------
# Admin dashboard
# -----------------------------
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect('/admin_login')

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM leaves")
    leaves = cur.fetchall()

    return render_template('admin_dashboard.html', leaves=leaves)

# -----------------------------
# First-time user creation (RUN ONCE, THEN DELETE) 
# ie, only for first time..if needed we can delete this create_initial_users()
# -----------------------------
def create_initial_users():
    db = get_db()
    cur = db.cursor()

    try:
        cur.execute(
            "INSERT INTO users VALUES (NULL,'admin','Admin@123','admin')"
        )
        cur.execute(
            "INSERT INTO users VALUES (NULL,'staff1','Staff@123','staff')"
        )
        db.commit()
    except:
        pass   # avoids duplicate error

# create_initial_users()
# ........................................

@app.route('/update_leave/<int:leave_id>/<status>')
def update_leave(leave_id, status):
    if 'admin' not in session:
        return redirect('/admin_login')

    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE leaves SET status=? WHERE id=?", (status, leave_id))
    db.commit()

    return redirect('/admin_dashboard')

# -----------------------------
# Run app
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
