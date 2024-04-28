# 数据库

# # 数据库配置
import os
import sys

import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#
# WIN = sys.platform.startswith('win')
# if WIN:  # 如果是 Windows 系统，使用三个斜线
#     prefix = 'sqlite:///'
# else:  # 否则使用四个斜线
#     prefix = 'sqlite:////'
#
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# # 在扩展类实例化前加载配置
db = SQLAlchemy(app)


# 创建数据库模型
class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


# # 创建数据库表
# (env) $ flask shell
# >>> from app import db
# >>> db.create_all()
# >>> db.drop_all()
# >>> db.create_all()

# 自定义命令initdb
import Click


@app.cli.command()  # 注册为命令，可以传入name参数来自定义
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    '''Initialize the database.'''
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


from app import User, Movie  # 导入模型类

user = User(name='Jian Li')  # 创建一个User记录
m1 = Movie(title='Leon', year='1994')
m2 = Movie(title='Mahjong', year='1996')
db.session.add(user)  # 把新创建的记录添加到数据库会话
db.session.add(m1)
db.session.add(m2)
db.session.commit()  # 提交数据库会话，只需要在最后调用一次即可
