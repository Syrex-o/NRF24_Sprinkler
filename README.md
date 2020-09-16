# NRF24_Sprinkler
NRF24 communication for RPi (FHEM Sprinkler)

## General Installation
1. enable SPI in raspi-config
2. sudo apt-get install python3-dev -y
3. sudo apt-get install git -y
4. sudo apt-get install python3-rpi.gpio -y
5. wget https://github.com/Gadgetoid/py-spidev/archive/master.zip
6. unzip master.zip
7. rm master.zip
8. cd ./py-spidev-master
9. sudo python3 setup.py install
10. sudo rm -r py-spidev-master
11. git clone https://github.com/Syrex-o/NRF24_Sprinkler

---

## Testing
!!! Configure Channel in send and receive script.
### Sender (Raspberry Pi 3)
- sudo python3 /home/pi/NRF24_Sprinkler/test_send.py
### Receiver (Raspberry Pi 2)
- sudo python3 /home/pi/NRF24_Sprinkler/test_receive.py

---

## Raspberry Pi No. 1 (Sender) --> Raspberry Pi 3
## Raspberry Pi No. 2 (Receiver) --> Raspberry Pi 2
