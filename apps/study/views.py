from flask import Blueprint, render_template, request, redirect, url_for
from apps.study.forms import WriteForm
from apps.study.models import Study
from apps.app import db

study = Blueprint(
  "study",
  __name__,
  template_folder="templates",
  static_folder="static"
)

@study.route('/', methods=['GET'])
def index():
  posts = Study.query.order_by(Study.id.desc())
  return render_template('study/index.html', posts=posts)

@study.route('/write', methods=['POST', 'GET'])
def write():
  form = WriteForm()
  if form.validate_on_submit():
    post = Study(
      subject = form.subject.data,
      content = form.content.data,
      writer = form.writer.data
    )
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('study.index'))
  
  return render_template('study/write.html', form = form)

@study.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
  post = Study.query.get(id)
  form = WriteForm(obj = post)

  if form.validate_on_submit():
      post.subject = form.subject.data
      post.content = form.content.data
      post.writer = form.writer.data
      db.session.add(post)
      db.session.commit()
      return redirect(url_for('study.index'))  
    
  return render_template('study/edit.html', post = post, form=form)

@study.route('/edit/<id>/delete', methods=['POST'])
def delete_post(id):
  Study.query.filter_by(id = id).delete()
  db.session.commit()
  return redirect(url_for('study.index'))