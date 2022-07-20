import click
from click_default_group import DefaultGroup

print("running - https://stackoverflow.com/questions/52053491/a-command-without-name-in-click")
@click.group(cls=DefaultGroup, default='foo', default_if_no_args=True)
def cli():
    print("group execution")

@cli.command()
@click.option('--config', default=None)
def foo(config):
    click.echo('foo execution')
    if config:
        click.echo(config)

