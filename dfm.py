import click
import pickle
import os
from click.utils import echo
import sys
from subprocess import Popen

DATABASE = os.path.expanduser("~/.dfm_data")


def load_data():
    try:
        with open(f"{DATABASE}/.data", "rb+") as f:
            data = pickle.load(f)
    except OSError:
        data = []
    return data


def write_data(data):
    pickle.dump(data, open(f"{DATABASE}/.data", "wb"))


@click.command()
def link():
    data = load_data()
    for src, dest in data:
        dest = f"{DATABASE}/{dest}.config"
        os.symlink(dest, src)


@click.command()
@click.argument("src", type=click.Path())
@click.argument("name")
def add(src, name):
    """Add SRC to data as NAME"""
    data = load_data()
    if src in {i[0] for i in data}:
        raise click.BadParameter(src, param_hint="SRC")
    if name in {i[1] for i in data}:
        raise click.BadParameter(name, param_hint="NAME")
    try:
        try:
            os.mkdir(DATABASE)
            Popen(["git", "init"], cwd=DATABASE)
        except FileExistsError:
            pass
        dest = f"{DATABASE}/{name}.config"
        os.replace(src, dest)
        os.symlink(dest, src)
        data.append((src, name))
        echo(f"Add {src} as {name}")
        write_data(data)
    except FileNotFoundError:
        raise click.BadParameter(src, param_hint="SRC")


@click.command()
@click.argument("name")
def delete(name):
    """Delete NAME from data"""
    data = load_data()
    for k, v in enumerate(data):
        if v[1] == name:
            data.pop(k)
            write_data(data)
            try:
                dest = f"{DATABASE}/{v[1]}.config"
                os.replace(dest, v[0])
            except FileNotFoundError:
                pass
            return
    raise click.BadParameter(name, param_hint="NAME")


@click.command()
def show():
    """Show all added file"""
    data = load_data()
    if data != []:
        width = max([len(src) for src, _ in data])
        for src, name in data:
            echo(f"{src:<{width}} {name}")
    else:
        echo("Empty data.")


@click.command()
def test():
    """DEBUG METHOD"""
    echo(sys.path[0])


@click.group()
def dfm():
    pass


dfm.add_command(add)
dfm.add_command(show)
dfm.add_command(test)
dfm.add_command(delete)
dfm.add_command(link)
if __name__ == "__main__":
    dfm()
