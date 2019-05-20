#!/usr/bin/env python3

import click

from dotfile_manager.configuration import InvalidConfigurationJsonObject
from dotfile_manager.configuration_wrapper import ConfigurationWrapper, InvalidConfigurationWrapperJsonObject
from dotfile_manager.dotfile import InvalidDotfileJsonObject
from dotfile_manager.messages import error
from dotfile_manager.script import InvalidScriptJsonObject

PARSING_EXCEPTIONS = (
    InvalidConfigurationJsonObject,
    InvalidConfigurationWrapperJsonObject,
    InvalidScriptJsonObject,
    InvalidDotfileJsonObject
)


class Setup(object):
    def __init__(self, configuration_file: str, parsing_exception: tuple, verbose: bool = False):
        """Loads the configuration from the given json file."""
        self.path = configuration_file
        self.verbose = verbose

        try:
            self.config = ConfigurationWrapper.from_json_file(configuration_file, verbose)
        except FileNotFoundError:
            error("Configuration file {} not found".format(configuration_file), True)
        except parsing_exception as exception:
            error(exception.message, True)


@click.group()
@click.option("-c", "--configuration-file", type=str, default="~/.config/manager/config.json",
              help="The json configuration file (default is `~/.config/manager/config.json`).")
@click.option("-v", "--verbose", is_flag=True, default=False, help="More verbose outputs.")
@click.pass_context
def cli(ctx, configuration_file: str, verbose: bool = False):
    ctx.obj = Setup(configuration_file, PARSING_EXCEPTIONS, verbose)


@cli.command()
@click.pass_context
def build(ctx):
    """Builds the configuration."""
    ctx.obj.config.build()


if __name__ == "__main__":
    cli()
