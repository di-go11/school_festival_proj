#!/usr/bin/env python
# Read the analog sensor value via MCP3002.

import spidev
import time
import subprocess

# open SPI device 0.0
spi = spidev.SpiDev()

spi.open(0,0)
flag_file = './flag/transfer_success.flag'
spi.max_speed_hz = 1000000
spi.mode = 0
clock = 0
data_list = []
flag = 0
count = 0
threshold = int(input("threshold:"))

try:
    while True:
        resp = spi.xfer2([0x68,0x00])
        value = (resp[0] * 256 + resp[1]) & 0x3ff
        clock += 1
        if value > threshold:
            print(value)
            data_list.append(value)
            if flag == 0:
            		flag = 1
            else:
                pass
        
        elif value <= threshold:
            if flag == 1:
                if count <= 20:
                    count += 1
                elif count > 20:
                    flag = 0
                    data_list_string = ', '.join(map(str,data_list))
                    with open('./data/data.txt','w', encoding='utf-8') as file:
                        file.write(str(data_list_string))
                        file.close()
                        # txt tennsouyoukaku
                    with open(flag_file, 'w') as f:
                        f.write('Transfer flag created.\n')
                        print("Transfer flag created")
                    count = 0
                else:
                    pass
            else :
                pass
        else:
            pass
		#time.sleep(0.0005)
except KeyboardInterrupt:
	spi.close()

"""
try:
	while True:
		# print(f'value:{value.adc_ch0:.2f},Volt:{value.adc_ch0 * Vref:.2f}')
		sleep(1)
except KeyboardInterrupt:
    spi.close()
"""
