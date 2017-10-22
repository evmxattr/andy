import os
import shutil
from subprocess import check_call, check_output

from .adb import commands


def root_device(device=None):
    commands.wait_for_device()
    check_call(commands.adb(device) + 'root', universal_newlines=True, shell=True)
    check_call(commands.adb(device) + 'remount', universal_newlines=True, shell=True)
    commands.push(os.path.join(os.path.expanduser('~/.stuff'), 'binaries/su.pie'), '/system/xbin/su', device)
    check_call(commands.adb(device) + 'shell chmod 0755 /system/xbin/su', universal_newlines=True, shell=True)
    check_call(commands.adb(device) + 'shell su --install', universal_newlines=True, shell=True)
    check_call(commands.adb(device) + 'shell su --daemon&', universal_newlines=True, shell=True)
    check_call(commands.adb(device) + 'shell setenforce 0', universal_newlines=True, shell=True)
    commands.reboot(device)


def bootstrap(device=None):
    pass
