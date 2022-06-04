"""To-Do entry point script."""
# todo/__main__.py

from todo import cli, __app_name__


def main():
    cli.todo_cli(prog_name=__app_name__)


if __name__ == "__main__":
    main()
