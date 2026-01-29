
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'demo_secret_key'  # Change in production
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Dummy data
users = {'admin@example.com': {'name': 'Admin', 'age': 30, 'phone': '1234567890', 'blood_group': 'O+', 'address': '123 St', 'password': 'password'}}
alerts = []
resources = [{'id': 1, 'title': 'Kit Guide', 'category': 'Disaster', 'description': 'Prepare kit.'}]
blog_posts = [{'id': 1, 'title': 'Disaster Help', 'content': 'Content...', 'comments': []}]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/sos', methods=['GET', 'POST'])
def sos():
    if request.method == 'POST':
        location = request.form.get('location')
        message = request.form.get('message')
        alerts.append({'location': location, 'message': message, 'user': session.get('user')})
        flash('SOS sent!')
        return redirect(url_for('home'))
    return render_template('sos.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            session['user'] = email
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        if email in users:
            flash('Email taken')
            return redirect(url_for('signup'))
        users[email] = {
            'name': request.form['name'],
            'age': int(request.form['age']),
            'phone': request.form['phone'],
            'blood_group': request.form['blood_group'],
            'address': request.form['address'],
            'password': request.form['password']
        }
        session['user'] = email
        flash('Signup success!')
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    profile = users.get(session['user'], {})
    user_alerts = [a for a in alerts if a.get('user') == session['user']]
    return render_template('dashboard.html', profile=profile, alerts=user_alerts)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/resources', methods=['GET', 'POST'])
def resources_page():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Uploaded!')
    category = request.args.get('category', '')
    filtered = [r for r in resources if category in r['category']] if category else resources
    return render_template('resources.html', resources=filtered)

@app.route('/blog')
def blog():
    return render_template('blog.html', posts=blog_posts)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/alerts')
def get_alerts():
    return jsonify(alerts)

if __name__ == '__main__':
    app.run(debug=True)