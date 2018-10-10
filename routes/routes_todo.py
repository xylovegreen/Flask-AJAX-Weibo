from routes import (
    login_required,
)

from flask import (
    Blueprint,
    render_template,
)

todo = Blueprint('todo', __name__)


@todo.route('/todo/index')
@login_required
def index():
    """
    todo 首页的路由函数
    """
    return render_template('todo_index.html')
