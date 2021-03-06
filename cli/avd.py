import os
import shutil
from subprocess import check_call, check_output

ANDROID_SDK_ROOT = os.environ.get('ANDROID_SDK_ROOT')

patch = [
    'skin.dynamic=yes',
    'skin.name=nexus_5x',
    'skin.path=%s/skins/nexus_5x' % ANDROID_SDK_ROOT,
    'vm.heapSize=256',
    'hw.ramSize=1536',
    'hw.gpu.enabled=yes',
    'hw.gpu.mode=auto',
    'hw.cpu.arch=x86',
    'hw.cpu.ncore=2',
    'disk.dataPartition.size=800M',
    'showDeviceFrame=yes',
    'hw.initialOrientation=Portrait',
    'hw.camera.back=emulated',
    'hw.camera.front=emulated',
    'hw.keyboard=yes'
]


image_paths = {
    'kitkat': 'system-images;android-19;default;x86',
    'lollipop': 'system-images;android-22;default;x86',
    'marshmallow': 'system-images;android-23;default;x86',
    'nougat': 'system-images;android-24;default;x86',
}


def patch_config(device_name):
    with open(os.path.expanduser('~/.android/avd/%s.avd/config.ini' % device_name), "a") as f:
        for p in patch:
            f.write(p + '\n')


def create(name, codename):
    command = shutil.which('avdmanager') + ' -s create avd --force --name %s --device "Nexus 5" --package "%s" --sdcard 100M' % (
        name, image_paths.get(codename))
    out = check_output(command, shell=True, universal_newlines=True)
    patch_config(name)


def list_avd():
    command = shutil.which('avdmanager') + ' list avd'
    out = check_output(command.split(), universal_newlines=True).splitlines()
    return [n.replace('Name:', '').strip() for n in out if 'Name:' in n]


def delete_avd(name):
    print('Delete AVD')
    command = shutil.which('avdmanager') + ' delete avd --name %s' % name
    return 'deleted' in check_output(command.split(), universal_newlines=True)


def run(name, port, proxy=None, tcpdump=None):
    emulator = shutil.which('emulator')
    command = '%s -avd %s -writable-system -port %s ' % (emulator, name, port)
    if proxy:
        command += '-http-proxy %s ' % proxy
    if tcpdump:
        command += '-tcpdump %s ' % tcpdump
    check_call(command + '&', shell=True)
