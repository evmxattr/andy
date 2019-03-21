# -*- coding: utf-8 -*-
import os
import sys
import shutil
import time
import tempfile
import shutil

import click
import click_completion
import crayons
import pexpect

from blindspin import spinner

from . import avd
from . import root as rooter
from .adb import commands

from .__version__ import __version__

proxies = {
    'privoxy': 'http://127.0.0.1:8118',
    'mitmproxy': 'http://127.0.0.1:8080'
}


splash = """

"""


def format_help(help):
    """Formats the help string."""
    help = help.replace('Options:', str(crayons.white('Options:', bold=True)))

    help = help.replace('Usage: andy', str(
        'Usage: {0}'.format(crayons.white('andy', bold=True))))

    help = help.replace('  create', str(crayons.green('  create', bold=True)))
    help = help.replace('  delete', str(crayons.red('  delete', bold=True)))
    help = help.replace('  start', str(crayons.green('  start', bold=True)))
    help = help.replace('  root', str(crayons.red('  root', bold=True)))
    help = help.replace('  bootstrap', str(crayons.blue('  bootstrap', bold=True)))
    help = help.replace('  install', str(crayons.yellow('  install', bold=True)))
    help = help.replace('  shell', str(crayons.yellow('  shell', bold=True)))
    help = help.replace('  emulators', str(crayons.green('  emulators', bold=True)))
    help = help.replace('  packages', str(crayons.green('  packages', bold=True)))
    help = help.replace('  devices', str(crayons.green('  devices', bold=True)))
    help = help.replace('  reboot', str(crayons.yellow('  reboot', bold=True)))
    help = help.replace('  pull', str(crayons.blue('  pull', bold=True)))
    help = help.replace('  forward', str(crayons.green('  forward', bold=True)))
    help = help.replace('  frida', str(crayons.red('  frida', bold=True)))

    return help


@click.argument('package', default=None)
@click.option('--device', '-d', default=None, help="Specify which device to run the command on.")
@click.command(help="Installs app on the device.")
def install(package=None, device=None):
    name = os.path.basename(package)
    click.echo('Installing package: {}'.format(
        click.style(str(name), fg='green')))
    res = commands.install(package, device)
    if 'Success' in res:
        click.echo(str(crayons.yellow('Package has been installed', bold=True)))
    else:
        click.echo(
            str(crayons.red('Unable to install package: {}'.format(res), bold=True)))


@click.command(help="Interactive shell.")
@click.option('--device', '-d', default=None, help="Specify which device to run the command on.")
def shell(device):
    click.echo(str(crayons.green("Attaching to a shell", bold=True)))
    commands.shell(device)


