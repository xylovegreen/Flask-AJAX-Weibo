from utils import log
from models.todo import Todo
import functools
from routes import (
    current_user,
    login_required,
)

from flask import (
    Blueprint,
    request,
    url_for,
    jsonify,
    redirect,
)


api_todo = Blueprint('api_todo', __name__)


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
            todo_id = request.args['id']
        else:
            todo_id = request.get_json()['id']
        t = Todo.find_by(id=int(todo_id))

        if t.user_id == u.id:
            return route_function()
        else:
            return redirect(url_for('todo.index'))

    return f


@api_todo.route('/api/todo/all')
@login_required
def all():
    u = current_user()
    # todos = Todo.find_all(user_id=u.id)
    # todos = [t.json() for t in todos]
    todos = Todo.all_json()
    return jsonify(todos)


@api_todo.route('/api/todo/add', methods=['POST'])
@login_required
def add():
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里用新增加的 json 函数来获取格式化后的 json 数据
    form = request.get_json()
    # 创建一个 todo
    u = current_user()
    t = Todo(form)
    t.user_id = u.id
    t.save()
    # 把创建好的 todo 返回给浏览器
    return jsonify(t.json())


@api_todo.route('/api/todo/delete')
@login_required
@same_user_required
def delete():
    todo_id = int(request.args['id'])
    Todo.delete(todo_id)
    d = dict(
        message="成功删除 todo"
    )
    log('in delete route function', d, jsonify(d))
    return jsonify(d)


@api_todo.route('/api/todo/update', methods=['POST'])
@login_required
@same_user_required
def update():
    """
    用于增加新 todo 的路由函数
    """
    form = request.get_json()
    log('api todo update form', form)
    t = Todo.update(form)
    return jsonify(t.json())
