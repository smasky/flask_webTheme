"""
    :author: Wu
    :url: https://github.com/smasky/flask_webTheme
    :copyright: © 2019 Smasky <492109831@qq.com>
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint,request,render_template,current_app,redirect,url_for,flash
from SmaBlog.models import Post,Message,Admin
from SmaBlog.forms import MessageForm,AdminForm,RegisterForm
from SmaBlog.extensions import db
from flask_login import login_user,logout_user,login_required
from SmaBlog.utils import redirect_back
#在app上注册一个叫blog的蓝本
blog_bp=Blueprint('blog',__name__)

@blog_bp.route('/',methods=['GET','POST'])
def index():
    page=request.args.get('page',1,type=int)
    per_page=current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts=pagination.items

    admin_form=AdminForm()
    login(admin_form)
    return render_template('blog/index.html',Posts=posts,pagination=pagination,adminForm=admin_form)



@blog_bp.route('/posts/<int:post_id>',methods=['GET','POST'])
def show_post(post_id):
    post=Post.query.get_or_404(post_id)
    admin_form=AdminForm()
    login(admin_form)

    return render_template('blog/post.html',Post=post,adminForm=admin_form)
#注册视图
@blog_bp.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    admin_form=AdminForm()
    login(admin_form)
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.email.data
        auth_code=form.auth_code.data
        if(auth_code=='3428'):
            admin=Admin(username=username,password=password,email=email,right=2)
            db.session.add(admin)
            db.session.commit()
            return redirect(url_for('blog.index'))
        else:
            form.auth_code.errors='激活码不正确,请重试!'
    return render_template('blog/register.html',Form=form,adminForm=admin_form)


#留言板视图
@blog_bp.route('/MessageBoard',methods=['GET','POST'])
def MessageBoard():
    messages=Message.query.order_by(Message.timestamp.desc()).all()
    form=MessageForm()

    admin_form=AdminForm()
    login(admin_form)

    if form.validate_on_submit():
        Name=form.name.data
        Body=form.body.data
        message=Message(name=Name,body=Body)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('blog.MessageBoard'))
    return render_template('blog/MessageBoard.html',Form=form,Messages=messages,adminForm=admin_form)

@blog_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('blog.index'))

def login(admin_form):
    if admin_form.validate_on_submit():
        user_name=admin_form.username.data
        password=admin_form.password.data
        admin=Admin.query.filter(Admin.username==user_name).first()
        if admin:
            if user_name==admin.username and admin.validate_password(password):
                login_user(admin,remember=False)
                print('121')
