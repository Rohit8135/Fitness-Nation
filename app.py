from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import sqlite3
import os
from datetime import datetime
from functools import wraps
from flask import jsonify, request
from datetime import datetime
from flask_mail import Message,Mail

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.secret_key = 'fitnessnation_secret_key_2024'

DB_PATH = os.path.join(BASE_DIR, 'fitness_nation.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            plan TEXT NOT NULL,
            message TEXT,
            date TEXT NOT NULL,
            status TEXT DEFAULT 'New'
        )
    ''')
    conn.commit()
    conn.close()


init_db()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return render_template('index.html')



# ================== 📧 MAIL CONFIG ==================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'rohitbavale8135@gmail.com'
app.config['MAIL_PASSWORD'] = 'ptak qosc ectj icio'  # 🔴 PUT YOUR APP PASSWORD HERE

mail = Mail(app)

# ================== 💾 DATABASE ==================
def get_db():
    return sqlite3.connect('database.db')

# Create table (run once)
def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            plan TEXT,
            message TEXT,
            date TEXT
        )
    ''')
    conn.close()

init_db()

# ================== 🚀 ENQUIRY ROUTE ==================
@app.route('/submit_enquiry', methods=['POST'])
def submit_enquiry():
    try:
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        plan = request.form.get('plan', '').strip()
        message = request.form.get('message', '').strip()

        # ✅ VALIDATION
        if not name or not phone or not plan:
            return jsonify({'success': False, 'message': 'Please fill all required fields.'})

        date = datetime.now().strftime('%d %b %Y, %I:%M %p')

        # ✅ SAVE TO DATABASE
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO enquiries (name, phone, plan, message, date) VALUES (?, ?, ?, ?, ?)',
            (name, phone, plan, message, date)
        )
        conn.commit()
        conn.close()

        # 📧 SEND EMAIL
        msg = Message(
            subject="🔥 New Gym Enquiry Received",
            sender=app.config['MAIL_USERNAME'],
            recipients=['rohitbavale8135@gmail.com']
        )

        msg.body = f"""
New Enquiry Received 🚀

👤 Name: {name}
📞 Phone: {phone}
📦 Plan: {plan}
💬 Message: {message}
📅 Date: {date}
        """

        mail.send(msg)

        print("✅ Email Sent Successfully")

        return jsonify({
            'success': True,
            'message': 'Your enquiry has been submitted successfully. Our team will contact you shortly.'
        })

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({
            'success': False,
            'message': 'Error: ' + str(e)
        })

# ================== 🧪 TEST MAIL ==================
@app.route('/test-mail')
def test_mail():
    try:
        msg = Message(
            subject="Test Mail",
            sender=app.config['MAIL_USERNAME'],
            recipients=['rohitbavale8135@gmail.com']
        )
        msg.body = "Mail working successfully ✅"
        mail.send(msg)
        return "Mail Sent Successfully!"
    except Exception as e:
        return str(e)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('admin'))
        else:
            error = 'Invalid credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    search = request.args.get('search', '').strip()
    conn = get_db()
    if search:
        enquiries = conn.execute(
            "SELECT * FROM enquiries WHERE name LIKE ? OR phone LIKE ? OR plan LIKE ? ORDER BY id DESC",
            (f'%{search}%', f'%{search}%', f'%{search}%')
        ).fetchall()
    else:
        enquiries = conn.execute('SELECT * FROM enquiries ORDER BY id DESC').fetchall()

    total = conn.execute('SELECT COUNT(*) FROM enquiries').fetchone()[0]
    today_str = datetime.now().strftime('%d %b %Y')
    today_count = conn.execute(
        "SELECT COUNT(*) FROM enquiries WHERE date LIKE ?", (f'{today_str}%',)
    ).fetchone()[0]
    conn.close()
    return render_template('admin.html', enquiries=enquiries, search=search, total=total, today_count=today_count)

@app.route('/delete_enquiry/<int:id>', methods=['POST'])
@login_required
def delete_enquiry(id):
    conn = get_db()
    conn.execute('DELETE FROM enquiries WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/update_status/<int:id>', methods=['POST'])
@login_required
def update_status(id):
    status = request.form.get('status')
    conn = get_db()
    conn.execute('UPDATE enquiries SET status = ? WHERE id = ?', (status, id))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))


if __name__ == '__main__':
    print("\n" + "="*50)
    print("  FITNESS NATION - Management System")
    print("="*50)
    print("  Running locally...")
    print("="*50 + "\n")

    app.run(host='0.0.0.0', port=5000)