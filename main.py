import click
import pickle


@click.command()
@click.argument("src", type=click.Path())
@click.argument("name")
def add(src, name):
    """Add file SRC to center folder as TO"""
    try:
        data = pickle.load(open(".data", "rb"))
        data.append((src, name))
    except:
        data = [(src, name)]
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
        pass


@click.group()
def main():
    pass


main.add_command(add)
main.add_command(show)

if __name__ == "__main__":
    main()
