#!/usr/bin/env python3
import sys 
from mastertext.objectstore import TextObjectStore
from mastertext.etl import inject_file, crawl_dir
import click

ts = TextObjectStore()

@click.group()
def cli():
    pass

@cli.command()
@click.argument('hash')
@click.option('--attribs', default=False, help='Display Extended Attributes')
def get(hash, attribs):
    """
    Retrevie a document object from the database by it's
    hashid.
    """
    tso = ts.retrieve_object(hash, attribs=False)
    if attribs:
        click.echo("Attributes are not supported yet")
        click.echo(tso)
    else:
        click.echo(tso)

@cli.command()
@click.argument('fts5term')
def search(fts5term):
    search_id = ts.search_text(fts5term)
    click.echo(search_id)
    il = search_id['ids']
    for i in il:
        click.echo(i)
    click.echo(search_id['count'])

if __name__ == '__main__':
    cli()


        