# Setup Photon-based MetaSense

## Setup Photon

### Background - Device Modes

Listening Mode - blink blue slowly - waiting to connect to Wi-Fi

Wi-Fi Network Reset - blink blue rapidly - erase existing network - hold setup button for ten seconds

DFU Mode - blink yellow - for firmware program - hold both button and release reset button first, wait until it blinks yellow

For more information, check the [official guide](https://docs.particle.io/tutorials/device-os/led/photon/#standard-modes).

### Environment Setup

Use the CLI tool in terminal is the most convenient option. Following the [installation guide](https://docs.particle.io/tutorials/developer-tools/cli/).

### Setup a Photon

1. Verify your account is working! Check [setup account](https://login.particle.io/signup?app=setup&redirect=http://setup.particle.io).

   **Trouble Shooting #1**: if you got the output "Please login", try the following commands to re-log into your account.

   ```shell
   particle logout
   particle login
   ```

   **Trouble Shooting #2**: if you need the MAC address of the photon, you can use a serial tool such as PuTTy, enter "m" and you will get the MAC address. For detailed information, check [here](https://blog.jongallant.com/2015/08/particle-photon-mac-address/).

2. Enter Wi-Fi Network Reset Mode. Then use `particle setup` to guide you through setting up your account and your device

### Compile and Flash

**Important Note**: To compile and flash program to your Photon, you only need to setup your Particle account. Setting up Photon and register it on network is not required.

1. To compile a project in the current directory

   ```shell
   particle compile photon my_project_folder --saveTo firmware.bin
   ```

   For more options, check [official guide of CLI - particle compile](https://docs.particle.io/reference/developer-tools/cli/#particle-compile)

2. To flash to the device locally

   First enter DFU mode. Make sure dfu-util is installed. Then run the following command:

   ```shell
   particle flash --usb firmware.bin
   ```