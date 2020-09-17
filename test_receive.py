import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
from threading import Timer
import sys
import os

# Define Board GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO, spidev.SpiDev())


radio.begin(0, 17)
radio.setRetries(15,15)

radio.setPayloadSize(3)
radio.setChannel(10)

radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(True)
radio.enableAckPayload()

radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])

radio.printDetails()

radio.stopListening()
radio.startListening()

while True:
        while not radio.available():
                time.sleep(1/100)
        recv_buffer = []
        radio.read(recv_buffer, radio.getPayloadSize())
        print("Received: {}".format(recv_buffer))
        radio.stopListening()
        radio.write(recv_buffer)
        radio.startListening()
