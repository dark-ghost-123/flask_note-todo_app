from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta


auths = Blueprint("auths", __name__)


@auths.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Account Acticate.", category="Seccess")
                return redirect(url_for("views.home"))
            else : 
                flash("XXX password is wrong XXX", category="Error")
        else:
            flash("XXX user dosent exist XXX", category="Error")

    return render_template("login.html", user=current_user)


@auths.route('/logout', methods=["POST","GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auths.login"))


@auths.route('/sign-up', methods=["POST","GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("user exist !!!", category="Error")
        elif len(username) < 1 :               # check email 
            flash("fill username fild !!!", category="Error")
        elif len(email) < 4 :                # check username
            flash("email is not valid !!!", category="Error")
        elif password1 != password2 :        # check password confirmation
            flash("password dont match !!!", category="Error")
        elif len(password1) < 7 :            # check password len
            flash("password is short, password limit is 8 !!!", category="Error")
        else:                                # all data is correct
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(user=new_user, remember=True)
            flash("Account is create seccessfully.", category="Seccess")
            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)