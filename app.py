import sqlite3
from flask import Flask, request, render_template, g
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB = "users.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create the users table and add a few sample users."""
    with sqlite3.connect(DB) as c:
        c.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "username TEXT PRIMARY KEY, password_hash TEXT NOT NULL)"
        )
        for name, pw in [("admin", "admin123"), ("ayush", "pass@123")]:
            c.execute(
                "INSERT OR IGNORE INTO users VALUES (?, ?)",
                (name, generate_password_hash(pw)),
            )


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Parameterized query -> safe from SQL injection
        row = get_db().execute(
            "SELECT password_hash FROM users WHERE username = ?", (username,)
        ).fetchone()

        if row and check_password_hash(row[0], password):
            return render_template("success.html", username=username)

        return render_template("login.html", error="Invalid login name or password.")

    return render_template("login.html", error=None)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
