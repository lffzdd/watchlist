from flask import request, redirect, url_for, flash, render_template
from flask_login import current_user, login_required, login_user, logout_user

from watchlist import app, db
from watchlist.models import Movie, User


@app.route('/', methods=['GET', 'POST'])  # 都得设置 methods
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) != 4:
            flash('输入错误，请重新输入！')
            return redirect(url_for('index'))

        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('已添加电影！')

        return redirect(url_for('index'))

    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


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
        flash(f'ID[{movie.id}]数据已更新！')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required  # 登录保护，不允许未登录用户访问
def delete(movie_id):
    """删除页面"""
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash(f'《{movie.title}》已删除！')
    return redirect(url_for('index'))


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
        username = request.form['username']

        if not username or len(username) > 20:
            flash('Invalid input')
            return redirect(url_for('settings'))

        current_user.username = username
        db.session.commit()
        flash('Settings updated.\n设置更新')
        return redirect(url_for('index'))

    return render_template('settings.html')
