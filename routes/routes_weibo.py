from flask import (
    Blueprint,
    render_template,
)

from routes import (
    login_required,
)

weibo = Blueprint('weibo', __name__)


@weibo.route('/weibo/index')
@login_required
def index():
    """
    weibo 首页的路由函数
    """
    return render_template('weibo_index.html')


