"""Some small wrappers for output messages."""
from click import echo, style


def info(message: str):
    echo(style(message, fg="cyan"))


def error(message: str, exit_after: bool = False):
    """Prints the given message as error message."""
    echo(style(message, fg="red"), err=True)

    if exit_after:
        exit(1)
