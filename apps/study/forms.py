from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class WriteForm(FlaskForm):
  subject = StringField(
    "제목",
    validators=[
      DataRequired(message = '제목은 필수'),
      Length(max = 20, message = '20글자')
    ]
  )
  content = TextAreaField(
    "내용",
    validators=[
      DataRequired(message= '내용을 입력하세요.')
    ]
  )
  writer = StringField(
    "작성자",
    validators=[
      DataRequired(message='작성자 이름은 필수로 적어주세요.')
    ]
  )
  submit = SubmitField('글작성')
