"""
    :author: Wu
    :url: https://github.com/smasky/flask_webTheme
    :copyright: © 2019 Smasky <492109831@qq.com>
    :license: MIT, see LICENSE for more details.
"""
import click
from flask import Flask,render_template

from .blueprints.blog import blog_bp
from .settings import config
from .extensions import db,bootstrap
'''
创建app主体文件
'''
def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app=Flask('skyBlog')
    register_commands(app)
    register_blueprints(app)
    register_extensions(app)
    
    app.config.from_object(config[config_name])
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    return app

'''
    为app注册路由
'''
def register_blueprints(app):
    app.register_blueprint(blog_bp)


def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    def forge(post):
        """Generate fake data."""
        from .fakes import  fake_posts

        db.drop_all()
        db.create_all()

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Done.')
