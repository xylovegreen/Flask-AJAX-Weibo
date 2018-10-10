import functools
from models.session import Session
from models.user import User
from utils import log

import random
import json

from flask import (
    request,
    redirect,
    url_for,
)


def random_string():
    """
    生成一个随机的字符串
    """
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def current_user():
    log('session_id in current_user()', request.cookies)
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        s = Session.find_by(session_id=session_id)
        if s is None or s.expired():
            return User.guest()
        else:
            user_id = s.user_id
            u = User.find_by(id=user_id)
            return u
    else:
        return User.guest()


def login_required(route_function):
    """
    装饰器
    用于用户登陆验证
    """

    @functools.wraps(route_function)
    def f():
        log('login_required')
        u = current_user()
        if u.is_guest():
            log('游客用户')
            return redirect(url_for('user.login_view'))
        else:
            log('登录用户', route_function)
            return route_function()

    return f
