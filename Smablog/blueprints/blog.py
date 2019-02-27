"""
    :author: Wu
    :url: https://github.com/smasky/flask_webTheme
    :copyright: © 2019 Smasky <492109831@qq.com>
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint,request,render_template,current_app
from SmaBlog.models import Post
#在app上注册一个叫blog的蓝本
blog_bp=Blueprint('blog',__name__)

@blog_bp.route('/')
def index():
    page=request.args.get('page',1,type=int)
    per_page=current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    hot_posts=Post.query.order_by(Post.comments.desc())[:5]
    rand_posts=Post.query.order_by(Post.views.desc())[:5]
    posts=pagination.items
    print(hot_posts)
    return render_template('blog/index.html',Posts=posts,pagination=pagination,hot_posts=hot_posts,rand_posts=rand_posts)

@blog_bp.route('/posts/<int:post_id>',methods=['GET','POST'])
def show_post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('blog/post.html',Post=post)
