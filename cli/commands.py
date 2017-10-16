import shutil
from subprocess import check_call, check_output


def _adb(device=None):
    adb = shutil.which('adb')
    if device:
        return adb + ' -s %s ' % device
    return adb + ' '


def shell(device):
    cmd = _adb(device) + 'shell'
    check_call(cmd.split())


def install(package, device=None, *args, **kwargs):
    cmd = _adb(device) + 'install %s' % package  # -l -r -t -s -d -p -g
    try:
        res = check_output(
            cmd.split(), universal_newlines=True).splitlines()[-1]
    except Exception as e:
        raise
    else:
        return res


def pull(source, dest, device):
    cmd = _adb(device) + "pull {0} {1}".format(source, dest)
    res = check_output(cmd.split(), universal_newlines=True)
    return res


def get_packages(device=None):
    packages = {}
    cmd = _adb(device) + 'shell pm list packages -f'
    res = check_output(cmd.split(), universal_newlines=True)
    for package in res.splitlines():
        info = package.replace('package:', '').split('=')
        if '.apk' in info[0]:
            packages[info[1]] = info[0]
    return packages


def forward(local, remote, device):
    cmd = _adb(device) + "forward tcp:{0} tcp:{1}".format(local, remote)
    check_call(cmd.split())


def reboot(device):
    cmd = _adb(device) + "shell ps | grep zygote | awk '{print $2}'"
    zygote = check_output(cmd.split(), universal_newlines=True)
    cmd = _adb(device) + 'shell kill %s' % zygote
    check_call(cmd.split())


def devices():
    cmd = _adb(None) + "devices"
    output = check_output(cmd.split(), universal_newlines=True)
    return output


def subprocess_with_output(command, newlines=True):
    with spinner():
        return subprocess.check_output(command, universal_newlines=newlines)
