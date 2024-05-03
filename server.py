from flask import Flask, render_template, redirect, flash, url_for, session, request
from datetime import timedelta
from sqlalchemy.exc import IntegrityError, DataError, DatabaseError, InterfaceError, InvalidRequestError
from werkzeug.routing import BuildError
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from auth.app import login_manager, db
from auth.models import User
from auth.forms import login_form, register_form


from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


from auth.auth_routing import auth_routing


app = Flask(__name__)

app.register_blueprint(auth_routing)

app.secret_key = 'tempkey'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SECRET_KEY'] = 'secret!'

migrate = Migrate()
bcrypt = Bcrypt()

login_manager.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)


@app.before_request
def create_tables():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=7)


app.run(debug=True, host='0.0.0.0', port=8080)