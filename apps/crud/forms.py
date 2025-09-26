from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):

  username = StringField(
    "사용자명", # label
    validators=[
      DataRequired(message = "사용자명은 필수."),
      Length(max=30, message = "사용자명은 30글자 이내로 입력")
    ]
  )

  email = StringField(
    "이메일", # label
    validators=[
      DataRequired(message="이메일은 필수 입력."),
      Email(message="이메일 형식으로 입력하시오.")
    ]
  )
  password = PasswordField(
    "비밀번호", # label
    validators=[
      DataRequired(message="비밀번호는 필수")
    ]
  )
  submit = SubmitField("회원가입")
  