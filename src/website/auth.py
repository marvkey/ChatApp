from flask import Blueprint,render_template,redirect,url_for,request,flash
from .model import User
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint("auth",__name__)
@auth.route("/login",methods=["GET","POST"])
def Login():
    if request.method =='POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("logged in!",category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Password is incorrect",category='error')
        else:
            flash("email is not valid",category='error')
    return render_template("auth/login.html",user=current_user)
    
@auth.route("/sign-up",methods=["GET","POST"])
def SignUp():
    if request.method =='POST':
        
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password")
        password2 = request.form.get("password2")

        email_exist = User.query.filter_by(email=email).first()
        username_exist = User.query.filter_by(username=username).first()
        if email_exist:
            flash("User already exist with the given email", category='error') # flash an error onscreen
        elif username_exist:
            flash("User already exist with the given username",category="error")
        elif password1 != password2:
            flash("Password dont\'t match!",category='error')
        elif len(username)<2:
            flash("username is to short atleast3 characters",category='error')
        elif len(password1)<4:
            flash("password is to short atleast 5 character in lenght",category='error')
        else:#if everything success
            new_user =User(email=email,username=username,password=generate_password_hash(password1,method ="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash("User Created",category='success')
            return redirect(url_for('views.home'))
    return render_template("auth/sign-up.html",user=current_user)
@auth.route("/logout")
@login_required # only access the page when logged in
def logout():
    logout_user()
    return redirect(url_for("views.home"))