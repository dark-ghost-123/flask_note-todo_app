from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import Note, Todo
from . import db

views = Blueprint("views", __name__)

@views.route('/', methods=["POST","GET"])
@login_required
def home():           
    return render_template("index.html", user=current_user)

@views.route('/admin', methods=["POST","GET"])
@login_required
def admin():
    return render_template("index.html", user=current_user)

@views.route("/delete_note/<int:id>", methods=["POST"])
@login_required
def delete_note(id):
    note = Note.query.filter_by(id=id).first()
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("views.home"))

@views.route("/delete_todo/<int:id>", methods=["POST"])
@login_required
def delete_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("views.home"))

@views.route("/status_todo/<int:id>", methods=["POST"])
@login_required
def status_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.status = not todo.status
    db.session.commit()
    return redirect(url_for("views.home"))

@views.route("/add_todo", methods=["POST"])
@login_required
def add_todo():
    cat = request.form.get("category")
    title = request.form.get("title")
    cat = request.form.get("category")
    status = request.form.get("status")
    if len(title)<1:
        flash("title is too short", category='Error')
    elif len(cat)<1:
        cat = "Unknown"
    else:
        status = False
        new_note = Todo(category=cat, title=title, status=status, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash("Todo added !!!", category="Seccess")
    return redirect(url_for("views.home"))

@views.route("/add_note", methods=["POST"])
@login_required
def add_note():
    cat = request.form.get("category")
    title = request.form.get("title")
    note = request.form.get("note")
    if len(title)<1:
        flash("title is too short", category='Error')
    elif len(note)<1:
        flash("note text is too short", category='Error')
    else:
        new_note = Note(category=cat, title=title, note=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash("Note added !!!", category="Seccess")
    return redirect(url_for("views.home"))

@views.route("/cat-filter/<category>", methods=["POST"])
@login_required
def cat_filter(category):
    return render_template("test.html", user=current_user, cat=category)