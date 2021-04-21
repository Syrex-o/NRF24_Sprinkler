#!/bin/sh

# Error out if anything fails.
#set -e
clear
echo "SmartSprinkler Installer"
echo ""
sleep 3
if [ "$(id -u)" != "0" ]; then
    echo -e "\033[1;31mRun Script as sudo./install.sh\033[0m"
  exit 1
fi
echo "Installation Step: 1"
echo "=========================="
apt update
apt -y full-upgrade
# set time
sudo timedatectl set-timezone Europe/Berlin
sudo timedatectl set-ntp true
# lang
sudo sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen 
sudo locale-gen 
sudo localectl set-locale LANG=de_DE.UTF-8 LANGUAGE=de_DE
echo "Installation Step: 2"
echo "Disable some settings"
echo "=========================="
if grep gpu_mem /boot/config.txt; then
  echo "Not changing GPU memory since it's already set"
else
  echo "" >> /boot/config.txt
  echo "# Decrease GPU memory because its headless not needed" >> /boot/config.txt
  echo "gpu_mem=16" >> /boot/config.txt
fi

if grep hdmi_blanking=1 /boot/config.txt; then
  echo "HDMI tweak already set"
else
  echo "" >> /boot/config.txt
  echo "# Turn off HDMI without connected Monitor to reduce inteference with HomematicIP Devices" >> /boot/config.txt
  echo "hdmi_blanking=1" >> /boot/config.txt
  echo "" >> /boot/config.txt
  echo "# disable HDMI audio" >> /boot/config.txt
  echo "hdmi_drive=1" >> /boot/config.txt
fi

echo "Installation Step: 3"
echo "=========================="
echo "Select Sender/Receiver"
echo -n -e '\033[36mSender (Y) or Receiver (R) [S/R]\033[0m'

read selectdecision
if [[ $selectdecision =~ (S|s) ]]
  then
    echo "Install Dependencies"
    apt -y install perl-base libdevice-serialport-perl libwww-perl libio-socket-ssl-perl libcgi-pm-perl libjson-perl sqlite3 libdbd-sqlite3-perl libtext-diff-perl libtimedate-perl libmail-imapclient-perl libgd-graph-perl libtext-csv-perl libxml-simple-perl liblist-moreutils-perl ttf-liberation libimage-librsvg-perl libgd-text-perl libsocket6-perl libio-socket-inet6-perl libmime-base64-perl libimage-info-perl libusb-1.0-0-dev libnet-server-perl vlan
    apt -y install apt-transport-https ntpdate socat libnet-telnet-perl libcrypt-rijndael-perl libdatetime-format-strptime-perl libsoap-lite-perl libjson-xs-perl libxml-simple-perl libdigest-md5-perl libdigest-md5-file-perl liblwp-protocol-https-perl liblwp-protocol-http-socketunix-perl libio-socket-multicast-perl libcrypt-cbc-perl libcrypt-ecb-perl libtypes-path-tiny-perl librpc-xml-perl libdatetime-perl libmodule-pluggable-perl libreadonly-perl libjson-maybexs-perl
    apt -y install libcryptx-perl avrdude
    echo "Install FHEM"
    echo "=========================="
    sleep 3
    sudo wget -qO - http://debian.fhem.de/archive.key | apt-key add -
    echo "deb http://debian.fhem.de/nightly/ /" >> /etc/apt/sources.list
    sudo apt update
    sudo apt install fhem
else
    echo "FHEM not needed on Receiver"
fi

echo "Installation Step: 4"
echo "Installing Sprinkler Parts"
echo "=========================="
sudo apt-get install python3-dev -y
sudo apt-get install git -y
sudo apt-get install python3-rpi.gpio -y

cd ../home/pi
wget https://github.com/Gadgetoid/py-spidev/archive/master.zip
unzip master.zip
rm master.zip
cd ./py-spidev-master
sudo python3 setup.py install
cd ../
sudo rm -r py-spidev-master
git clone https://github.com/Syrex-o/NRF24_Sprinkler

echo "Done"
echo "Enable SPI Interface manually!!!"
echo "Rebooting in 3 secs"
sleep 3
sudo shutdown -r now
exit
