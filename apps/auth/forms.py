from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class SignUpForm(FlaskForm):
  username = StringField(
    "사용자명",
    validators=[
      DataRequired('사용자명 작성은 필수 입니다')
    ]
  )
  password = PasswordField(
    "비밀번호",
    validators=[
      DataRequired('비밀번호는 필수 입니다'),
      Length(min=3, max=20, message='비밀번호는 3~20글자')
    ]
  )
  email = StringField(
    "이메일",
    validators=[
      DataRequired('이메일은 필수 입니다'),
      Email('이메일 형식으로 입력')
    ]
  )
  submit = SubmitField("회원가입")

class LoginForm(FlaskForm):
  username = StringField(
    "사용자명",
    validators=[
      DataRequired('사용자명 작성은 필수 입니다')
    ]
  )
  password = PasswordField(
    "비밀번호",
    validators=[
      DataRequired('비밀번호는 필수 입니다'),
      Length(min=3, max=20, message='비밀번호는 3~20글자')
    ]
  )
  submit = SubmitField("로그인")