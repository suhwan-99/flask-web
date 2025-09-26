from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required # 인증되지 않은 사용자가 접근하면 막아버림
from apps.crud.forms import UserForm
from apps.crud.models import User
from apps.app import db

crud = Blueprint(
  "crud", # 블루프린트의 이름 지정
  __name__, # 블루포인트가 정의된 모듈명
  template_folder="templates", # 해당 블루포인트와 관련된 템프릿 파일이 있는 폴더
  static_folder="static" # 해당 블루포인트와 관련된 정적(static) 파일이 있는 폴더
)

@crud.route('/')
def index():

  return render_template("crud/index.html")

@crud.route('/test', methods=['GET','POST']) # flask_form을 사용하지 않음
def test():
  if request.method == 'POST':
    print(request.form.get('username')) # 진자를 사용 안하고 직접 태그를 쓰면 이렇게 받아옴 get을 사용해도 되고
    print(request.form['email'])        # 대괄호를 사용해도 됨
    print(request.form['password'])
  return render_template('crud/formtest.html')

@crud.route('/users/new', methods=['GET', 'POST']) # flask_form 사용
def create_user():
  form = UserForm() # 객체로 만들어 놓으면 진자로 토큰을 받고 데이터도 받을 수 있음
  # print(form.username.data)
  # print(form.password.data)
  # print(form.email.data)

  if form.validate_on_submit(): # 유효성 검사 해주는 함수
    # 유효성 검사 통과 후 처리될 코드
    user = User(
      username = form.username.data, 
      email = form.email.data,
      password = form.password.data
    )
    # add = insert
    db.session.add(user)
    db.session.commit()
    return redirect(url_for ('crud.users'))


  return render_template('crud/create.html', form = form)

# 회원목록 페이지로 이동
@crud.route('/users', methods=['GET'])
@login_required
def users():
  # DB에서 전체 레코드 꺼내오기
  # select * from users
 # users = db.session.query(User).all() # User테이블을 사용해서 쿼리문 사용 하겠단 코드
  users = User.query.all()
  # print(users[0].username)
  return render_template('crud/index.html', users = users)

@crud.route('/users/<user_id>', methods=['POST', 'GET'])
@login_required
def edit_user(user_id):
  form = UserForm()
  user= User.query.filter_by(id = user_id).first()

  if form.validate_on_submit():
      user.username = form.username.data
      user.email = form.email.data
      user.password = form.password.data
      db.session.add(user)
      db.session.commit()
      return redirect(url_for('crud.users'))  
    
  return render_template('crud/edit.html', user = user, form = form)

@crud.route('/user/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
  User.query.filter_by(id = user_id).delete()
 
 # db.session.delete(user)
  db.session.commit()
  return redirect( url_for ('crud.users'))
