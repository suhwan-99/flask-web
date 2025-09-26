import secrets
from pathlib import Path

basedir = Path(__file__).parent.parent

# 개발과 배포 영역을 분리 할 거임

# 전체 환경 공통 설정들...
class BaseConfig:
  SECRET_KEY = secrets.token_urlsafe(32)
  WTF_CSRF_SECRET_KEY = secrets.token_urlsafe(32)
  UPLOAD_FOLDER = str(Path(basedir, 'apps', 'images'))
  LABELS = [
        "unlabeled",
        "person",
        "bicycle",
        "car",
        "motorcycle",
        "airplane",
        "bus",
        "train",
        "truck",
        "boat",
        "traffic light",
        "fire hydrant",
        "street sign",
        "stop sign",
        "parking meter",
        "bench",
        "bird",
        "cat",
        "dog",
        "horse",
        "sheep",
        "cow",
        "elephant",
        "bear",
        "zebra",
        "giraffe",
        "hat",
        "backpack",
        "umbrella",
        "shoe",
        "eye glasses",
        "handbag",
        "tie",
        "suitcase",
        "frisbee",
        "skis",
        "snowboard",
        "sports ball",
        "kite",
        "baseball bat",
        "baseball glove",
        "skateboard",
        "surfboard",
        "tennis racket",
        "bottle",
        "plate",
        "wine glass",
        "cup",
        "fork",
        "knife",
        "spoon",
        "bowl",
        "banana",
        "apple",
        "sandwich",
        "orange",
        "broccoli",
        "carrot",
        "hot dog",
        "pizza",
        "donut",
        "cake",
        "chair",
        "couch",
        "potted plant",
        "bed",
        "mirror",
        "dining table",
        "window",
        "desk",
        "toilet",
        "door",
        "tv",
        "laptop",
        "mouse",
        "remote",
        "keyboard",
        "cell phone",
        "microwave",
        "oven",
        "toaster",
        "sink",
        "refrigerator",
        "blender",
        "book",
        "clock",
        "vase",
        "scissors",
        "teddy bear",
        "hair drier",
        "toothbrush",
    ]
# 로컬(개발) 환경에서 적용할 환경 설정들
class LocalConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:1234@localhost:3306/flaskdb'
  SQLALCHEMY_TRACK_MODIFICATIONS=False # 변경 추적 비활성화
  SQLALCHEMY_ECHO=True # sql문 콘솔창에 띄워주는 것

# 배포환경에서 적용할 환경 설정들
class DeployConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI='배포 후 사용할 DB 주소'
  SQLALCHEMY_TRACK_MODIFICATIONS=False
  SQLALCHEMY_ECHO=False

config = {
  "local" : LocalConfig,
  "deploy" : DeployConfig
}