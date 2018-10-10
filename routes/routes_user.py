from urllib.parse import unquote_plus

from models.session import Session
from routes import (
    current_user,
    random_string,
)

from utils import log
from models.user import User


from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    current_app,
)

user = Blueprint('user', __name__)


@user.route('/user/login', methods=['POST'])
def login():
    """
    登录页面的路由函数
    """
    form = request.form
    log('form in post login', form)
    u, result = User.login(form)
    log('u in login post request', u)
    if not u.is_guest():
        session_id = random_string()
        form = dict(
            session_id=session_id,
            user_id=u.id,
        )
        Session.new(form)

        redirect_to_index = redirect('/user/login/view?result={}'.format(result))
        response = current_app.make_response(redirect_to_index)
        response.set_cookie('session_id', value=session_id)

        return response
    else:
        return redirect('/user/login/view?result={}'.format(result))


@user.route('/user/login/view')
def login_view():
    u = current_user()
    result = request.args.get('result', '')
    result = unquote_plus(result)
    return render_template(
        'login.html',
        username=u.username,
        result=result,
    )


@user.route('/user/register', methods=['POST'])
def register():
    """
    注册页面的路由函数
    """
    form = request.form

    u, result = User.register(form)
    log('register post', result)

    return redirect('/user/register/view?result={}'.format(result))


@user.route('/user/register/view')
def register_view():
    result = request.args.get('result', '')
    result = unquote_plus(result)

    return render_template('register.html', result=result)


