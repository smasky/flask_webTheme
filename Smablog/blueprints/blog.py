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
    pagination=Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=per_page)
    posts=pagination.items
    return render_template('blog/index.html',Posts=posts,pagination=pagination)
