from flask import Flask, render_template, request, redirect, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "secret123"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db():
    return sqlite3.connect("database.db")

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = hash_password(request.form["password"])

        db = get_db()
        db.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,password))
        db.commit()
        return redirect("/")
    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = hash_password(request.form["password"])

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username=? AND password=?",
                      (username,password)).fetchone()

    if user:
        session["user"] = username
        return redirect("/dashboard")
    else:
        return "Invalid Login"

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", user=session["user"])
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    db = get_db()
    db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    db.commit()
    app.run(debug=True)
