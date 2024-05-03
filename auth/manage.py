from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

from flask_login import (
  UserMixin,
  login_user,
  LoginManager,
  current_user,
  logout_user,
  login_required,
)

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
  app = Flask(__name__)

  app.secret_key = 'tempkey'
  app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

  login_manager.init_app(app)
  db.init_app(app)
  migrate.init_app(app, db)
  bcrypt.init_app(app)

  return app


def deploy():
  """Run deployment tasks."""
  from app import db
  from flask_migrate import upgrade, migrate, init, stamp
#  from models import User

  
  app = create_app()
  app.app_context().push()
  db.create_all()

  # migrate database to latest revision
  init()
  stamp()
  migrate()
  upgrade()


deploy()