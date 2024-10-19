#!/usr/bin/env python
# Read the analog sensor value via MCP3002.

# import spidev
import time
import subprocess
import matplotlib.pyplot as plt

# open SPI device 0.0
# spi = spidev.SpiDev()

# read SPI data from MCP3002 chip
# spi.open(0,0)
# flag_file = './flag/transfer_success.flag'
# spi.max_speed_hz = 1000000
# spi.mode = 0

# 表記ゆれリスト
# 'yes'のリスト
yes_variants = ['yes', 'y', 'ok']
# 'no'のリスト
no_variants = ['no', 'n',]

# タイトルコール
print("こんにちは。台パン力測定自己診断プログラムv1.0.0です")
print("途中で終了したい場合   -> ctl + C (ctlとCを同時入力) してください")
print("画面が落ちただけの場合 -> モニタA : python3 bangtable/main_A.py モニタB : python3 bangtable/main_B.py の入力で再開します")
print("本プログラムは、叩いても反応がない・叩くと毎回落ちてしまう・叩いてないのに反応してしまう、という症状に対応しています")
print("\033[31m※実行中は指示がない限り、装置に力を加えないでください\n\033[0m")



def measure(length) -> list:
	# データ取得
	print("測定中", end="")
	data_list = []
	'''
	for i in range(100):
		# read SPI data from MCP3002 chip
		resp = spi.xfer2([0x68,0x00])
		value = (resp[0] * 256 + resp[1]) & 0x3ff
		data_list.append(value)
		# 進捗
		if i % 10 == 0:
			print(".", end="")
	'''
	print("\n")
 
	# ダミーデータ
	data_list = [150, 150, 150, 149, 167, 166, 165, 165, 164, 155, 159]
	return data_list


# バッテリー
def is_battery():
	print("Q1. 圧電センサに接続されている基板のライト(黄色)が点灯していますか？")
	user_input = input("yes or no -> ")
	# 入力がyesでもnoでもない場合
	while user_input not in yes_variants + no_variants:
		print("Error : 無効な入力 'yes' か 'no' で入力してください")
		user_input = input("yes or no -> ")
  # 解答
	print("\n")
	if user_input in yes_variants:
		is_data_reach()
	else:
		print("A1. バッテリーが接続されていません。バッテリーを接続してください\n    ライト(オレンジ)が点灯している場合は、バッテリーを交換してください")

# データ到達
def is_data_reach():
	print(">>> 圧電センサを基板から取り外してください")
	user_input = input("取り外しが完了したら何かキーを入力してください -> ")

	# データ取得
	data_list = measure(100)

	# データ表示
	plt.plot(data_list, marker='o')
	plt.xlabel("Time")
	plt.ylabel("Voltage")
	plt.title("Voltage-Time Graph")
	plt.ylim(0, 1023)
	plt.grid(True)
	plt.show(block=False)

	# 質問
	print("Q2. 表示されたグラフで大きいノイズ(100以上)がある or 300以上の大きな値がある")
	user_input = input("yes or no -> ")
	# 入力がyesでもnoでもない場合
	while user_input not in yes_variants + no_variants:
		print("Error : 無効な入力 'yes' か 'no' で入力してください")
		user_input = input("yes or no -> ")
  # 解答
	plt.close()
	print("\n")
	if user_input in yes_variants:
		print("A2. 配線が外れている可能性があります。配線を確認してください")
	else:
		print(">>> 圧電センサを基板に取り付けて下さい")
		user_input = input("取り付けが完了したら何かキーを入力してください -> ")
		is_hardware_error()

# ハード異常
def is_hardware_error():
	print(">>> 装置に力を加えないでください")
	user_input = input("何かキーを入力してください -> ")

	# データ取得
	data_list = measure(200)

	# データ表示
	plt.plot(data_list, marker='o')
	plt.xlabel("Time")
	plt.ylabel("Voltage")
	plt.title("Voltage-Time Graph")
	plt.ylim(0, 1023)
	plt.grid(True)
	plt.show(block=False)

	# 質問
	print("Q3. 表示されたグラフで大きいノイズ(100以上)がある or 平均的に600以上である")
	user_input = input("yes or no -> ")
	# 入力がyesでもnoでもない場合
	while user_input not in yes_variants + no_variants:
		print("Error : 無効な入力 'yes' か 'no' で入力してください")
		user_input = input("yes or no -> ")
	# 解答
	plt.close()
	print("\n")
	if user_input in yes_variants:
		print("A3. 装置のネジの締め付けが甘いor強い可能性があります。ネジの締め付けを調整してください")
	else:
		is_sensor_error()

# センサ異常
def is_sensor_error():
	print(">>> 測定が終了するまで装置に継続的に力を加えてください")
	user_input = input("キーを入力してください(測定開始) -> ")

	# データ取得
	data_list = measure(200)

	# データ表示
	plt.plot(data_list, marker='o')
	plt.xlabel("Time")
	plt.ylabel("Voltage")
	plt.title("Voltage-Time Graph")
	plt.ylim(0, 1023)
	plt.grid(True)
	plt.show(block=False)

	# 質問
	print("Q4. 先ほどのグラフより大きな値が出ている")
	user_input = input("yes or no -> ")
	# 入力がyesでもnoでもない場合
	while user_input not in yes_variants + no_variants:
		print("Error : 無効な入力 'yes' か 'no' で入力してください")
		user_input = input("yes or no -> ")
	# 解答
	plt.close()
	print("\n")
	if user_input in yes_variants:
		print("わからんので、自己診断は終了します。技術担当者に連絡してください")
	else:
		print("A4. 圧電センサがぶっ壊れてます。交換してください")

# 診断開始
is_battery()

# spi.close()