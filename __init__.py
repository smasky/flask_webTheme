"""
    :author: Wu
    :url: https://github.com/smasky/flask_webTheme
    :copyright: © 2019 Smasky <492109831@qq.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import Flask,render_template

from .blueprints.blog import blog_bp
from .settings import config
def create_app(config_name=None):
'''
    创建app主体文件
'''
    app=Flask('skyBlog')

    app.config.from_object(config[config_name])
    return app


def register_blueprints(app):
'''
    为app注册路由
'''
    app.register_blueprint(blog_bp)

