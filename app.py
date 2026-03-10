from flask import Flask, render_template, request, jsonify, redirect, session
import subprocess
import os
import uuid
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"


# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS files(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        filename TEXT,
        code TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


# ---------------- HOME ----------------

@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return render_template("login.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users(username,password) VALUES (?,?)",
                (username, hashed_password)
            )
            conn.commit()
        except:
            conn.close()
            return "Username already exists"

        conn.close()

        return redirect("/")

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    row = cur.fetchone()
    conn.close()

    if row and check_password_hash(row[0], password):
        session["user"] = username
        return redirect("/dashboard")

    return "Invalid username or password"


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    return render_template("dashboard.html")


# ---------------- SAVE FILE ----------------

@app.route("/save_file", methods=["POST"])
def save_file():

    if "user" not in session:
        return jsonify({"status": "not_logged_in"})

    data = request.json
    filename = data.get("filename")
    code = data.get("code")

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO files(username,filename,code) VALUES (?,?,?)",
        (session["user"], filename, code)
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "saved"})


# ---------------- LOAD USER FILES ----------------

@app.route("/get_files")
def get_files():

    if "user" not in session:
        return jsonify([])

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT filename,code FROM files WHERE username=?",
        (session["user"],)
    )

    rows = cur.fetchall()
    conn.close()

    files = []

    for r in rows:
        files.append({
            "filename": r[0],
            "code": r[1]
        })

    return jsonify(files)


# ---------------- RUN CODE ----------------

@app.route("/run", methods=["POST"])
def run_code():

    data = request.json
    code = data.get("code", "")

    if len(code) > 10000:
        return jsonify({"output": "Code too large."})

    blocked_keywords = [
        "import os",
        "import sys",
        "subprocess",
        "shutil",
        "open(",
        "__import__",
        "eval(",
        "exec("
    ]

    for word in blocked_keywords:
        if word.lower() in code.lower():
            return jsonify({"output": "Restricted operation detected."})

    filename = f"temp_{uuid.uuid4().hex}.py"

    with open(filename, "w") as f:
        f.write(code)

    try:

        result = subprocess.run(
            ["python3", filename],
            capture_output=True,
            text=True,
            timeout=5
        )

        output = result.stdout + result.stderr

        if len(output) > 5000:
            output = output[:5000] + "\nOutput truncated..."

    except subprocess.TimeoutExpired:
        output = "Execution timed out (possible infinite loop)"

    except Exception as e:
        output = str(e)

    finally:
        if os.path.exists(filename):
            os.remove(filename)

    return jsonify({"output": output})


# ---------------- START SERVER ----------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)