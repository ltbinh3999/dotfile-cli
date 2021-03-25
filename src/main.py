import click
import pickle


@click.command()
@click.argument("src", type=click.Path())
@click.argument("name")
def add(src, name):
    """Add file SRC to center folder as NAME"""
    try:
        data = pickle.load(open(".data", "rb"))
        if src in {i[0] for i in data}:
            raise click.BadParameter(name, param_hint="SRC")
        if name in {i[1] for i in data}:
            raise click.BadParameter(name, param_hint="NAME")
        data.append((src, name))
    except OSError:
        data = [(src, name)]
    click.echo(f"Add {src} as {name}")
    pickle.dump(data, open(".data", "wb"))


@click.command()
def show():
    """Show all added file"""
    try:
        data = pickle.load(open(".data", "rb"))
        width = max([len(src) for src, _ in data])
        for src, name in data:
            click.echo(f"{src:<{width}} {name}")
    except:
        click.echo("Empty data.")


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
if __name__ == "__main__":
    dfm()
