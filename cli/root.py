import os
import shutil
import crayons
from subprocess import check_call, check_output

from .adb import commands


def root_device(device=None):
    commands.wait_for_device()
    check_call(commands.adb(device) + 'root', universal_newlines=True, shell=True)
    check_call(commands.adb(device) + 'remount', universal_newlines=True, shell=True)
    commands.push(os.path.join(os.path.expanduser('~/.rooter'), 'binaries/su/x86/su.pie'), '/system/xbin/su', device)
    check_call(commands.adb(device) + 'shell chmod 0755 /system/xbin/su', universal_newlines=True, shell=True)
    check_call(commands.adb(device) + 'shell su --install', universal_newlines=True, shell=True)
    check_call(commands.adb(device) + 'shell su --daemon&', universal_newlines=True, shell=True)
    check_call(commands.adb(device) + 'shell setenforce 0', universal_newlines=True, shell=True)
    commands.reboot(device)


def bootstrap(device=None):
    commands.wait_for_device()
    print(crayons.green('Installing %s' % crayons.white('Busybox', bold=True)))
    commands.push(os.path.join(os.path.expanduser('~/.rooter'), 'binaries/busybox/x86/busybox'), '/system/xbin/', device)
    check_call(commands.adb(device) + 'shell chmod 0755 /system/xbin/busybox', shell=True)
    check_call(commands.adb(device) + 'shell "cd /system/xbin/ && busybox --install /system/xbin/"', shell=True)

    from os import walk
    for (dirpath, dirnames, filenames) in walk(os.path.join(os.path.expanduser('~/.rooter'), '')):
        if os.path.basename(dirpath) == 'apps':
            for f in filenames:
                print(crayons.green('Installing %s' % crayons.white(f, bold=True)))
                commands.install(os.path.join(dirpath,f), device)

    print(crayons.white('All done!', bold=True))
