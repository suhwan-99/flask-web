from flask import Flask, render_template, redirect, url_for, request, flash
from email_validator import validate_email, EmailNotValidError
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message
import os # 환경변수 안에 값들을 꺼내오기 위한 import

app = Flask(__name__)

# flash 메세지는 세션을 이용해서 서버 > 클라이언트로 메세지를 전달
# 세션은 클라이언트 측에서 관리하므로 보안상 암호화가 필요
# flask 는 세션 데이터를 안전하게 암호화 하고 서명하는데 비밀키를 사용
app.config['SECRET_KEY'] = '1234'

# 디버그툴바가 리다이렉트를 가로채고 중단시키는걸 방지
app.config['DEBUG_TB_INTERCEPT-REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

# flask_Mail 에 필요한 환경설정
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)

@app.route('/')
def index():
  return "hello flask"

@app.route('/hello/<name>')
def hello(name):
  return render_template('index.html', name=name)

@app.route('/contact')
def contact():
  return render_template('contact.html')

@app.route('/contact/complete', methods=['POST', 'GET'])
def complete():
  if request.method == 'POST':
    username = request.form.get('username')
    email = request.form['email']
    description = request.form['description']

    is_vali = True
    if not username:
      flash('사용자 이름 필수.')
      is_vali = False

    if not email:
      flash('이메일 필수.')
      is_vali = False

    if not description:
      flash('문의 내용은 필수.')
      is_vali = False

    try:
      validate_email(email)
    except EmailNotValidError:
      flash('메일 형식이 아닙니다')
      is_vali = False

    except Exception:
      print('......알 수 없는 오류......')

    # 유효성 검사 실패 시 다시 문의 페이지로 리다이렉트
    if not is_vali:
      return redirect( url_for ('contact'))
    
    send_mail(email, "문의 내용 확인", "contact_mail", username=username, description=description)

    # 문의 완료시 리다이렉트
    return redirect ( url_for ('complete') )
  
  # 겟 요청시 페이지 렌더링
  return render_template('contact_complete.html')

# @app.route('/contact/complete', methods=['POST'])
# def send():
#   # 전송 기능 구현 예정
#   print('=====문의 전송 기능 실행=======')
#   return redirect( url_for ('complete') )

def send_mail(to, subject, template, **kwagrs):
  msg = Message(subject, recipients=[to])
  msg.body = render_template(template + ".txt", **kwagrs)
  msg.html = render_template(template + ".html", **kwagrs)
  mail.send(msg)
  