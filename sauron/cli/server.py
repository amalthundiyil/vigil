
import logging
from multiprocessing import Process

import click

from sauron.backend import app

LOG = logging.getLogger("sauron.cli.server")


@click.group(help="Command to manage the server")
def server():
    pass

@server.command(context_settings=dict(ignore_unknown_options=True))
@click.pass_context
def start(ctx):
    server = Process(target=app.run)
    click.secho(f'️🖥️ Starting Server', fg="blue", bold=True)
    ctx.obj["server"] = server
    server.start()

@server.command(context_settings=dict(ignore_unknown_options=True))
@click.pass_context
def stop(ctx):
    try:
        server = ctx.obj["server"]
    except KeyError:
        click.secho(f'️🤔 No server instance found', fg="red", bold=True)
    server.terminate()
    server.join()
    click.secho(f'❗ Failed to shutdown the server', fg="red", bold=True)