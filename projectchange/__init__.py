from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_required
# from projectchange.models import Idea
from sqlalchemy.orm import column_property


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

###########################
############# DATABASE SETUP 
###########################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)


#############################
###############LOGIN CONFIGS
#############################

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

from projectchange.core.views import core
from projectchange.error_pages.handlers import error_pages
from projectchange.ideas.views import ideas
from projectchange.users.views import users
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(ideas)

# @app.route('/like/<int:idea_id>/<action>')
# @login_required
# def like_action(idea_id, action):
#     idea = Idea.query.filter_by(id=idea_id).first_or_404()
#     if action == 'like':
#         current_user.like_idea(idea)
#         db.session.commit()
#     if action == 'unlike':
#         current_user.unlike_idea(idea)
#         db.session.commit()
#     return redirect(request.referrer)