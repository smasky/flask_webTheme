"""
    :author: Wu
    :url: https://github.com/smasky/flask_webTheme
    :copyright: © 2019 Smasky <492109831@qq.com>
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint,request,render_template,current_app,redirect,url_for,flash,make_response,request
from SmaBlog.models import Post,Message,Admin,PostComment,SelfComment,Itembox,Weiadmin,Weiitem,Dati,Paperday
from SmaBlog.forms import MessageForm,AdminForm,RegisterForm,PostCommentForm,SpeakForm
from SmaBlog.extensions import db,csrf
from flask_login import login_user,logout_user,login_required,current_user
from SmaBlog.utils import redirect_back,sum_comment,encrypt,decrypt
from datetime import datetime
from sqlalchemy import and_
import json
import requests

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


@blog_bp.route('/aboutme',methods=['GET','POST'])
def aboutme():

    admin_form=AdminForm()
    login(admin_form)
    return render_template('blog/aboutMe.html',adminForm=admin_form)

@blog_bp.route('/posts/<int:post_id>',methods=['GET','POST'])
def show_post(post_id):

    post=Post.query.get_or_404(post_id)
    post_coms=post.postcomments
    post.views=post.views+1
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
        admin=Admin.query.filter(Admin.email==email).first()
        if current_user.can():
            if admin:
                admin.name=username
                db.session.add(admin)
                post_com=PostComment(body=body,post_id=postId,admin_id=admin.id)
            else:
                addmin=Admin(name=username,email=email,right=3)
                db.session.add(admin)
                db.session.commit()
                admin=Admin.query.filter(Admin.email==email).first()
                post_com=PostComment(body=body,post_id=postId,admin_id=admin.id)
        else:
            if admin:
                admin.name=username
                db.session.add(admin)
                post_com=PostComment(body=body,post_id=postId,admin_id=admin.id)
            else:
                admin=Admin(name=username,email=email,right=3)
                db.session.add(admin)
                db.session.commit()
                admin=Admin.query.filter(Admin.email==email).first()
                post_com=PostComment(body=body,post_id=postId,admin_id=admin.id)
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
        if('//' not in avater):
            avater="http://q1.qlogo.cn/g?b=qq&nk={}&s=640".format(avater)
        auth_code=form.auth_code.data
        adminU=Admin.query.filter(Admin.username==username).first()
        adminE=Admin.query.filter(Admin.email==email).first()
        adminN=Admin.query.filter(Admin.name==name).first()
        if(auth_code=='3428' and adminN==None and adminE==None and adminN==None):
            admin=Admin.query.filter(Admin.email==email).first()
            if admin:
                admin.name=name
                admin.set_password(password)
                admin.right=2
                admin.avater=avater
            else:
                admin=Admin(username=username,name=name,password=password,email=email,right=2,avater=avater)
            db.session.add(admin)
            db.session.commit()
            res=make_response(redirect(url_for('blog.index')))
            res.set_cookie('name',username,max_age=30*24*3600)
            res.set_cookie('email',email,max_age=30*24*3600)
            return res
        else:
            if(not adminU):
                form.username.errors='该用户名已存在'
            elif(not adminE):
                form.email.errors='该邮箱已经注册'
            elif(not adminN):
                form.name.errors='该昵称已经被注册'
            else:
                form.auth_code.errors='激活码不正确,请重试!'
    return render_template('blog/register.html',Form=form,adminForm=admin_form)


#留言板视图
@blog_bp.route('/MessageBoard',methods=['GET','POST'])
def MessageBoard():
    page=request.args.get('page',1,type=int)
    per_page=current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Message.query.order_by(Message.timestamp.desc()).paginate(page, per_page=per_page)
    messages=pagination.items
    form=MessageForm()
    admin_form=AdminForm()
    login(admin_form)
    if form.validate_on_submit():
        Body=form.body.data
        message=Message(body=Body,admin_id=current_user.id)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('blog.MessageBoard'))
    return render_template('blog/MessageBoard.html',Form=form,Messages=messages,adminForm=admin_form,pagination=pagination)
#我的动态视图
@blog_bp.route('/speakself',methods=['GET','POST'])
def SpeakSelf():
    page=request.args.get('page',1,type=int)
    per_page=current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = SelfComment.query.order_by(SelfComment.timestamp.desc()).paginate(page, per_page=per_page)
    messages=pagination.items
    form=SpeakForm()
    admin_form=AdminForm()
    login(admin_form)
    if form.validate_on_submit() and current_user.test_right():
        Body=form.body.data
        secret=form.secret.data
        message=SelfComment(body=Body,admin_id=current_user.id,secret=secret)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('blog.SpeakSelf'))
    return render_template('blog/speakBoard.html',Form=form,Messages=messages,adminForm=admin_form,pagination=pagination)
@blog_bp.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    adminform=AdminForm()
    html=str(render_template('login_fail.html',adminForm=adminform))
    return html

def login(admin_form):
    if admin_form.validate_on_submit():
        user_name=admin_form.username.data
        password=admin_form.password.data
        admin=Admin.query.filter(Admin.username==user_name).first()
        if admin:
            if user_name==admin.username and admin.validate_password(password):
                login_user(admin,remember=False)
@blog_bp.route('/login',methods=['POST'])
def login_admin():
    name = request.values.get("name")
    pwd = request.values.get("pwd")
    if True:
        user_name=name
        password=pwd
        admin=Admin.query.filter(Admin.username==user_name).first()
        if admin:
            if user_name==admin.username and admin.validate_password(password):
                login_user(admin,remember=True)
                html=render_template('login_sucess.html')
                return str(html)
            else:
                adminform=AdminForm()
                adminform.username.errors='密码错误或用户名不存在'
                html=str(render_template('login_fail.html',adminForm=adminform))
                return html
        else:
            adminform=AdminForm()
            adminform.username.errors='用户名不存在'
            print('111')
            html=str(render_template('login_fail.html',adminForm=adminform))
            return html
    return make_response("")
@csrf.exempt
@blog_bp.route('/weixin',methods=['POST','GET'])
def weixincx():
    if request.method=='POST':
        data=request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        papercode=json_data['papercode']
        print(papercode)
        items=Itembox.query.filter(Itembox.papercode==int(papercode)).all()
        Que={}
        answerid=[]
        Que['shiti']=[]
        if(items):
            for item in items:
                qnaire={}
                answer={}
                question=item.question
                answers=item.answers
                right=item.right
                qnaire['question']=question
                print(answers)
                options=answers.split('/')
                answer['a']=options[0]
                answer['b']=options[1]
                answer['c']=options[2]
                answer['d']=options[3]
                answerid.append(item.id)
                qnaire['option']=answer
                qnaire['answer']=right
                Que['shiti'].append(qnaire)
            Que['answerid']=answerid
        else:
            Que={'error':'不存在该试题码'}
    return json.dumps(Que,ensure_ascii=False)

@csrf.exempt
@blog_bp.route('/loginweixin',methods=['POST','GET'])
def loginweixin():
    if request.method=='POST':
        appID='wxd7def1e0e031ba47'
        appSecret='ec2b6482408a8c8e9d0ed36a743acbd4'
        data=request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        code=json_data['code']
        try:
            url='https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(appID,appSecret,code)
            req=requests.get(url)
            openid=req.json()['openid']
        except BaseException as e:
            if(json_data['hash']):
                openid=decrypt(5,hash)
        weixin=Weiadmin.query.filter(Weiadmin.openid==openid).first()
        code=encrypt(5,openid)
        print(openid)
        if(not weixin):
            data={'message':1,'code':code}
        else:
            data={'message':0,'code':code}
    json_data=json.dumps(data)
    print(json_data)
    return json_data
@csrf.exempt
@blog_bp.route('/registerweixin',methods=['POST','GET'])
def registerweixin():
    if request.method=='POST':
        data=request.get_data()
        data= json.loads(data.decode("utf-8"))
        username=data.get('username')
        truename=data.get('truename')
        code=data.get('code')
        openid=decrypt(5,code)
        print(openid)
        years=data.get('years')
        ifstudent=data.get('ifstudent')
        weixin=Weiadmin(openid=openid,username=username,truename=truename,year=years,ifstudent=ifstudent)
        db.session.add(weixin)
        db.session.commit()
    data={'message':1}
    return json.dumps(data)

@csrf.exempt
@blog_bp.route('/datiweixin',methods=['POST','GET'])
def datiweixin():
    if request.method=='POST':
        data=request.get_data()
        data= json.loads(data.decode("utf-8"))
        ranks=data.get('rank')
        answers=data.get('answers')
        papercode=data.get('paperid')
        answerid=data.get('answerid')
        right=data.get('right')
        code=data.get('code')
        openid=decrypt(5,code)
        admin_id=Weiadmin.query.filter(Weiadmin.openid==openid).first().id

        stranswer=' '.join(answers)

        num=len(answerid)
    
        paperday_id=Paperday.query.filter(Paperday.paperdaycode==papercode).first().id
        weiitem=Weiitem.query.filter(and_(Weiitem.weiadmin_id==admin_id,Weiitem.paperday_id==paperday_id)).first()
        if(not weiitem):
            weiitem=Weiitem(weiadmin_id=admin_id,paperday_id=paperday_id,answers=stranswer,rank=ranks)
            db.session.add(weiitem)
            db.session.commit()
            weiitem=Weiitem.query.filter(and_(Weiitem.weiadmin_id==admin_id,Weiitem.paperday_id==paperday_id)).first()
            weiitem_id=weiitem.id
            for i in range(num):
                answer_id=answerid[i]
                subanswerid=answerid[i]
                itembox=Itembox.query.filter(Itembox.id==subanswerid).first()
                itembox_id=itembox.id
                subanswer=answers[i]
                subright=right[i]
                if(subright):
                    subright=True
                else:
                    subright=False
                dati=Dati(itembox_id=itembox_id,right=subright,answer=subanswer,weiitem_id=weiitem_id)
                db.session.add(dati)
            db.session.commit()
            data={'message':'今日答题成功！','suc':True}
        else:
            data={'message':'请勿重复答题哦！','suc':False}
    return json.dumps(data)
    


