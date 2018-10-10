from routes.routes_public import public
from routes.routes_user import user
from routes.routes_todo import todo
from routes.api_todo import api_todo
from routes.routes_weibo import weibo
from routes.api_weibo import api_weibo
from routes.api_comment import api_comment

from flask import (
    Flask,
)

app = Flask(__name__)

app.register_blueprint(public)
app.register_blueprint(user)
app.register_blueprint(todo)
app.register_blueprint(api_todo)
app.register_blueprint(weibo)
app.register_blueprint(api_weibo)
app.register_blueprint(api_comment)

# 运行服务器
if __name__ == '__main__':
    # debug 模式可以自动加载代码的变动, 不用重启程序
    config = dict(
        debug=False,
        host='0.0.0.0',
        port=3000,
    )
    # app.run() 开始运行服务器
    app.run(**config)
