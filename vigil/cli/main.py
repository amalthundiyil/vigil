import click
from checks import check
from cli_util import call_and_exit_flag, print_version


@click.group()
@call_and_exit_flag(
    "--version",
    callback=print_version,
    help="Show version information and exit.",
)
@click.pass_context
def cli(ctx):
    fmt = "%(asctime)s T%(thread)d %(levelname)s %(name)s [%(filename)s:%(lineno)d] - %(message)s"
    # fmt = "%(asctime)s %(levelname)s %(name)s - %(message)s"
    # logging.basicConfig(filename=os.path.join(ROOT_VIGIL_DIRECTORY, "logs", "cli.log"), filemode='a', format=fmt, force=True)


cli.add_command(check)

if __name__ == "__main__":
    cli()
