import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
from threading import Timer
import sys

# Define Board GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO, spidev.SpiDev())

# initialization
radio.begin(0, 17)
radio.setRetries(15,15)

radio.setPayloadSize(3)
radio.setChannel(10)

radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(True)
radio.enableAckPayload()

radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])

radio.printDetails()

millis = lambda: int(round(time.time() * 1000))

total_tries = 100
listen_tries = 10

received_counter = 0
timeout_counter = 0

# start test
for i in range(total_tries):
        radio.stopListening()
        print("Test No. {}".format(i + 1))
        # sending/receiving
        test_buff = [1, 1, (i + 1)]

        # multiple tries
        for t in range(listen_tries):
                radio.write(test_buff)
                # listen
                radio.startListening()

                # timeout
                s = millis()
                timeout = False

                while (not radio.available() and (not timeout)):
                        if (millis() - s) > 10:
                                timeout = True
                if timeout:
                        print("No response received")
                        timeout_counter += 1
                        radio.stopListening()
                else:
                        # response received
                        received_buffer = []
                        radio.read(received_buffer, radio.getPayloadSize())
                        print("Received: {}".format(received_buffer))
                        radio.stopListening()

                        # check if response was equal to send
                        if received_buffer == test_buff:
                                # count and leave loop
                                received_counter += 1
                        break

print("----------Test Results:----------")
p = str((received_counter / total_tries) * 100) + "%"
p2 = str((timeout_counter / (total_tries * listen_tries)) * 100) + "%"
print("Result: {}/{} ({})".format(received_counter, total_tries, p))
print("Timeout Rate: {}/{} ({})".format(timeout_counter, (total_tries * listen_tries), p2))
