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
    help = help.replace('  pull', str(crayons.green('  pull', bold=True)))

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
@click.option('--device', default=None, help="Specify which device to install application to")
@click.option('--verbose', is_flag=True, default=False, help="Verbose mode.")
def install(package=None, device=None, verbose=False):
    name = os.path.basename(package)
    print(str(crayons.green('Installing package: {}'.format(name))))
    dev = ""
    if device:
        dev = "-s %s" % device
    command = "adb {extra} install {package}".format(
        extra=dev, package=package).split()
    try:
        res = subprocess_with_output(command).splitlines()[-1]
    except Exception as e:
        print(e)
        pass
    else:
        if 'Success' in res:
            print(str(crayons.yellow('Package has been installed', bold=True)))
        else:
            print(
                str(crayons.red('Unable to install package: {}'.format(res), bold=True)))


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


#####
def get_packages(device=None):
    packages = []
    res = subprocess_with_output(
        ['adb', 'shell', 'pm', 'list', 'packages', '-f'])
    for package in res.splitlines():
        info = package.replace('package:', '').split('=')
        if '.apk' in info[0]:
            packages.append(info)
    return packages

#####


@click.command(help="List installed packages.", context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.option('--device', help="Specify which device to attach to")
def packages(device):
    print(str(crayons.green("Installed packages", bold=True)))
    for package in get_packages():
        print('Package: {} :: Location: {}'.format(package[1], package[0]))


@click.command(help="Pull apk from device.", context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.argument('arg', default=None)
@click.argument('dest', default=None)
@click.option('--device', help="Specify which device to attach to")
@click.option('--package', is_flag=True, default=None,  help="Search for package and pull it")
def pull(arg, dest, device, package):
    print(str(crayons.green("Pull from device", bold=True)))
    if package:
        packages = get_packages(device)
        for package in packages:
            if arg in package[1]:
                print(crayons.green('Found a match: %s' % package[1]))
                arg = package[0]
                print(arg)
    try:
        # TODO: Specific device
        res = subprocess_with_output(['adb', 'pull', arg, dest])
    except Exception as e:
        print(crayons.red('Unable to pull file/folder'))
    else:
        if 'pulled' in res:
            print(crayons.green('Pulled %s from device' % arg))


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


@click.command(help="Reboot device.", context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.option('--verbose', is_flag=True, default=False, help="Verbose mode.")
def reboot(
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
cli.add_command(reboot)
cli.add_command(packages)
cli.add_command(pull)


if __name__ == '__main__':
    cli()
