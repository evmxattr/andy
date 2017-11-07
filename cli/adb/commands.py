import shutil
from subprocess import check_call, check_output


def adb(device=None):
    adb = shutil.which('adb')
    if device:
        return adb + ' -s %s ' % device
    return adb + ' '


def shell(device):
    cmd = adb(device) + 'shell'
    check_call(cmd.split())


def install(package, device=None, *args, **kwargs):
    cmd = adb(device) + 'install %s' % package  # -l -r -t -s -d -p -g
    try:
        res = check_output(
            cmd.split(), universal_newlines=True).splitlines()[-1]
    except Exception as e:
        pass
    else:
        return res

def pull(source, dest, device):
    cmd = adb(device) + "pull {0} {1}".format(source, dest)
    res = check_output(cmd.split(), universal_newlines=True)
    return res


def push(source, dest, device):
    cmd = adb(device) + "push {0} {1}".format(source, dest)
    res = check_output(cmd.split(), universal_newlines=True)
    return res


def get_prop(prop, device=None):
    # ro.build.version.sdk
    out = check_output(adb(device) + 'shell getprop %s' % prop, shell=True, universal_newlines=True).strip()
    return out


def get_packages(device=None):
    packages = {}
    cmd = adb(device) + 'shell pm list packages -f'
    res = check_output(cmd.split(), universal_newlines=True)
    for package in res.splitlines():
        info = package.replace('package:', '').split('=')
        if '.apk' in info[0]:
            packages[info[1]] = info[0]
    return packages


def forward(local, remote, device):
    cmd = adb(device) + "forward tcp:{0} tcp:{1}".format(local, remote)
    check_call(cmd.split())


def reboot(device):
    cmd = adb(device) + "shell ps | grep zygote | awk '{print $2}'"
    pid = check_output(cmd, universal_newlines=True, shell=True)
    cmd = adb(device) + 'shell kill %s' % pid
    check_call(cmd.split())


def devices():
    cmd = adb(None) + "devices"
    output = check_output(cmd.split(), universal_newlines=True)
    return output


def wait_for_device(device=None):
    import time
    check_output(adb(device) + 'wait-for-device', shell=True)

    while True:
        out = check_output(
            adb(device) + 'shell getprop sys.boot_completed', shell=True)
        if '1' in str(out):
            break
        time.sleep(1)

    while True:
        try:
            if check_output(adb(device) + 'shell ps | grep android.process.acore', shell=True):
                break
        except:
            time.sleep(1)
    time.sleep(1)


def subprocess_with_output(command, newlines=True):
    with spinner():
        return check_output(command, universal_newlines=newlines)
