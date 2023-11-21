from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'your_default_secret_key')


conn = sqlite3.connect('database')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS database (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, username TEXT, email TEXT, password TEXT)')
conn.commit()
conn.close()


def create_connection():
    conn = sqlite3.connect('database')
    return conn


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/capsule')
def capsule():
    return render_template("capsule.html")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user_details = request.form

        if not user_details["firstname"] or not user_details["lastname"] or not user_details["username"] or not \
        user_details["email"] or not user_details["password"]:
            flash("All fields are required. Please fill in all the details.", "danger")
            return render_template('signup.html')


        if user_details["password"] != user_details["confirmPassword"]:
            flash("Passwords do not match! Try again!", "danger")
            return render_template('signup.html')

        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM database WHERE username=? OR email=?", (user_details["username"], user_details["email"]))
        existing_user = cur.fetchone()

        if existing_user:
            flash("Username or email already exists. Please choose another.", "danger")
            return render_template('signup.html')

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO database (first_name, last_name, username, email, password) VALUES (?, ?, ?, ?, ?)",
            (
                user_details["firstname"],
                user_details["lastname"],
                user_details["username"],
                user_details["email"],
                generate_password_hash(user_details["password"]),
            ),
        )
        conn.commit()
        conn.close()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM database WHERE username=? AND email=?", (username, email))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[5], password):
            print('User authenticated successfully')
        else:
            print('Invalid username, email, or password')

        return redirect(url_for('capsule'))

    return render_template('login.html')


@app.route('/monday.html')
def monday():
    return render_template('monday.html')

@app.route('/men-monday')
def menmonday():
    return render_template('men-monday.html')

@app.route('/men-tuesday.html')
def tuesday():
    return render_template('men-tuesday.html')

@app.route('/men-wednesday')
def wednesday():
    return render_template('men-wednesday.html')

@app.route('/men-thursday.html')
def thursday():
    return render_template('men-thursday.html')

@app.route('/men-friday.html')
def friday():
    return render_template('men-friday.html')

@app.route('/men-saturday.html')
def saturday():
    return render_template('men-saturday.html')

@app.route('/men-sunday.html')
def sunday():
    return render_template('men-sunday.html')

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080, use_reloader=False)


