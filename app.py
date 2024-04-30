import os.path
import sys

import click
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, url_for, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from markupsafe import escape

# 数据库配置
WIN = sys.platform.startswith('win')
if WIN:  # 如果是Windows系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)  # type:Flask
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app


# 创建数据库模型
class User(db.Model, UserMixin):  # 表名将会是 user（自动生成，小写处理）
    # 继承mixin会让 User 类拥有几个用于判断认证状态的属性和方法
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 哈希散列值

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


# (env) $ flask shell
# >>> from app import db
# >>> db.create_all()
# >>> db.drop_all()
# >>> db.create_all()

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """初始化数据库"""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialzed database.')


@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}


# 一个视图函数也可以绑定多个 URL，这通过附加多个装饰器实现
@app.route('/')
@app.route('/home')
def hello():  # put application's code here
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'


'''
注意 用户输入的数据会包含恶意代码，所以不能直接作为响应返回，需要使用 MarkupSafe（Flask 的依赖之一）提供的 escape() 函数对 name 变量进行转义处理，比如把 < 转换成 &lt;。这样在返回响应时浏览器就不会把它们当做代码执行。
# 对于 URL 变量，Flask 支持在 URL 规则字符串里对变量设置处理器，对变量进行预处理。比如 /user/<int:number> 会将 URL 中的 number 部分转换成整型。
# @app.route('/hello', methods=['GET', 'POST']) 只处理GET和POST方法
'''


# @app.route('/user/<name>')
# def user_page(name):
#     return 'User page'
@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'


@app.route('/test')
def test_url_for():
    # 下面是一些调用示例（请访问 http://localhost:5000/test 后在命令行窗口查看输出的 URL）：
    print(url_for('hello'))  # 生成 hello 视图函数对应的 URL，将会输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    print(url_for('user_page', name='peter'))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'


# 定义虚拟数据
@app.cli.command()
def forge():
    """Generate fake data."""
    name = '刘非凡'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')


@app.cli.command()
@click.option('--username', prompt=True, help='管理员用户名')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='管理员密码')
def admin(username, password):
    """生成管理员账户"""
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo('Done')


# base模板页面
@app.route('/base')
def bh():
    return render_template('base.html')


@app.route('/index', methods=['GET', 'POST'])
# type: Flask
def index():
    """ index 页面 """
    if request.method == 'POST':
        '''创建电影条目'''

        if not current_user.is_authenticated:  # 如果未登录
            return redirect(url_for('index'))
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) != 4 or len(title) > 60:  # 若数据为空或长度错误
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()
        flash('提交成功！')  # flash() 函数在内部会把消息存储到 Flask 提供的 session 对象里。session 用来在请求间存储数据，它会把数据签名后存储到浏览器的 Cookie 中

        return redirect(url_for('index'))

    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    """编辑页面"""
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(title) > 60 or len(year) != 4:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('数据已更新！')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required  # 登录保护，不允许未登录用户访问
def delete(movie_id):
    """删除页面"""
    movie = Movie.query.get_or_404(movie_id)
    title = movie.title
    db.session.delete(movie)
    db.session.commit()
    flash(f'《{title}》已删除！')
    return redirect(url_for('index'))


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    """ 404 处理页面 """
    return render_template('404.html'), 404  # 返回模板和状态码


login_manager = LoginManager(app)
login_manager.login_view = 'login'  # 添加@required装饰器后未登录用户访问页面重定向到 login 界面
login_manager.login_message = '请登录管理员账户！'  # 并显示错误消息提示


@login_manager.user_loader
def load_user(user_id):  # 创建一个用户加载回调函数，用于根据用户 ID 加载用户对象
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('请输入用户名和密码！')
            return redirect(url_for('login'))
        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户，将用户对象加载到了会话中，这样在整个会话期间，Flask 就知道当前用户是谁了。
            flash('Login success.\n登录成功')
            return redirect(url_for('index'))
        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required  # 用于视图保护
def logout():
    """登出页面"""
    logout_user()
    flash('已退出登录')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])  # 没写method报错：Method Not Allowed
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input')
            return redirect(url_for('settings'))

        current_user.name = name
        db.session.commit()
        flash('Settings updated.\n设置更新')
        return redirect(url_for('index'))

    return render_template('settings.html')


if __name__ == '__main__':
    # from waitress import serve

    # serve(app, host="0.0.0.0", port=8080)
    app.run()
