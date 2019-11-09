# Setup a Raspberry Pi node in the mesh network

[Setup Raspberry Pi as Mesh Node](#Setup-Raspberry-Pi-as-Mesh-Node)

[Setup Time Synchronization](#Setup-Time-Synchronization)

[Use Mosquitto with fixed interface](#Use-Mosquitto-with-fixed-interface)

## Setup Raspberry Pi as Mesh Node

### Setup Procedures

1. Install `batman-dev` and `batctl`, configure network settings on RPi with the following commands:

   ```shell
   sudo bash ./install.sh # require internet connection
   sudo bash ./batsetup-rpi.sh <ip>
   ```

   Replace <ip> with the desired IP you want to set for this device, e.g. 172.27.0.1/16.

   **Trouble-shooting**

   * If you get error like "device or resource busy", it is likely that you didn't disable wpa_supplicant. First try disconnecting from Wi-Fi, erasing Wi-Fi credentials in `/etc/wpa_supplicant/wpa_supplicant.conf`, finally rebooting the system.

   If the setup is successful,  you should be able to get similar output as the following:

   ```shell
   pi@pi:~ $ ifconfig
   bat0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
           inet 172.10.0.1  netmask 255.255.0.0  broadcast 172.10.255.255
           inet6 fe80::983e:f7ff:feac:9195  prefixlen 64  scopeid 0x20<link>
           ether 9a:3e:f7:ac:91:95  txqueuelen 1000  (Ethernet)
           RX packets 5  bytes 210 (210.0 B)
           RX errors 0  dropped 0  overruns 0  frame 0
           TX packets 8  bytes 1222 (1.1 KiB)
           TX errors 0  dropped 15 overruns 0  carrier 0  collisions 0
   
   lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
           inet 127.0.0.1  netmask 255.0.0.0
           inet6 ::1  prefixlen 128  scopeid 0x10<host>
           loop  txqueuelen 1000  (Local Loopback)
           RX packets 9  bytes 524 (524.0 B)
           RX errors 0  dropped 0  overruns 0  frame 0
           TX packets 9  bytes 524 (524.0 B)
           TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
   
   wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
           inet6 fe80::ba27:ebff:fe87:2978  prefixlen 64  scopeid 0x20<link>
           ether b8:27:eb:87:29:78  txqueuelen 1000  (Ethernet)
           RX packets 0  bytes 0 (0.0 B)
           RX errors 0  dropped 0  overruns 0  frame 0
           TX packets 70  bytes 6952 (6.7 KiB)
           TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
   
   pi@pi:~ $ iwconfig
   lo        no wireless extensions.
   
   bat0      no wireless extensions.
   
   wlan0     IEEE 802.11  ESSID:"my-mesh"  
             Mode:Ad-Hoc  Frequency:2.432 GHz  Cell: 76:B9:A4:66:DC:CA   
             Tx-Power=31 dBm   
             Retry short limit:7   RTS thr:off   Fragment thr:off
             Power Management:on
             
   eth0      no wireless extensions.
   ```

   The important part of above output is `ESSID` and `Cell` value. They should be same on all devices. If you see a similar outcome, then the network has been setup.  

2. Test mesh network.

   You can try reaching other mesh nodes in the network, if any, with the following commands:

   ```shell
   sudo batctl o # get originators
   sudo batctl n # get neighbors
   ```

3. To automatically complete network setup each time when the system boots, Make `batsetup-rpi.sh` executable with `chmod u+x batsetup-rpi.sh` and finally add its absolute path into `/etc/rc.local` before `return 0` line.

### Reset Procedure

1. Remember to delete the line you added in `/etc/rc.local`, if any.
2. Run `reset.sh` to undo all the settings.
3. Reboot system.

### Resources

[pi-adhoc-mqtt-cluster](https://github.com/suiluj/pi-adhoc-mqtt-cluster/wiki/Batman-Adv-and-Batctl): Setup RPi 3, 2, zero as normal mesh node and gateway.

[USB Dongle as AP and Hotspot Sharing Configuration](https://github.com/suiluj/pi-adhoc-mqtt-cluster/wiki/USB-Dongle-Wifi-Configuration).

[Setting up an Ad-Hoc Mesh Network with Raspberry Pi 3B+ using BATMAN-Adv](https://medium.com/swlh/setting-up-an-ad-hoc-mesh-network-with-raspberry-pi-3b-using-batman-adv-1c08ee565165).

[How To Configure batman-adv on the Raspberry Pi 3](https://www.reddit.com/r/darknetplan/comments/68s6jp/how_to_configure_batmanadv_on_the_raspberry_pi_3/).

## Setup Time Synchronization

According to [a blog](http://raspberrypi.tomasgreno.cz/ntp-client-and-server.html), if you want to sync Pi's time with NTP server:

```shell
sudo apt-get install ntp
sudo systemctl stop systemd-timesyncd
sudo systemctl disable systemd-timesyncd
sudo /etc/init.d/ntp stop
sudo /etc/init.d/ntp start
```

## Use Mosquitto with fixed interface

To use `bind_interface` in `mosquitto.conf`, you need to download the newest version of mosquitto from their [official download page](https://mosquitto.org/download/). Untar the file and `cd` into it, run the following commands:

```shell
sudo apt-get install libssl-dev # required in the make process
sudo make
sudo make install
```

You can use the configuration file in this directory to start the mosquitto bound to eth0:

```shell
mosquitto -c ./mosquitto.conf -p 61613 -v
```

