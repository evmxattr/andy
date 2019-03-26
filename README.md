# Andy

A simple CLI to do fun stuff with stock Android emulators.

Wrapper around tools found in the Android SDK. It makes it super easy to spin up rooted Android devices
and bootstrap them with useful tools such as Busybox, Frida and Xposed.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

1. Android SDK
2. At least kitkat system image

This will install KitKat, LolliPop, Marshmallow and Nougat  
```
$ /path/to/sdk/tools/bin/sdkmanager "system-images;android-19;default;x86"
$ /path/to/sdk/tools/bin/sdkmanager "system-images;android-22;default;x86"
$ /path/to/sdk/tools/bin/sdkmanager "system-images;android-23;default;x86"
$ /path/to/sdk/tools/bin/sdkmanager "system-images;android-24;default;x86"
```

The following programs have to be available in your path
```
/path/to/sdk/platform-tools/adb
/path/to/sdk/emulator/emulator
/path/to/sdk/tools/bin/avdmanager
```
**ANDROID_SDK_ROOT** environment variable set to point to your SDK

```
export ANDROID_SDK_ROOT = /path/to/sdk
```

And finally, you must unzip necessary dependencies (Busybox, Frida, Xposed, su and more)

```
$ unzip deps.zip -d ~/.andy
```

### Installing

Create a new virtual environment, here I am using pew.

```
$ pew new andy --python=python3
```

```
$ pew workon andy
$ pip install -U .
```

Create a new device, start, bootstrap and root the device and proxy through privoxy.

This will also deploy frida server, Xposed, Busybox and some useful apps to the device.

```
$ andy create test_device --target kitkat --proxy 127.0.0.1:8118 --bootstrap
```

```
$ andy root
$ andy reboot
$ andy start somename --proxy 127.0.0.1:8118 --root
```

## Running the tests

TODO


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