@click.command(help="Pull apk from device.", context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.argument('arg', default=None)
@click.argument('dest', default=None)
@click.option('--device', '-d', default=None, help="Specify which device to run the command on.")
@click.option('--package', is_flag=True, default=None,  help="Search for package and pull it")
def pull(arg, dest, device, package):
    click.echo(str(crayons.green("Pull from device", bold=True)))
    if package:
        for package, location in commands.get_packages(device).items():
            if arg in package:
                click.echo(crayons.green('Found a match: %s' % package))
                arg = location
                click.echo(arg)
    try:
        res = commands.pull(arg, dest, device)
    except Exception as e:
        click.echo(crayons.red('Unable to pull file/folder'))
    else:
        if 'pulled' in res:
            click.echo(crayons.green('Pulled %s from device' % arg))


@click.command(help="List attached devices.")
def devices():
    click.echo(str(crayons.green('Available devices', bold=True)))
    output = commands.devices()
    for line in output.splitlines()[1:]:
        click.echo(line.split('\t')[0])


@click.command(help="Root a running device.")
@click.option('--device', '-d', default=None, help="Specify which device to run the command on.")
def root(device):
    rooter.root_device(device)


@click.command(help="Bootstrap a running device.")
@click.option('--device', '-d', default=None, help="Specify which device to run the command on.")
def bootstrap(device):
    click.echo(str(crayons.white('Bootstrapping', bold=True)))
    rooter.bootstrap(device)


@click.command(help="Reboot device.")
@click.option('--device', '-d', default=None, help="Specify which device to run the command on.")
def reboot(device):
    commands.reboot(device)


@click.command(help="Start/stop frida server.")
@click.option('--device', '-d', default=None, help="Specify which device to run the command on.")
@click.option('--kill', '-k', is_flag=True, help="Kill running frida server.")
def frida(device, kill):
    if not kill:
        click.echo(str(crayons.white('Starting frida server', bold=True)))
        rooter.start_frida(device)
    else:
        rooter.stop_frida(device)


@click.command(help="Forward ports.")
@click.argument('local', default=None)
@click.argument('remote', default=None)
@click.option('--device', '-d', default=None, help="Specify which device to run the command on.")
def forward(local, remote, device):
    try:
        commands.forward(local, remote, device)
        click.echo(crayons.white(
            "Forwarded local port {0} to remote port {1}".format(local, remote), bold=True))
    except Exception as e:
        click.echo("Unable to forward ports")


@click.command(help="Create new AVD.")
@click.argument('name', default=None)
@click.argument('codename', default='kitkat')
@click.option('--proxy', '-p', default=proxies['privoxy'], help="http proxy.")
@click.option('--start', '-s', is_flag=True, help="Start device after creating it.")
@click.option('--bootstrap', '-b', is_flag=True, default=False, help="Bootstrap device when ready.")
def create(name, codename, proxy, start, bootstrap):
    click.echo(crayons.white(
        "Creating new device {0} [{1}]".format(name, codename), bold=True))
    avd.create(name, codename)
    if start:
        dev, port = commands.get_device_tuple()
        avd.run(name, port=port, proxy=proxy)
        print(crayons.white('Rooting', bold=True))
        rooter.root_device(dev)
        if bootstrap:
            print(crayons.white('Boostrapping', bold=True))
            rooter.bootstrap(dev)


@click.command(name='start', help="Start AVD.")
@click.argument('name', default=None)
@click.option('--proxy', '-p', default=proxies['privoxy'], help="http proxy.")
@click.option('--root', '-r', is_flag=True, help="Root device when ready.")
@click.option('--tcpdump', '-d', help="Capture network packets to file.")
def start(name, proxy, root, tcpdump):
    click.echo(crayons.white(
        "Starting device %s" % name, bold=True))
    dev, port = commands.get_device_tuple()
    avd.run(name, port=port, proxy=proxy, tcpdump=tcpdump)
    if root:
        print(crayons.white('Rooting', bold=True))
        rooter.root_device(dev)


@click.command(name='emulators', help="List available emulators")
def emulators():
    click.echo(crayons.white("Available AVD's", bold=True))
    for dev in avd.list():
        click.echo(str(crayons.green(dev)))

@click.command(name='delete', help="Delete emulator")
@click.argument('name')
def delete(name):
        click.echo(crayons.white("Deleting AVD %s" % name, bold=True))
        if avd.delete_avd(name):
            click.echo(crayons.green('Success!'))
        else:
            click.echo(crayons.red('Unable to delete AVD'))

@click.command(name='packages', help="List installed packages.")
@click.option('--device', '-d', default=None, help="Device  name.")
def packages(device):
    if packages:
        click.echo(str(crayons.green("Installed packages", bold=True)))
        lines = []
        for package, location in commands.get_packages(device).items():
            lines.append('{package}: {location}'.format(
                package=click.style(str(package), fg='green'), location=location))
        click.echo_via_pager('\n'.join(lines))


@click.group(invoke_without_command=True)
@click.option('--help', '-h', is_flag=True, default=None, help="Show this message then exit.")
@click.version_option(prog_name=crayons.yellow('rooter'), version=__version__)
@click.pass_context
def cli(ctx, help=False):

    if ctx.invoked_subcommand is None:
        click.echo(crayons.white(splash, bold=True))
        click.echo(format_help(ctx.get_help()))


cli.add_command(create)
cli.add_command(delete)
cli.add_command(start)
cli.add_command(root)
cli.add_command(bootstrap)
cli.add_command(install)
cli.add_command(packages)
cli.add_command(emulators)
cli.add_command(shell)
cli.add_command(devices)
cli.add_command(reboot)
cli.add_command(pull)
cli.add_command(forward)
cli.add_command(frida)


if __name__ == '__main__':
    cli()
