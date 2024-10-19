#!/usr/bin/env python
# Read the analog sensor value via MCP3002.

import spidev
import time
import subprocess

# open SPI device 0.0
spi = spidev.SpiDev()
spi.open(0, 0)

try:
    while True:
        resp = spi.xfer2([0x68, 0x00])
        value = (resp[0] * 256 + resp[1]) & 0x3ff
        print value
        time.sleep(1)
except KeyboardInterrupt:
    spi.close()
