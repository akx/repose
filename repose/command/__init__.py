import click

from repose.command.chart import chart
from repose.command.scan import scan


@click.group()
def cli():
    pass


cli.add_command(scan)
cli.add_command(chart)

if __name__ == "__main__":
    cli()
