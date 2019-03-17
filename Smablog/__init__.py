"""
    :author: Wu
    :url: https://github.com/smasky/flask_webTheme
    :copyright: © 2019 Smasky <492109831@qq.com>
    :license: MIT, see LICENSE for more details.
"""
import click
from flask import Flask,render_template
from .models import Admin,Post
from .blueprints.blog import blog_bp
from .settings import config
from .extensions import db,bootstrap,moment,csrf,login,Guest
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
    register_template_context(app)

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
    moment.init_app(app)
    csrf.init_app(app)
    login.init_app(app)
    login.anonymous_user=Guest


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
    @click.option('--filename',help='add new post into db')
    def addpost(filename):
        from .loading_post import loading_post
        click.echo(filename)
        loading_post(filename)
        click.echo('done.')


    @app.cli.command()
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    def forge(post):
        """Generate fake data."""
        from .fakes import  fake_posts

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Done.')

    @app.cli.command()
    @click.option('--message',default=50,help='Quantity of message,default is 50.')
    def forge_m(message):
        from .fakes import fake_message
        db.create_all()
        click.echo('Generatinf %d message...' % message)
        fake_message(message)

        click.echo('Done')

    @app.cli.command()
    @click.option('--username',prompt=True,help='The username to login')
    @click.option('--password',prompt=True,help='login password',hide_input=True,confirmation_prompt=True)
    @click.option('--right',prompt=True,help='right')
    def init(username,password,right):
        """init blog admin"""

        click.echo('create blog admin')
        db.create_all()

        admin=Admin.query.first()

        if admin:
            click.echo('admin already exists')
            admin.username=username
            admin.set_password(password)
        else:
            admin=Admin(username=username,right=right)
            admin.set_password(password)
            db.session.add(admin)
        db.session.commit()
        click.echo('Done')
def register_template_context(app):
    @app.context_processor
    def inject_right():
        from SmaBlog.utils import cal_days
        post_info={}
        hot_posts=Post.query.order_by(Post.comments.desc())[:5]
        rand_posts=Post.query.order_by(Post.views.desc())[:5]
        post_info['number']=Post.query.count()
        post_info['days_from_s']=str(cal_days())+'天'
        return dict(Post_info=post_info,hot_posts=hot_posts,rand_posts=rand_posts)
