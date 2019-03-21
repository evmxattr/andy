# Andy

A simple CLI to do fun stuff with stock Android emulators


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

1. Android SDK
2. At least kitkat system image

The following programs have to be available in your path
```
/path/to/sdk/platform-tools/adb
/path/to/sdk/emulator/emulator
/path/to/sdk/tools/bin/avdmanager
```
**ANDROID_SDK_ROOT** environment variable set to point to your SDK

Unzip dependencies.
This contains, busybox, frida, Xposed framework and other useful apps.
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
$ pip install -U -e .
```

Create a new device, start, bootstrap and root the device and proxy through privoxy.

This will also deploy frida server, Xposed, Busybox and some useful apps to the device.
```
andy create --proxy 127.0.0.1:8118 --bootstrap --start kitkat
```


## Running the tests

TODO


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
