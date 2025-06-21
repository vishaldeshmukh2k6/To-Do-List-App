from flask import Blueprint, render_template, flash, url_for, redirect, session, request
from app import db
from app.models import Task, User

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=session['user']).first()
    if not user:
        flash("User not found", "danger")
        return redirect(url_for('auth.login'))

    tasks = Task.query.filter_by(user_id=user.id).all()
    return render_template('tasks.html', tasks=tasks)

@tasks_bp.route('/add', methods=['POST'])
def add_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    title = request.form.get('title')
    if title:
        user = User.query.filter_by(username=session['user']).first()
        new_task = Task(title=title, status='Pending', user_id=user.id)
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully.", 'success')

    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/toggle/<int:task_id>', methods=["POST"])
def toggle_status(task_id):
    task = Task.query.get(task_id)
    if task and task.owner.username == session.get('user'):
        if task.status == 'Pending':
            task.status = 'Working'
        elif task.status == 'Working':
            task.status = 'Done'
        else:
            task.status = 'Pending'
        db.session.commit()
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/delete/<int:task_id>', methods=["POST"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task and task.owner.username == session.get('user'):
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted successfully.", "info")
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/clear', methods=['POST'])
def clear_tasks():
    user = User.query.filter_by(username=session['user']).first()
    Task.query.filter_by(user_id=user.id).delete()
    db.session.commit()
    flash("All tasks cleared.", 'info')
    return redirect(url_for('tasks.view_tasks'))

