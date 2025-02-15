#!/usr/bin/env python3
"""Commandline interface to mastertext"""

from getpass import getpass
from os.path import isfile, isdir
import click
from werkzeug.security import generate_password_hash
from mastertext.objectstore import TextObjectStore
from mastertext.etl import inject_file, crawl_dir
from mastertext.models import database, NewUser
from mastertext.importer import fetch_and_parse

ts = TextObjectStore()


@click.group()
def cli():
    pass


@cli.command()
@click.argument("hash")
@click.option("--attribs", default=False, help="Display Extended Attributes")
@click.option("--less", default=False, help="Use the pager")
def get(hashid, attribs, less):
    """
    Retrevie a document object from the database by it's
    hashid.
    """
    tso = ts.retrieve_object(hashid, attribs=False)
    if attribs:
        click.echo("Attributes are not supported yet")
        click.echo(tso)
    else:
        if less:
            click.echo_via_pager(tso)
        else:
            click.echo(tso)


@cli.command()
@click.argument("fts5term")
@click.option("--less", default=False, help="Use the pager")
def search(fts5term, less):
    search_id = ts.search_text(fts5term)
    echo_function = click.echo_via_pager if less else click.echo
    il = search_id["ids"]
    echo_function("Results for: " + fts5term)
    for i in il:
        echo_function(i)
    echo_function("Total = " + str(search_id["count"]))


@cli.command()
@click.argument("ent")
@click.option("--destroy", default=False, help="Destroy originals when injecting")
@click.option("--mdate", default=False, help="Ugly Hack you know what it does")
def etl(ent, destroy, mdate):
    if isfile(ent):
        inject_file(ent, destroy=destroy, magic_date=mdate)
    elif isdir(ent):
        crawl_dir(ent, destroy, mdate)
    else:
        click.echo("Not a file i can ETL")


@cli.command()
@click.argument("username")
def migrate_add_users(username):
    if not click.confirm("Warning this will destroy and reintalize the users table"):
        return 1
    usr = None
    passwd = getpass(f"Enter password for {username}: ")
    confirm = getpass("Confirm: ")
    if passwd != confirm:
        click.echo("password mismatch")
        return 1
    hashed = generate_password_hash(passwd)
    with database:
        NewUser.drop_table(safe=True)
        NewUser.create_table(safe=True)
        usr = NewUser.create(
            username=username, email="test@example.com", password_hash=hashed
        )

    click.echo(usr)
    return 0


@cli.command
@click.argument("username")
def create_user(username):
    usr = None
    passwd = getpass(f"Enter password for {username}: ")
    confirm = getpass("Confirm: ")
    if passwd != confirm:
        click.echo("password mismatch")
        return 1
    hashed = generate_password_hash(passwd)
    email = click.prompt(f"Email address for {username}: ", default="test@example.com")
    with database:
        usr = NewUser.create(username=username, email=email, password_hash=hashed)

    click.echo(usr)
    return 0


@cli.command
@click.argument("url")
def import_url(url):
    text = fetch_and_parse(url)
    created_object = ts.create_object(text)
    print(created_object)


if __name__ == "__main__":
    cli()
