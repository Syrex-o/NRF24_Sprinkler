import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
from threading import Timer

# Define Board GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# needed GPIO PINS
PINS = [2,3,4,5,6,7]

# set all pins off
def allPinsOff():
    for i in PINS:
        GPIO.setup(i, GPIO.OUT, initial=GPIO.HIGH)
# initial off
allPinsOff()

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
radio.setRetries(15,15)

radio.setChannel(10)

radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setPayloadSize(7)
radio.setAutoAck(True)
radio.enableAckPayload()
radio.enableDynamicPayloads()

radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])

radio.stopListening()
radio.startListening()

millis = lambda: int(round(time.time() * 1000))

last_call = millis()

# timer status
isTimerActive = False

def pinOff(pin):
    global isTimerActive
    GPIO.output(pin, GPIO.HIGH)
    isTimerActive = False

while True:
        while not radio.available():
                time.sleep(1/100)
        recv = []
        radio.read(recv, radio.getDynamicPayloadSize())
        radio.stopListening()
        radio.write(recv)
        radio.startListening()

        # translate message
        arr = []
        for n in recv:
            # Decode into standard unicode set
                if (n >= 32 and n <= 126):
                    arr.append(chr(n))

        # validation
        if len(arr) > 0 and int(arr[0]) in PINS:
            # validation complete --> check last call to prevent bubbles
            if (millis() - last_call) > 100:
                # on
                if arr[1] == '1':
                    # reset all active pins
                    for pin in PINS:
                        if not GPIO.input(pin):
                            GPIO.output(pin, GPIO.HIGH)
                    # activate
                    GPIO.output(int(arr[0]), GPIO.LOW)
                    secs = int("".join(arr)[2:])

                    # timer
                    if isTimerActive:
                        t.cancel()
                        isTimerActive = False
                    t = Timer(secs, pinOff, [int(arr[0])])
                    t.start()
                    isTimerActive = True
                else:
                    # off
                    GPIO.output(int(arr[0]), GPIO.HIGH)
            # update last reply
            last_call = millis()
