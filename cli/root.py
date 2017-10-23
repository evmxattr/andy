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


def install_xposed(device=None):
    print(crayons.white('Installing Xposed framework', bold=True))
    installer = {
        19: 'xposed.installer_v33_36570c.apk'
    }
    api = int(commands.get_prop('ro.build.version.sdk', device))
    xposed_dir = 'xposed-v88-sdk%s-x86' % api
    commands.install(os.path.join(os.path.expanduser('~/.rooter'),'framework/xposed/installer/%s' % installer.get(api, 'xposed.installer_3.1.2.apk')), device)
    commands.push(os.path.join(os.path.expanduser('~/.rooter'), 'framework/xposed/sdk/%s' % xposed_dir), '/data/local/tmp/', device)
    check_call(commands.adb(device) + 'shell chmod 0755 /data/local/tmp/%s/flash-script.sh' % xposed_dir, shell=True)
    check_call(commands.adb(device) + 'shell "cd /data/local/tmp/%s/ && ./flash-script.sh"' % xposed_dir, shell=True)


def install_busybox(device=None):
    print(crayons.white('Installing Busybox', bold=True))
    commands.push(os.path.join(os.path.expanduser('~/.rooter'), 'binaries/busybox/x86/busybox'), '/system/xbin/', device)
    check_call(commands.adb(device) + 'shell chmod 0755 /system/xbin/busybox', shell=True)
    check_call(commands.adb(device) + 'shell "cd /system/xbin/ && busybox --install /system/xbin/"', shell=True)


def install_apps(device=None):
    print(crayons.white('Installing apps', bold=True))
    for (dirpath, dirnames, filenames) in os.walk(os.path.expanduser('~/.rooter')):
        folder = os.path.basename(dirpath)
        if folder in ['apps', 'hooks']:
            for f in filenames:
                print(crayons.green('Installing %s' % crayons.white(f, bold=True)))
                commands.install(os.path.join(dirpath,f), device)



def bootstrap(device=None):
    commands.wait_for_device()
    install_busybox(device)
    install_apps(device)
    install_xposed(device)
    print(crayons.white('All done!', bold=True))
