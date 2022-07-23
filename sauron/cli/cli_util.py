import click
import string

from sauron._version import __version__


def print_version(ctx):
    click.echo(f"Sauron version info - v{__version__}")


def call_and_exit_flag(*args, callback, is_eager=True, **kwargs):
    """
    Add an is_flag option that, when set, eagerly calls the given callback with only the context as a parameter.
    The process exits once the callback is finished.
    Usage:
    @call_and_exit_flag("--version", callback=print_version, help="Print the version number")
    """

    def actual_callback(ctx, param, value):
        if value and not ctx.resilient_parsing:
            callback(ctx)
            ctx.exit()

    return click.option(
        *args,
        is_flag=True,
        callback=actual_callback,
        expose_value=False,
        is_eager=is_eager,
        **kwargs,
    )

