from simplecls.command.aliased_group import AliasedGroup
from simplecls.command.train import train
from simplecls.command.evaluate import evaluate
from simplecls.command.test import test
from simplecls.command.make_dataset import make
from simplecls.command.data_transform import transform
from simplecls.command.visual_model import visual
from simplecls.command.generate import generate
from simplecls.command.export import export
import click


__all__ = ['cli']

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
def cli():
    pass


cli.add_command(train)
cli.add_command(evaluate)
cli.add_command(test)
cli.add_command(make)
cli.add_command(transform)
cli.add_command(visual)
cli.add_command(generate)
cli.add_command(export)

if __name__ == '__main__':
    cli()
