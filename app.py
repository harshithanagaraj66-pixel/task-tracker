from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

def init_db():
    conn = sqlite3.connect('tasks.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, username TEXT, task TEXT)')
    conn.close()

init_db()

@app.route('/')
def home():
    if 'user' in session:
        return redirect('/dashboard')
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('tasks.db')
        conn.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('tasks.db')
        cur = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cur.fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect('/dashboard')
        else:
            return "❌ Invalid username or password"

    return render_template('login.html')
    return render_template('login.html')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 'user' not in session:
        return redirect('/login')

    username = session['user']

    conn = sqlite3.connect('tasks.db')
    conn.execute(
        "DELETE FROM tasks WHERE id=? AND username=?",
        (task_id, username)
    )
    conn.commit()
    conn.close()

    return redirect('/dashboard')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    username = session['user']
    conn = sqlite3.connect('tasks.db')

    if request.method == 'POST':
        task = request.form['task']
        conn.execute(
            "INSERT INTO tasks (username, task) VALUES (?,?)",
            (username, task)
        )
        conn.commit()

    cur = conn.execute(
        "SELECT id, task FROM tasks WHERE username=?",
        (username,)
    )

    tasks = cur.fetchall()
    conn.close()

    return render_template('dashboard.html', tasks=tasks, username=username)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('tasks.db')
    conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/dashboard')
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
