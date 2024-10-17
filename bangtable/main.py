# main.py
import pygame
import asyncio
import random

from state import state as State
from animationclass import Animation

animationA = Animation()
animationB = Animation()
stateA = State(animationA, '/home/bangtable001/data/data.txt', 280)
stateB = State(animationB, '/home/bangtable002/data/data.txt', 280)


flag_A_path = '/home/bangtable001/data/flag.txt'
flag_B_path = '/home/bangtable002/data/flag.txt'


# 全部をこの関数内で定義する必要がある
async def run():
	gui_A = asyncio.create_task(animationA.main(Animation.FIRST))
	
	running = True
	while running:
		for event in pygame.event.get():
			# ウィンドウを閉じるイベント処理
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				print("ESC")
				running = False
				return
			# ダイパントリガ(仮)
			if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
				# ファイルを開く (書き込みモード 'w')
				with open(flag_A_path, 'w', encoding='utf-8') as file:
					file.write("True")


		# 台パンフラグ読み込み
		with open(flag_A_path, 'rb+') as file:
			content = file.read()
			true_str = ''.join(format(byte, '02x') for byte in ("True").encode('utf-8'))
			read_str = ''.join(format(byte, '02x') for byte in content)
			print(read_str + " : " + true_str)
			if (str(content.hex()) == true_str):
				print("flag")
				# 台パンデータセット、台パンフラグON
				stateA.set_bang_flag()
				# フラグリセット
				file.seek(0)
				file.write("False".encode('utf-8'))
		# ステート監視
		stateA.BangObserver()

		await asyncio.sleep(0.1)

	print("-----")
	await gui_A


# ここから動作
asyncio.run(run())
