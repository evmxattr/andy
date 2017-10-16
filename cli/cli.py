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

    help = help.replace('  install', str(
        crayons.yellow('  install', bold=True)))
    help = help.replace('  root', str(crayons.red('  root', bold=True)))
    help = help.replace('  shell', str(crayons.blue('  shell', bold=True)))
    help = help.replace('  pull', str(crayons.green('  pull', bold=True)))
    help = help.replace('  reboot', str(crayons.yellow('  reboot', bold=True)))

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
@click.option('--device', '-d', default=None, help="Specify which device to run the command on.")
@click.option('--verbose', is_flag=True, default=False, help="Verbose mode.")
def install(package=None, device=None, verbose=False):
    name = os.path.basename(package)
    print(str(crayons.green('Installing package: {}'.format(name))))
    cmd = _adb(device) + 'install %s' % package # -l -r -t -s -d -p -g
    try:
        res = subprocess_with_output(cmd.split()).splitlines()[-1]
    except Exception as e:
        print(e)
        pass
    else:
        if 'Success' in res:
            print(str(crayons.yellow('Package has been installed', bold=True)))
        else:
            print(
                str(crayons.red('Unable to install package: {}'.format(res), bold=True)))


@click.command(help="Interactive shell.", context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.option('--device', '-d', default=None, help="Specify which device to run the command on.")
def shell(device):
    print(str(crayons.green("Attaching to a shell", bold=True)))
    cmd = _adb(device) + 'shell'
    subprocess.call(cmd.split())


#####
def get_packages(device=None):
    packages = {}
    cmd = _adb(device) + 'shell pm list packages -f'
    res = subprocess_with_output(cmd.split())
    for package in res.splitlines():
        info = package.replace('package:', '').split('=')
        if '.apk' in info[0]:
            packages[info[1]] = info[0]
    return packages
#####


@click.command(help="List installed packages.", context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.option('--device', '-d', default=None, help="Specify which device to run the command on.")
def packages(device):
    print(str(crayons.green("Installed packages", bold=True)))
    lines = []
    for package, location in get_packages(device).items():
        lines.append('{package}: {location}'.format(package=click.style(str(package), fg='green'), location=location))
    click.echo_via_pager('\n'.join(lines))



@click.command(help="Pull apk from device.", context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.argument('arg', default=None)
@click.argument('dest', default=None)
@click.option('--device', '-d', default=None, help="Specify which device to run the command on.")
@click.option('--package', is_flag=True, default=None,  help="Search for package and pull it")
def pull(arg, dest, device, package):
    print(str(crayons.green("Pull from device", bold=True)))
    if package:
        for package, Location in get_packages(device).items():
            if arg in package:
                print(crayons.green('Found a match: %s' % package))
                arg = Location
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
@click.option('--device', '-d', default=None, help="Specify which device to run the command on.")
@click.option('--verbose', is_flag=True, default=False, help="Verbose mode.")
def root(device, verbose=False):
    print(str(crayons.red('Not implemented yet')))


@click.command(help="Reboot device.", context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.option('--device', '-d', default=None, help="Specify which device to run the command on.")
def reboot(device):
    cmd = _adb(device) + "shell ps | grep zygote | awk '{print $2}'"
    zygote = subprocess.check_output(cmd.split(), universal_newlines=True)
    cmd = _adb(device) + 'shell kill %s' % zygote
    subprocess.check_call(cmd.split())


@click.command(help="Forward ports.", context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.argument('local', default=None)
@click.argument('remote', default=None)
@click.option('--device', '-d', default=None, help="Specify which device to run the command on.")
def forward(local, remote, device):
    cmd = _adb(device) + "forward tcp:{0} tcp:{1}".format(local, remote)
    try:
        subprocess.check_call(cmd.split(), universal_newlines=True)
        click.echo(crayons.white(
            "Forwarded local port {0} to remote port {1}".format(local, remote), bold=True))
    except:
        click.echo("Unable to forward ports")


def _adb(device=None):
    import shutil
    adb = shutil.which('adb')
    if device:
        return adb + ' -s %s ' % device
    return adb + ' '


@click.group(invoke_without_command=True)
@click.option('--help', '-h', is_flag=True, default=None, help="Show this message then exit.")
@click.version_option(prog_name=crayons.yellow('froot'), version="0.0.1")
@click.pass_context
def cli(ctx, help=False):

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
cli.add_command(forward)


if __name__ == '__main__':
    cli()
