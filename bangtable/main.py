# main.py
import pygame
import asyncio
import random


from state import state as State
from animationclass import Animation

animationA = Animation()
animationB = Animation()
stateA = State(animationA, 'bangtable/data/data01.txt', 280)
stateB = State(animationB, 'bangtable/data/data02.txt', 280)

flag_A_path = 'bangtable/data/flag01.txt'
flag_B_path = 'bangtable/data/flag02.txt'


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
		with open(flag_A_path, 'r+', encoding='utf-8') as file:
			content = file.read()
			if (content == "True"):
				print("flag")
				# 台パンデータセット、台パンフラグON
				stateA.set_bang_flag()
				# フラグリセット
				file.seek(0)
				file.write("False")

		# ステート監視
		stateA.BangObserver()

		await asyncio.sleep(0.1)

	print("-----")
	await gui_A


# ここから動作
asyncio.run(run())