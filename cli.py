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
import subprocess

#from .__version__ import __version__
from blindspin import spinner


splash = """
  ______                                 __     __
 /      \                               /  |   /  |
/$$$$$$  |______    ______    ______   _$$ |_  $$ |
$$ |_ $$//      \  /      \  /      \ / $$   | $$ |
$$   |  /$$$$$$  |/$$$$$$  |/$$$$$$  |$$$$$$/  $$ |
$$$$/   $$ |  $$/ $$ |  $$ |$$ |  $$ |  $$ | __$$/
$$ |    $$ |      $$ \__$$ |$$ \__$$ |  $$ |/  |__
$$ |    $$ |      $$    $$/ $$    $$/   $$  $$//  |
$$/     $$/        $$$$$$/   $$$$$$/     $$$$/ $$/
                                                   
"""

def format_help(help):
    """Formats the help string."""
    help = help.replace('Options:', str(crayons.white('Options:', bold=True)))

    help = help.replace('Usage: froot', str(
        'Usage: {0}'.format(crayons.white('froot', bold=True))))

    help = help.replace('  install', str(crayons.yellow('  install', bold=True)))
    help = help.replace('  root', str(crayons.red('  root', bold=True)))
    help = help.replace('  shell', str(crayons.blue('  shell', bold=True)))

    additional_help = """
Usage Examples:
   A:
   $ {0}


Commands:""".format(
        crayons.red('froot --A'),
    )

    help = help.replace('Commands:', additional_help)

    return help


@click.command(help="Installs app on the device.", context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.argument('package', default=None)
@click.option('--device', default=None, help="Specify which device to get shell in")
@click.option('--verbose', is_flag=True, default=False, help="Verbose mode.")
def install(package=None, device=None, verbose=False):
    name = os.path.basename(package)
    print(str(crayons.green('Installing package: {}'.format(name))))
    dev = ""
    if device:
        dev = "-s {device}".format(device=device)

    command = "adb {extra} install {package}".format(extra=dev, package=package).split()
    try:
        res = subprocess_with_output(command).splitlines()[-1]
    except:
        pass
    else:
        if 'Success' in res:
            print(str(crayons.yellow('Package was installed', bold=True)))
        else:
            print(str(crayons.red('Unable to install package: {}'.format(res), bold=True)))


@click.command(help="Spawn a shell on the device.", context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.option('--device', help="Specify which device to get shell in")
def shell(device):
    print(str(crayons.green("Attaching to a shell", bold=True)))
    if device:
        subprocess.call(["adb", "-s", device, "shell"])
    else:
        subprocess.call(["adb", "shell"])


def subprocess_with_output(command, newlines=True):
    with spinner():
        return subprocess.check_output(command, universal_newlines=newlines)


@click.command(help="List attached devices.", context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.option('--verbose', is_flag=True, default=False, help="Verbose mode.")
def devices(verbose=False):
    print(str(crayons.green('Available devices', bold=True)))
    output = subprocess_with_output(["adb", "devices"])
    for line in output.splitlines()[1:]:
        print(line.split('\t')[0])


@click.command(help="Root a running device.", context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.option('--verbose', is_flag=True, default=False, help="Verbose mode.")
def root(
        package_name=False, verbose=False):

    print(str(crayons.red('Not implemented yet')))


@click.group(invoke_without_command=True)
@click.option('--help', '-h', is_flag=True, default=None, help="Show this message then exit.")
@click.version_option(prog_name=crayons.yellow('froot'), version="0.0.1")
@click.pass_context
def cli(
        ctx, help=False):

    if ctx.invoked_subcommand is None:
        click.echo(crayons.white(splash, bold=True))
        click.echo(format_help(ctx.get_help()))


# Install click commands.
cli.add_command(install)
cli.add_command(root)
cli.add_command(shell)
cli.add_command(devices)

if __name__ == '__main__':
    cli()
