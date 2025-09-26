from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class WriteBoardForm(FlaskForm):
  subject = StringField(
    "제목",
    validators=[
      DataRequired("글 제목은 필수")
    ]
  )
  content = TextAreaField(
    "내용",
    validators=[
      DataRequired('내용은 필수')
    ]
  )
  submit = SubmitField('글 등록')