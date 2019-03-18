"""
    :author: Wu
    :url: https://github.com/smasky/flask_webTheme
    :copyright: © 2019 Smasky <492109831@qq.com>
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint,request,render_template,current_app,redirect,url_for,flash,make_response,request
from SmaBlog.models import Post,Message,Admin,PostComment
from SmaBlog.forms import MessageForm,AdminForm,RegisterForm,PostCommentForm
from SmaBlog.extensions import db
from flask_login import login_user,logout_user,login_required,current_user
from SmaBlog.utils import redirect_back,sum_comment
from datetime import datetime
#在app上注册一个叫blog的蓝本
blog_bp=Blueprint('blog',__name__)

@blog_bp.route('/',methods=['GET','POST'])
def index():
    page=request.args.get('page',1,type=int)
    per_page=current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts=pagination.items
    print('a')
    admin_form=AdminForm()
    login(admin_form)

    return render_template('blog/index.html',Posts=posts,pagination=pagination,adminForm=admin_form)



@blog_bp.route('/posts/<int:post_id>',methods=['GET','POST'])
def show_post(post_id):
    post=Post.query.get_or_404(post_id)
    post_coms=post.postcomments
    post.views=post.views+1
    print(post.views)
    admin_form=AdminForm()
    login(admin_form)
    if request.cookies.get('name'):
        username=request.cookies.get('name')
        email=request.cookies.get('email')
        form=PostCommentForm(username=username,email=email)
    elif current_user.can():
        form=PostCommentForm(username=current_user.name,email=current_user.email)
    else:
        form=PostCommentForm()
    if form.validate_on_submit() :
        username=form.username.data
        body=form.body.data
        email=form.email.data
        postId=post_id
        if current_user.can():
            post_com=PostComment(name=username,body=body,post_id=postId,email=email,avater=current_user.avater)
        else:
            post_com=PostComment(name=username,body=body,post_id=postId,email=email)
        post.comments+=1
        db.session.add(post_com)
        db.session.commit()
        if not request.cookies.get('name'):
            res=make_response(redirect(url_for('blog.show_post',post_id=post_id)))
            res.set_cookie('name',username,max_age=30*24*3600)
            res.set_cookie('email',email,max_age=30*24*3600)
            return res
        return redirect(url_for('blog.show_post',post_id=post_id))
    db.session.commit()
    return render_template('blog/post.html',Post=post,adminForm=admin_form,PostCom=post_coms,Form=form)
#注册视图
@blog_bp.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    admin_form=AdminForm()
    login(admin_form)
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        name=form.name.data
        email=form.email.data
        avater=form.avater.data
        auth_code=form.auth_code.data
        if(auth_code=='3428'):
            admin=Admin(username=username,name=name,password=password,email=email,right=2,avater=avater)
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
    if current_user.can():
        form=MessageForm(name=current_user.name)
        form.name.data=current_user.name
    else:
        form=MessageForm()

    admin_form=AdminForm()
    login(admin_form)
    if form.validate_on_submit():
        Name=form.name.data
        Body=form.body.data
        message=Message(name=Name,body=Body,admin_id=current_user.id)
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
        print(user_name)
        password=admin_form.password.data
        admin=Admin.query.filter(Admin.username==user_name).first()
        if admin:
            if user_name==admin.username and admin.validate_password(password):
                login_user(admin,remember=False)
                print('121')
