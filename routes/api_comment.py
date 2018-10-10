from routes import (
    current_user,
    login_required,
)

from models.weibo import Weibo
from utils import log
from models.comment import Comment

from flask import (
    Blueprint,
    request,
    url_for,
    jsonify,
    redirect,
)

import functools

api_comment = Blueprint('api_comment', __name__)


def same_user_required(route_function):
    """
    装饰器
    用于用户身份验证
    """
    @functools.wraps(route_function)
    def f():
        log('same_user_required')
        u = current_user()
        if 'id' in request.args:
            comment_id = request.args['id']
        else:
            comment_id = request.get_json()['id']
        c = Comment.find_by(id=int(comment_id))
        w = Weibo.find_by(id=int(c.weibo_id))
        log(comment_id, u.id, c.user_id)
        if c.user_id == u.id or w.user_id == u.id:
            return route_function()
        else:
            return redirect(url_for('weibo.index'))

    return f


@api_comment.route('/api/comment/add', methods=['POST'])
@login_required
def add():
    # 得到浏览器发送的表单，浏览器用 Ajax 发送 json 格式的数据过来
    # 所以这里用新增加的 json 函数来获取格式化后的 json 数据
    form = request.get_json()
    # 创建一个 comment
    c = Comment(form)
    u = current_user()
    c.user_id = u.id
    c.save()
    # 把创建好的 comment 返回给浏览器
    return jsonify(c.json())


@api_comment.route('/api/comment/delete')
@login_required
@same_user_required
def delete():
    comment_id = int(request.args['id'])
    log('delete comment', comment_id)
    Comment.delete(comment_id)
    d = dict(
        message="成功删除 comment"
    )
    return jsonify(d)


@api_comment.route('/api/comment/update', methods=['POST'])
@login_required
@same_user_required
def update():
    """
    用于增加新 comment 的路由函数
    """
    form = request.get_json()
    log('api comment update form', form)
    w = Comment.update(form)
    return jsonify(w.json())