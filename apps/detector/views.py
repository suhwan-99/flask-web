from flask import Blueprint, render_template, current_app, send_from_directory, redirect, url_for,flash,request
from flask_login import login_required, current_user
from pathlib import Path
import uuid # 파일명 변경하는 용도
import cv2 # 이미지에 선 그리는 용도
import torch
import torchvision
from PIL import Image # 이미지 불러오는 용도
import numpy as np


from apps.detector.forms import UploadImageForm
from apps.app import db
from apps.detector.models import UserImage, UserImageTag
from apps.crud.models import User

dt = Blueprint(
  "detector",
  __name__,
  template_folder="templates"
  
)

@dt.route('/')
def index():
  # DB에서 user_id가 서로 일치한 것들을 조인해서 가져옴
  user_images = db.session.query(User, UserImage).join(UserImage).filter(User.id == UserImage.user_id).all()
  user_image_tag_dict = {}
  
  for user_image in user_images:
    user_image_tags = db.session.query(UserImageTag).filter(UserImageTag.user_image_id == user_image.UserImage.id).all()

    user_image_tag_dict[user_image.UserImage.id] = user_image_tags

  return render_template('detector/index.html', user_images = user_images, user_image_tag_dict = user_image_tag_dict)

@dt.route('/images/<path:filename>')
def images(filename):

  return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

@dt.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_image():
  form = UploadImageForm()
  if form.validate_on_submit():
    file = form.image.data

    # 중복된 이미지 파일명 방지를 위해 이름을 uuid로 교체 / suffix 확장자 꺼내옴
    ext = Path(file.filename).suffix
    image_uuid_filename = str(uuid.uuid4()) + ext
    image_path = Path(current_app.config["UPLOAD_FOLDER"], image_uuid_filename)
    file.save(image_path)

    # 위 데이터를 DB에 저장
    user_image = UserImage(user_id = current_user.id, img_path = image_uuid_filename)
    db.session.add(user_image)
    db.session.commit()
    return redirect( url_for ('detector.index'))

  return render_template('detector/upload.html', form = form)

