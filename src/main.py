import click
import pickle
import os
from click.utils import echo


def load_data():
    try:
        with open(".data", "rb+") as f:
            data = pickle.load(f)
    except OSError:
        data = []
    return data


def write_data(data):
    pickle.dump(data, open(".data", "wb"))


@click.command()
@click.argument("src", type=click.Path())
@click.argument("name")
def add(src, name):
    """Add file SRC to database as NAME"""
    data = load_data()
    if src in {i[0] for i in data}:
        raise click.BadParameter(src, param_hint="SRC")
    if name in {i[1] for i in data}:
        raise click.BadParameter(name, param_hint="NAME")
    try:
        dest = f"{os.getcwd()}/{name}.config"
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
    """Delete NAME from database"""
    data = load_data()
    for k, v in enumerate(data):
        if v[1] == name:
            data.pop(k)
            write_data(data)
            try:
                dest = f"{os.getcwd()}/{v[1]}.config"
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
    raise click.UsageError("bullshit")


@click.group()
def dfm():
    pass


dfm.add_command(add)
dfm.add_command(show)
dfm.add_command(test)
dfm.add_command(delete)
if __name__ == "__main__":
    dfm()
