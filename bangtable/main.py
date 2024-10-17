# main.py
import pygame
import asyncio
import random


from state import state as State
from animationclass import Animation

animationA = Animation()
animationB = Animation()
stateA = State(animationA)
stateB = State(animationB)


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
				print("SPACE")
				# 台パンデータセット、台パンフラグON
				stateA.set_bang_data(random.randint(0, 999))

		# ステート監視
		stateA.BangObserver()

		await asyncio.sleep(0.1)

	print("-----")
	await gui_A


# ここから動作
asyncio.run(run())