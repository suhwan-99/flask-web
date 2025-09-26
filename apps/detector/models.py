from datetime import datetime
from apps.app import db

class UserImage(db.Model):
  __tablename__ = 'user_images'
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  img_path = db.Column(db.String(255))
  is_detected = db.Column(db.Boolean, default = False) # 이미지를 업로드 후 물체감지가 됐는지 안됐는지 확인 함
  created_at = db.Column(db.DateTime, default = datetime.now)
  updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)

class UserImageTag(db.Model):
  __tablename__ = "user_image_tags"
  id = db.Column(db.Integer, primary_key = True)
  user_image_id = db.Column(db.Integer, db.ForeignKey('user_images.id'))
  tag_name = db.Column(db.String(255))
  created_at = db.Column(db.DateTime, default = datetime.now)
  updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)