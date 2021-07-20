import click

from repose.chart import generate_chart_data, generate_streamchart
from repose.command.utils import validate_resolution
from repose.db import ReposeDB


@click.option("-r", "--resolution", callback=validate_resolution, default=None)
@click.option("-o", "--output", default="chart.html")
@click.argument("database", required=True)
@click.command()
def chart(database, resolution, output):
    db = ReposeDB(database)
    chart_data = generate_chart_data(db, resolution)
    streamchart = generate_streamchart(chart_data)
    streamchart = streamchart.interactive()
    streamchart.save(output)
