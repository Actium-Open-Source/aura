from auth.app import db
from auth.forms import login_form, register_form
from auth.models import User
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_bcrypt import check_password_hash
from flask_login import login_required, login_user, logout_user
from sqlalchemy.exc import DataError, DatabaseError, IntegrityError, InterfaceError, InvalidRequestError
from werkzeug.routing import BuildError


auth_routing = Blueprint('auth_routing', __name__, template_folder='templates')


@auth_routing.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
  form = login_form()

  if form.validate_on_submit():
      try:
          user = User.query.filter_by(email=form.email.data).first()
          if check_password_hash(user.pwd, form.pwd.data):
              login_user(user)
              return redirect(url_for('index'))
          else:
              flash("Invalid Username or password!", "danger")
      except Exception as e:
          flash(e, "danger")

  return render_template(
    "auth.html",
     form=form,
     text="Login",
     title="Login",
     btn_action="Login"
  )


# Register route
@auth_routing.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
  form = register_form()
  if form.validate_on_submit():
      try:
          email = form.email.data
          pwd = form.pwd.data
          username = form.username.data

          newuser = User(
              username=username,
              email=email,
              pwd=bcrypt.generate_password_hash(pwd),
              img="./logo.png"
          )

          db.session.add(newuser)
          db.session.commit()
          flash(f"Account Successfully created", "success")
          return redirect(url_for("login"))

      except InvalidRequestError:
          db.session.rollback()
          flash(f"Something went wrong!", "danger")
      except IntegrityError:
          db.session.rollback()
          flash(f"User already exists!.", "warning")
      except DataError:
          db.session.rollback()
          flash(f"Invalid Entry", "warning")
      except InterfaceError:
          db.session.rollback()
          flash(f"Error connecting to the database", "danger")
      except DatabaseError:
          db.session.rollback()
          flash(f"Error connecting to the database", "danger")
      except BuildError:
          db.session.rollback()
          flash(f"An error occurred !", "danger")
  return render_template("auth.html",
                         form=form,
                         text="Create account",
                         title="Register",
                         btn_action="Register account"
                      )


@auth_routing.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for('login'))
