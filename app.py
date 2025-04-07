from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Criar banco e tabela se não existir
def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT)")
init_db()

@app.route("/")
def index():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.execute("SELECT id, title FROM tasks")
        tasks = cursor.fetchall()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    with sqlite3.connect("database.db") as conn:
        conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    with sqlite3.connect("database.db") as conn:
        conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