@dt.route('/images/delete/<image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
  try:
    # tags 먼저 삭제
    db.session.query(UserImageTag).filter(UserImageTag.user_image_id == image_id).delete()

    # 이미지 정보 삭제
    db.session.query(UserImage).filter(UserImage.id == image_id).delete()

    db.session.commit()
  except Exception as e:
    flash('삭제 중 오류 발생')
    current_app.logger.error(e) # print(e)
    db.session.rollback()

  return redirect(url_for ('detector.index'))

@dt.route('/images/search')
def search():
  search_text = request.args.get('search')
  user_images = db.session.query(User, UserImage).join(UserImage).filter(User.id == UserImage.user_id).all()
  user_image_tag_dict = {}
  filtered_user_images = [] # 검색어를 포함하는 태그를 가지고 있는 이미지 목록들을 가지고 있는 리스트
  for user_image in user_images:
    if not search_text:
      user_image_tags = db.session.query(UserImageTag).filter(UserImageTag.user_image_id == user_image.UserImage.id).all()
    else:
      user_image_tags = db.session.query(UserImageTag).filter(UserImageTag.user_image_id == user_image.UserImage.id)\
                                                      .filter(UserImageTag.tag_name.like(f"%{search_text}")).all()
      # 검색어를 포함하는 태그가 없는지
      if not user_image_tags:
        continue
    user_image_tags = db.session.query(UserImageTag).filter(UserImageTag.user_image_id == user_image.UserImage.id).all()
    
    filtered_user_images.append(user_image)
    
    user_image_tag_dict[user_image.UserImage.id] = user_image_tags

  return render_template('detector/index.html', user_images = filtered_user_images, user_image_tag_dict = user_image_tag_dict)


















# 물체 감지 처리에 필요한 함수들

import random
# 선의 색을 지정하는 함수
# ai 가 객체 탐지를 완료 후 탐지된 물체 목록들을 labels로 보냄
def make_color(labels):
  colors = [ [random.randint(0, 255) for _ in range(3)] for _ in labels ]
  color = random.choice(colors)
  return color

# 이미지 크기에 따라 선 두께를 리턴해주는 함수
# 이미지의 너비와 높이 중 더 큰 값을 기준으로 선 두께를 정함
def make_line(result_image):
  line = round(max (result_image.shape[0:2]) * 0.002) + 1
  return line

# 이미지에 박스 그려주는 함수
# c1, c2 : 박스를 그릴 좌표(왼쪽위, 오른쪽 아래)
def draw_lines(c1, c2, result_image, line, color):
  cv2.rectangle(result_image, c1, c2, color, thickness=line) # 이미지, 좌표, 색, 두께
  return cv2

# 이미지에 라벨 넣는 함수
def draw_texts(result_image, line, c1, cv2, color, labels, label):
  display_text = labels[label]
  font = max(line - 1, 1) # 선 두께
                        # 라벨 이름,         선 두께,               두께 = 선 두께
  t_size = cv2.getTextSize(display_text, 0, fontScale = line/3, thickness=font)[0]
  c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
                                            # 색 채우기 thickness = -1
  cv2.rectangle(result_image, c1, c2, color, -1)
  cv2.putText(result_image, display_text, (c1[0], c1[1]- 2), 0, line/3, [255,255,255], thickness = font, lineType = cv2.LINE_AA)

# 이미지를 가져온 후 물체 탐지 후 라벨이 추가 된 이미지를 생성
# 생성된 이미지와 라벨을 리턴
def exec_detect(target_image_path):
  labels = current_app.config['LABELS']
  
  # 이미지 가져오기
  image = Image.open(target_image_path)
  # 가져온 이미지를 모델이 읽을 수 있는 (tensor)자료형으로 변환 - 숫자형태인 배열
  image_tensor = torchvision.transforms.functional.to_tensor(image)

  # 모델(ai) 불러오기
  model = torch.load(Path(current_app.root_path, "detector", "model.pt"), weights_only=False)
  # 예측할 수 있게 변경
  model = model.eval()

  # 예측 해보기
  output = model( [image_tensor] )[0]

  # 감지된 물체들 목록을 저장할 리스트
  tags = []
  result_image = np.array(image.copy())

  for box, label, score in zip( output['boxes'], output['labels'], output['scores']):
    if score > 0.5 and labels[label] not in tags:
      color = make_color(labels)
      line = make_line(result_image)

      c1 = (int(box[0]), int(box[1]))
      c2 = (int(box[2]), int(box[3]))

      cv2 = draw_lines(c1, c2, result_image, line, color)
      draw_texts(result_image, line, c1, cv2, color, labels, label)

      tags.append(labels[label])
    if tags:
      # 이미지 파일명
      detected_image_file_name = str(uuid.uuid4()) + '.jpg'

      # 이미지 저장 경로
      detected_image_file_path = str(Path(current_app.config['UPLOAD_FOLDER'], detected_image_file_name))
      
      # 이미지 저장
      cv2.imwrite(detected_image_file_path, cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR))

      return tags, detected_image_file_name
    else:
      return tags, None
    
@dt.route('/detect/<image_id>', methods=['POST'])
@login_required
def detect(image_id):
  user_image = db.session.query(UserImage).filter(UserImage.id == image_id).first()
  if user_image is None:
    flash("감지할 이미지가 존재하지 않습니다")
    return redirect( url_for ('detector.index'))
  target_image_path = Path(current_app.config['UPLOAD_FOLDER'], user_image.img_path) 
  tags, detected_file_name = exec_detect(target_image_path)
  

  if not tags:
    flash("감지된 결과가 없습니다")
    return redirect( url_for ('detector.index'))

  user_image.is_detected = True # 감지된 데이터
  user_image.img_path = detected_file_name # 이미지를 감지된 이미지로 변경
  db.session.add(user_image)

  # 감지된 라벨들을 DB에 넣는 반복문
  for tag in tags:
    user_image_tag = UserImageTag(user_image_id = user_image.id, tag_name = tag)

    db.session.add(user_image_tag)
    db.session.commit()
  return redirect( url_for ('detector.index'))





# @dt.route('/test')
# def test():
#   image_path = Path(current_app.config["UPLOAD_FOLDER"], '44e2a57b-f44d-4daf-9934-a0ec48782cc9.jpg')
#   result, image = exec_detect(image_path)

#   print("=" * 20)
#   print(result["boxes"][0])
#   print(result["labels"][0])
#   print(result["scores"][0])

#   copy_image = np.array(image.copy())
#   box = result["boxes"][0]
#   draw_lines( (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), copy_image, 1, [255, 0, 0], )
  
#   cv2.imshow("aa", copy_image)
#   cv2.waitKey(0)
#   return ""

