# -*- coding: utf-8 -*-
import os
import sys
import shutil
import time
import tempfile

import click
import click_completion
import crayons
import pexpect
import requests

#from .__version__ import __version__
from blindspin import spinner
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def format_help(help):
    """Formats the help string."""
    help = help.replace('Options:', str(crayons.white('Options:', bold=True)))

    help = help.replace('Usage: froot', str(
        'Usage: {0}'.format(crayons.white('froot', bold=True))))

    help = help.replace('  install', str(
        crayons.yellow('  install', bold=True)))
    help = help.replace('  root', str(crayons.red('  root', bold=True)))
    help = help.replace('  shell', str(crayons.blue('  shell', bold=True)))

    additional_help = """
Usage Examples:
   Create a new project using Python 3:
   $ {0}

   Create a new project using Python 3.6, specifically:
   $ {1}

   Install all dependencies for a project (including dev):
   $ {2}

   Create a lockfile:
   $ {3}

   Show a graph of your installed dependencies:
   $ {4}

Commands:""".format(
        crayons.red('froot --three'),
        crayons.red('froot --python 3.6'),
        crayons.red('froot install --dev'),
        crayons.red('froot lock'),
        crayons.red('froot graph')
    )

    help = help.replace('Commands:', additional_help)

    return help


@click.command(help="Installs provided apps.", context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.argument('package_name', default=False)
@click.option('--verbose', is_flag=True, default=False, help="Verbose mode.")
def install(
        package_name=False, verbose=False):

    print("Install")

@click.command(help="Spawn a shell on the device.", context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.option('--verbose', is_flag=True, default=False, help="Verbose mode.")
def shell(verbose=False):

    print("Shell")

@click.command(help="Root a running device.", context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.option('--verbose', is_flag=True, default=False, help="Verbose mode.")
def root(
        package_name=False, verbose=False):

    print("Root")


@click.group(invoke_without_command=True)
@click.option('--update', is_flag=True, default=False, help="Update to latest.")
@click.option('--python', default=False, nargs=1, help="Specify which version of Python virtualenv should use.")
@click.option('--help', '-h', is_flag=True, default=None, help="Show this message then exit.")
@click.version_option(prog_name=crayons.yellow('froot'), version="0.0.1")
@click.pass_context
def cli(
        ctx, help=False, update=False, python=False):

    if ctx.invoked_subcommand is None:
        click.echo(format_help(ctx.get_help()))


# Install click commands.
cli.add_command(install)
cli.add_command(root)
cli.add_command(shell)

if __name__ == '__main__':
    cli()
