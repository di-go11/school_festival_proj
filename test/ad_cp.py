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
# read SPI data from MCP3002 chip
data_list = []
# 閾値越えフラグ
flag = False
# チャタリング
chattering = 10
count = 0
# 閾値
threshold = int(input("threshold:"))

try:
	while True:
		# read SPI data from MCP3002 chip
		resp = spi.xfer2([0x68,0x00])
		value = (resp[0] * 256 + resp[1]) & 0x3ff
		clock += 1

		# 閾値を超えたらデータを取得
		if value > threshold:
			# print(value)
			print(f"{'threshold':>10} : {threshold:<10}\t{'data':>10} : {value:<10}")
			data_list.append(value)
			# フラグ立てる
			flag = True
			# チャタリングカウントリセット
			count = 0

		# 閾値越えフラグが経っていて、閾値以下になったらデータを書き込む
		if flag & value <= threshold:
			# チャタリング charactering回連続で閾値以下になったら書き込む
			if count < chattering:
				count += 1

			# データ書き込みトリガ
			else:
				# フラグを下ろす
				flag = False
				count = 0
				# データ整形
				data_list_string = ', '.join(map(str,data_list))

				# データファイル書き込み
				with open('./data/data.txt','w', encoding='utf-8') as file:
					file.write(str(data_list_string))
					# データリストをクリア
					data_list.clear()
					file.close() # 明示的にファイルを閉じる
				# 転送用フラグファイル書き込み
				with open(flag_file, 'w') as f:
					f.write('Transfer flag created.\n')
					print("Transfer flag created")

		# 閾値自動修正
		if value < threshold:
			threshold -= 0.1
		elif value > threshold:
			threshold += 0.1
    
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
