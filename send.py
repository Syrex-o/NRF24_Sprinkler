import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import sys
import os

# Define Board GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO, spidev.SpiDev())

# initialization
radio.begin(0, 17)
radio.setRetries(15,15)

radio.setChannel(10)

radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setPayloadSize(7)
radio.setAutoAck(True)
radio.enableAckPayload()
radio.enableDynamicPayloads()

radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])

millis = lambda: int(round(time.time() * 1000))

tries = 20

# message to send --> GPIO PIN + 1/0 (on/off) + duration ins secs
message = list(sys.argv[1]+sys.argv[2]+sys.argv[3])

# evaluate if callback received
callback = False

# start transmission tries
for i in range(tries):
    radio.stopListening()
    # send
    radio.write(message)
    # start listen
    radio.startListening()

    # timeout
    s = millis()
    timeout = False

    while (not radio.available() and (not timeout)):
        if (millis() - s) > 10:
            timeout = True
    if timeout:
        callback = False
    else:
        recv = []
        radio.read(recv, radio.getDynamicPayloadSize())

        # translate message
        arr = []
        for n in recv:
            # Decode into standard unicode set
            if (n >= 32 and n <= 126):
                arr.append(chr(n))
        # check if response was equal to send
        if arr == message:
            # callback received successful
            callback = True
            print(arr)
            break

# get relevant command --> translate command
command = "true" if sys.argv[2] == "1" else "false"
if callback:
    # write callback
    os.system('perl /opt/fhem/fhem.pl 7072 "set '+sys.argv[4]+' callbackState '+command+'"')
else:
    # set callback to false
    os.system('perl /opt/fhem/fhem.pl 7072 "set '+sys.argv[4]+' callbackState false"')
    
    # last error write
    os.system('perl /opt/fhem/fhem.pl 7072 "set '+sys.argv[4]+' lastError noReply"')
    
    # reset sprinkler to false --> no callback + want to set on --> remove sprinkler block
    if command == "true":
        os.system('perl /opt/fhem/fhem.pl 7072 "set '+sys.argv[4]+' state false"')

sys.exit()
