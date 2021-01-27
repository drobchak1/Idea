from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from projectchange import db
from projectchange.models import Idea
from projectchange.ideas.forms import IdeaForm
from projectchange.ideas.picture_handler import add_idea_pic
import sys

ideas = Blueprint('ideas',__name__)

#########################CREATE
@ideas.route('/create',methods=['GET','POST'])
@login_required
def create_idea():
    form = IdeaForm()
    if form.validate_on_submit():
        idea = Idea(title=form.title.data, text=form.text.data,target=form.target.data,user_id=current_user.id)
        db.session.add(idea)
        db.session.commit()
        if form.picture.data:
            pic = add_idea_pic(form.picture.data,idea.id)
            idea.image = pic
            db.session.commit()
        return redirect(url_for('core.index'))
        flash('Your idea created!')
    return render_template('create_idea.html', form=form)

#########################VIEW 
@ideas.route('/<int:idea_id>')
def idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    image = url_for('static', filename='idea_pics/' + idea.image)
    return render_template('idea.html',title=idea.title, date=idea.date, i=idea, target=idea.target, image=image)

#########################UPDATE
@ideas.route('/<int:idea_id>/update',methods=['GET','POST'])
@login_required
def update(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    if idea.author != current_user:
        abort(403)

    form = IdeaForm()
    if form.validate_on_submit():
        idea.title=form.title.data
        idea.text=form.text.data
        idea.target=form.target.data
        db.session.commit()
        if form.picture.data:
            pic = add_idea_pic(form.picture.data,idea.id)
            idea.image = pic
            db.session.commit()
        flash('Your idea updated!')
        return redirect(url_for('ideas.idea', idea_id=idea.id))
    elif request.method == "GET":
        form.title.data = idea.title
        form.text.data = idea.text
        form.target.data = idea.target

    return render_template('create_idea.html', title = 'Updating', form=form)

#########################DELETE
@ideas.route('/<int:idea_id>/delete',methods=['GET','POST'])
@login_required
def delete_idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    if idea.author != current_user:
        abort(403)    

    db.session.delete(idea)
    db.session.commit()
    flash('Your idea succesfully deleted!')
    return redirect(url_for('core.index'))

@ideas.route('/like/<int:idea_id>/<action>')
@login_required
def like_action(idea_id, action):
    idea = Idea.query.filter_by(id=idea_id).first_or_404()
    if action == 'like':
        current_user.like_idea(idea)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_idea(idea)
        db.session.commit()
    return redirect(request.referrer)

@ideas.route('/search',methods=['GET','POST'])
def search():
    if request.method == "POST":
        searchinput = request.form["searchinput"] 
        page = request.args.get('page',1,type=int)
        # if searchinput == "" or " ":
        #     ideasfound = Idea.query.filter(Idea.title.ilike(f"%park%")).order_by(Idea.date.desc()).paginate(page=page,per_page=10)
        #     numberfound = len(ideasfound.items)       
        #     return render_template('search.html', ideasfound=ideasfound, searchinput=searchinput, numberfound=numberfound)     
        ideasfound = Idea.query.filter(Idea.title.ilike(f"%{searchinput}%")).order_by(Idea.date.desc()).paginate(page=page,per_page=10)
        numberfound = len(ideasfound.items)
        return render_template('search.html', ideasfound=ideasfound, searchinput=searchinput, numberfound=numberfound)
    else:
        return redirect(url_for('core.index'))