from routes import (
    current_user,
)

from flask import (
    Blueprint,
    request,
    render_template,
    send_from_directory,
)

public = Blueprint('public', __name__)


@public.route('/')
def index():
    """
    主页的处理函数, 返回主页的响应
    """
    u = current_user()
    return render_template('index.html', username=u.username)


@public.route('/static')
def static():
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.args['file']
    return send_from_directory('static', filename)