"""
    :author: Wu
    :url: https://github.com/smasky/flask_webTheme
    :copyright: © 2019 Smasky <492109831@qq.com>
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint,request,render_template,current_app,redirect,url_for
from SmaBlog.models import Post,Message
from SmaBlog.utils import cal_days
from SmaBlog.forms import MessageForm
from SmaBlog.extensions import db
#在app上注册一个叫blog的蓝本
blog_bp=Blueprint('blog',__name__)

@blog_bp.route('/')
def index():
    post_info={}
    page=request.args.get('page',1,type=int)
    per_page=current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    hot_posts=Post.query.order_by(Post.comments.desc())[:5]
    rand_posts=Post.query.order_by(Post.views.desc())[:5]
    posts=pagination.items
    post_info['number']=Post.query.count()
    post_info['days_from_s']=str(cal_days())+'天'
    print(hot_posts)
    return render_template('blog/index.html',Posts=posts,Post_info=post_info,pagination=pagination,hot_posts=hot_posts,rand_posts=rand_posts)

@blog_bp.route('/posts/<int:post_id>',methods=['GET','POST'])
def show_post(post_id):
    post_info={}
    post_info['number']=Post.query.count()
    post_info['days_from_s']=str(cal_days())+'天'
    post=Post.query.get_or_404(post_id)
    return render_template('blog/post.html',Post=post,Post_info=post_info)

#留言板视图
@blog_bp.route('/MessageBoard',methods=['GET','POST'])
def MessageBoard():
    messages=Message.query.order_by(Message.timestamp.desc()).all()
    form=MessageForm()
    ###############
    post_info={}
    post_info['number']=Post.query.count()
    post_info['days_from_s']=str(cal_days())+'天'
    ########################
    if form.validate_on_submit():
        Name=form.name.data
        Body=form.body.data
        message=Message(name=Name,body=Body)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('blog.MessageBoard'))
    return render_template('blog/MessageBoard.html',Form=form,Messages=messages,Post_info=post_info)
