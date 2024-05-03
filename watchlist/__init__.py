import sys, os

# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from watchlist.watchlist import app

# 数据库配置
WIN = sys.platform.startswith('win')
if WIN:  # 如果是Windows系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app.secret_key = ['dev']
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'  # 添加@required装饰器后未登录用户访问页面重定向到 login 界面
login_manager.login_message = '请登录管理员账户！'  # 并显示错误消息提示


@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user


@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)


# 为了避免循环依赖（A 导入 B，B 导入 A），我们把这一行导入语句放到构造文件的结尾。同样的，load_user() 函数和 inject_user() 函数中使用的模型类也在函数内进行导入。
from watchlist import views, errors, commands
