from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,IntegerField
from wtforms.validators import DataRequired,Length,Email,ValidationError

class MessageForm(FlaskForm):
    body=TextAreaField('评论:',validators=[DataRequired(),Length(1,200)])
    submit=SubmitField('提交评论')

class AdminForm(FlaskForm):
    username=StringField('用户名:',validators=[DataRequired(),Length(1,20)])
    password=PasswordField('密码:',validators=[DataRequired(),Length(1,20)])
    submit=SubmitField('登录')

class RegisterForm(FlaskForm):
    username=StringField('用户名:',validators=[DataRequired(),Length(1,20)])
    password=PasswordField('密码:',validators=[DataRequired(),Length(1,20)])
    name=StringField('昵称:',validators=[DataRequired(),Length(1,20)])
    email=StringField('邮箱:',validators=[DataRequired(),Email()])
    avater=StringField('头像地址:')
    web=StringField('网站地址',default='')
    auth_code=StringField('邀请码:',validators=[DataRequired(),Length(4,5)])
    submit=SubmitField('确定')

class PostCommentForm(FlaskForm):
    username=StringField('昵称:',validators=[DataRequired(),Length(1,20)])
    email=StringField('邮箱:',validators=[DataRequired(),Email()])
    body=TextAreaField('评论:',validators=[DataRequired(),Length(1,200)])
    submit=SubmitField('确定')
