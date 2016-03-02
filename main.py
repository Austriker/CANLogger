#!/usr/bin/env python3
import RPi.GPIO as GPIO
import can
import time
import os
import queue
from threading import Thread
import logging
import os
import datetime

logger = logging.getLogger(__name__)
output_dir = os.path.dirname(os.path.realpath(__file__))
filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_can.log"

logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

handler = logging.FileHandler(os.path.join(output_dir, filename), "w", encoding=None)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


"""
Configs
"""
led = 22
bitrate = 250000
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, True)


# CAN receive thread
def can_rx_task():
    while True:
        message = bus.recv()
        # Put message into queue
        q.put(message)


def main():

    logger.info('Bring up CAN0....')

    # Bring up can0 interface at 500kbps
    os.system(
        "sudo /sbin/ip link set can0 up type can bitrate {0}".format(bitrate)
    )

    time.sleep(0.1)

    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    except OSError:
        logger.error('Cannot find PiCAN board.')
        GPIO.output(led, False)
        exit()

    q = queue.Queue()
    t = Thread(target=can_rx_task)    # Start receive thread
    t.start()

    # Main loop
    try:
        while True:
            if q.empty() != True:   # Check if there is a message in queue
                message = q.get()
                c = '{0:f} {1:x} {2:x} '.format(
                    message.timestamp,
                    message.arbitration_id,
                    message.dlc
                )

                s = ''
                for i in range(message.dlc):
                    s += '{0:x} '.format(message.data[i])

                outstr = c + s

                logger.info(outstr)

    except KeyboardInterrupt:
        # Catch keyboard interrupt
        GPIO.output(led, False)
        outfile.close()
        os.system("sudo /sbin/ip link set can0 down")
        logger.info('Keyboard interrtupt')

if __name__ == "__main__":
    main()
