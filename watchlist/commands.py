import click
from faker import Faker

from watchlist import app, db
from watchlist.models import User, Movie


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """初始化数据库"""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialzed database.')


@app.cli.command()
def forge():
    # user = User(name=‘User’,username='lff')
    # db.session.add(user)
    fake = Faker()
    for i in range(15):
        movie = Movie(title=fake.catch_phrase(), year=fake.year())
        db.session.add(movie)

    db.session.commit()
    click.echo('已生成数据！')


@app.cli.command()
@click.option('--user', help='管理员用户名')
@click.option('--password', hide_input=True, confirmation_prompt=True, help='管理员密码')
def admin(username, password):
    user = User.query.first()
    if user is not None:
        click.echo('更新用户名：')
        user.username = username
        user.set_password(password)
    else:
        click.echo('创建用户名：')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('管理员更新完毕！')


