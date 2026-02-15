from src.analyzer import ProteinAnalyzer
from pathlib import Path
import click

@click.group()
def cli():
    pass



@click.command()
@click.argument("filename", type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path))
def parse(filename):
    protan = ProteinAnalyzer(filename)
    protan.parse()

@click.command()
@click.argument("filename", type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path))
@click.option('-o', '--output', type=click.Path(dir_okay=False, writable=True, path_type=Path))
# @click.option('-f', '--format', type=click.Choice(['text', 'csv', 'json']), default='text', help='Output format')
def stats(filename, output):
    protan = ProteinAnalyzer(filename)
    if output:
        with open(output, 'w') as f:
            f.write(str(protan.get_stats()))
    else:
        click.echo(protan.get_stats())

cli.add_command(parse)
cli.add_command(stats)

if __name__ == '__main__':
    cli()