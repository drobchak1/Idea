from flask import render_template, request, Blueprint, url_for
from projectchange.models import Idea, IdeaLike
from projectchange import db
from sqlalchemy import func
from sqlalchemy.sql import text
from flask import session


core = Blueprint('core', __name__)

@core.route('/')
def index():
    page = request.args.get('page',1,type=int)
    # ideas = Idea.query.order_by(Idea.date.desc()).paginate(page=page,per_page=10)
    ideas = Idea.query.join(IdeaLike).group_by(Idea.id).order_by(func.count(Idea.id).desc()).paginate(page=page,per_page=10)
    next_url = url_for('core.index', page=ideas.next_num) \
        if ideas.has_next else None
    prev_url = url_for('core.index', page=ideas.prev_num) \
        if ideas.has_prev else None
    # ideas = Idea.query.order_by(Idea.likes.count().desc()).paginate(page=page,per_page=10)
    # ideas = Idea.query.join(IdeaLike).group_by(Idea.id).order_by(func.count().desc()).paginate(page=page,per_page=10)
    return render_template('index.html', ideas=ideas, next_url=next_url, prev_url=prev_url)

    #ideas = Idea.query.order_by(Idea.date.desc()).paginate(page=page,per_page=10)
    ###############THIS WORKS BUT DON`T SHOW ZERO
    
    # ideas = Idea.query.join(IdeaLike).group_by(Idea.id).order_by(func.count().desc()).paginate(page=page,per_page=10)


    # ideas = db.session.query(Idea, func.count(IdeaLike.user_id).label('total')).join(IdeaLike).group_by(Idea).order_by(cursor.execute(text('total DESC'))).paginate(page=page,per_page=10)
    # db.session.query(Post, func.count(likes.c.user_id).label('total')).join(likes).group_by(Post).order_by('total DESC')

    # ideas = Idea.query.join(Idea.likes).order_by('idea_like'.count(self).desc()).paginate(page=page,per_page=10) 
    # bases = dbsession.query(Base)
    # bases = bases.order_by(Base.owner.name)
    
    # session.query(Base).join(Base.owner).order_by(Player.name)
    

@core.route('/info')
def info():
    return render_template('info.html')
