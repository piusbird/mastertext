#!/usr/bin/env python3
import sys 
from mastertext.objectstore import TextObjectStore
from mastertext.etl import inject_file, crawl_dir
import click
from os.path import isfile, isdir
ts = TextObjectStore()

@click.group()
def cli():
    pass

@cli.command()
@click.argument('hash')
@click.option('--attribs', default=False, help='Display Extended Attributes')
@click.option('--less', default=False, help='Use the pager')
def get(hash, attribs, less):
    """
    Retrevie a document object from the database by it's
    hashid.
    """
    tso = ts.retrieve_object(hash, attribs=False)
    if attribs:
        click.echo("Attributes are not supported yet")
        click.echo(tso)
    else:
        if less:
            click.echo_via_pager(tso)
        else:
            click.echo(tso)

@cli.command()
@click.argument('fts5term')
@click.option('--less', default=False, help='Use the pager')
def search(fts5term,less):
    search_id = ts.search_text(fts5term)
    echo_function = click.echo_via_pager if less else click.echo
    il = search_id['ids']
    echo_function("Results for: " + fts5term)
    for i in il:
        echo_function(i)
    echo_function("Total = " + str(search_id['count']))

@cli.command()
@click.argument('ent')
@click.option('--destroy', default=False, help='Destroy originals when injecting')
def etl(ent, destroy):
    
    if isfile(ent):
        inject_file(ent, destroy)
    elif isdir(ent):
        crawl_dir(ent, destroy)
    else:
        click.echo("Not a file i can ETL")

if __name__ == '__main__':
    cli()


        