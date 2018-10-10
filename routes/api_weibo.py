from routes import (
    current_user,
    login_required,
)
from models.weibo import Weibo
from utils import log
from models.comment import Comment
import functools

from flask import (
    Blueprint,
    request,
    url_for,
    jsonify,
    redirect,
)


api_weibo = Blueprint('api_weibo', __name__)


def same_user_required(route_function):
    """
    装饰器
    用户身份验证
    """
    @functools.wraps(route_function)
    def f():
        log('same_user_required')
        u = current_user()
        if 'id' in request.args:
            weibo_id = request.args['id']
        else:
            weibo_id = request.get_json()['id']
        w = Weibo.find_by(id=int(weibo_id))
        log(weibo_id, u.id, w.user_id)
        if w.user_id == u.id:
            return route_function()
        else:
            return redirect(url_for('weibo.index'))

    return f


@api_weibo.route('/api/weibo/all')
@login_required
def all():
    """
    weibo 首页的路由函数
    """
    weibo_list = []
    weibos = Weibo.all()
    for weibo in weibos:
        form = weibo.json()
        comments = Comment.find_all(weibo_id=int(form['id']))
        comments = [comment.json() for comment in comments]
        form['comments'] = comments
        weibo_list.append(form)
    log('json weibo_list in weibo all', weibo_list)
    return jsonify(weibo_list)


@api_weibo.route('/api/weibo/add', methods=['POST'])
@login_required
def add():
    # 得到浏览器发送的表单，浏览器用 Ajax 发送 json 格式的数据过来
    # 所以这里用新增加的 json 函数来获取格式化后的 json 数据
    form = request.get_json()
    # 创建一个 weibo
    w = Weibo(form)
    u = current_user()
    w.user_id = u.id
    w.save()
    # 把创建好的 weibo 返回给浏览器
    return jsonify(w.json())


@api_weibo.route('/api/weibo/delete')
@login_required
@same_user_required
def delete():
    weibo_id = int(request.args['id'])
    Weibo.delete(weibo_id)
    comments = Comment.find_all(weibo_id=weibo_id)
    for c in comments:
        Comment.delete(c.id)
    d = dict(
        message="成功删除 weibo"
    )
    return jsonify(d)


@api_weibo.route('/api/weibo/update', methods=['POST'])
@login_required
@same_user_required
def update():
    """
    用于增加新 Weibo 的路由函数
    """
    form = request.get_json()
    log('api weibo update form', form)
    w = Weibo.update(form)
    return jsonify(w.json())
