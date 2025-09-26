from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from apps.board.forms import WriteBoardForm
from apps.board.models import Board
from apps.app import db


bp = Blueprint(
  "board",
  __name__,
  template_folder="templates",
  static_folder="static"
)

@bp.route("/", methods=['GET'])
def index():
  posts = Board.query.order_by(Board.created_at.desc()).all()
  return render_template('board/index.html', posts= posts)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_board():
  form = WriteBoardForm()
  if form.validate_on_submit():
    board = Board(
      user_id = current_user.id,
      subject = form.subject.data,
      content = form.content.data
    )
    db.session.add(board)
    db.session.commit()
    return redirect( url_for('board.index'))
  
  return render_template('board/write.html', form = form)

@bp.route('/detail/<int:board_id>')
def detail(board_id):
  board = Board.query.get_or_404(board_id)

  return render_template('board/detail.html', board = board)

@bp.route('/edit/<board_id>', methods=['GET', 'POST'])
def edit(board_id):
  board = Board.query.get_or_404(board_id)
  form = WriteBoardForm(obj = board)
  if form.validate_on_submit():
    
    board.subject = form.subject.data
    board.content = form.content.data
    db.session.add(board)
    db.session.commit()
    return redirect( url_for ('board.index'))
  
  return render_template('board/edit,html', form = form, board = board)