from flask import render_template, request, Blueprint, url_for
from projectchange.models import Idea, IdeaLike
from sqlalchemy import func


core = Blueprint('core', __name__)

@core.route('/')
def index():
    page = request.args.get('page',1,type=int)
    ideas = Idea.query.outerjoin(IdeaLike).group_by(Idea.id).order_by(func.count(Idea.id).desc()).paginate(page=page,per_page=10)
    next_url = url_for('core.index', page=ideas.next_num) \
        if ideas.has_next else None
    prev_url = url_for('core.index', page=ideas.prev_num) \
        if ideas.has_prev else None
    return render_template('index.html', ideas=ideas, next_url=next_url, prev_url=prev_url)

@core.route('/info')
def info():
    return render_template('info.html')
