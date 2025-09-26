from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms import SubmitField

class UploadImageForm(FlaskForm):
  image = FileField(
    validators=[
      FileRequired("업로드할 파일 선택"),
      FileAllowed(['png', 'jpg','gif','jpeg'], "지원하지 않는 확장자")
    ]
  )
  submit = SubmitField('업로드')
