# from flask import Blueprint, render_template, request, redirect, url_for, flash, session


# auth_bp = Blueprint('auth', __name__)

# USER_CREDENTIALS={
#     'username' : 'admin',
#     'password' : "12345"
# }

# @auth_bp.route('/login', methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get('password')

#         if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
#             session['user'] = username
#             flash("Login Successful", 'success')
#         else:
#             flash("Invalid User or password", 'danger')
#     return render_template('login.html')

# @auth_bp.route('/logout')
# def logout():
#     session.pop('user', None)
#     flash('Logged out', 'info')
#     return redirect(url_for('auth.login'))


from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already taken!", 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registered successfully! Please login.", 'success')
        return redirect(url_for('auth.login'))

    return render_template("register.html")

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user'] = username
            flash("Login Successful", 'success')
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash("Invalid credentials", 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))
