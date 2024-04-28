import click


@click.command()
@click.option('--count', default=1, help='打招呼的次数')
@click.option('--name', prompt='你的名字', help='打招呼的人')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for i in range(count):
        click.echo(f'Hello {name}')


hello()
# python click.py --count 5 --name 刘非凡
