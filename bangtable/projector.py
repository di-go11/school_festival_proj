import pygame
import asyncio
import time
import random



class Queue:
	def __init__(self, max_size):
		self.queue = []
		self.max_size = max_size

	def enqueue(self, item):
		if len(self.queue) < self.max_size:
			self.queue.append(item)
		else:
			# 古いアイテムを削除して新しいアイテムを追加
			removed_item = self.queue.pop(0)  # 最も古いアイテムを削除
			self.queue.append(item)  # 新しいアイテムを追加

	def dequeue(self):
		if self.queue:
			item = self.queue.pop(0)
			return item
		else:
			print("Queue is empty!")

	def size(self):
		return len(self.queue)

	def is_empty(self):
		return len(self.queue) == 0

	def is_full(self):
		return len(self.queue) == self.max_size

	def get_contents(self):
		return list(self.queue)  # キューの全ての中身をリストとして返す


class Projector:
	# スクリーン
	screen = None
	screen_width = 1920 / 1.25
	screen_height = 1024 / 1.25
	# データ
	bang_data_list = []
	max_bang_data = 0
	size = 4
	# フォント
	# font_path = "/home/tanaka-iiyama-linux-pc/school_festival_proj/font/DShirkg8.ttc"
	font_path = "school_festival_proj/font/DShirkg8.ttc"
	font_text = None
	font_unit = None

	def __init__(self):
		# データリスト初期化
		self.bang_data_list.append(Queue(self.size))
		self.bang_data_list.append(Queue(self.size))
  
		# デイスプレイ表示
		pygame.init()
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
		# ウィンドウのタイトルを設定
		pygame.display.set_caption("Animation")
		# 背景色を黒に設定
		self.screen.fill((0, 0, 0))
  
		# 文字表示
		self.font_text = pygame.font.Font(self.font_path, 70)
		self.font_unit = pygame.font.Font(self.font_path, 35)

		text_bangtableA = self.font_text.render("台パン測定器A", True, (255, 255, 255))
		text_bangtableB = self.font_text.render("台パン測定器B", True, (255, 255, 255))
		text_max = pygame.font.Font(self.font_path, 100).render("最高得点", True, (255, 255, 255))
		text_max = pygame.font.Font(self.font_path, 100).render("最高得点", True, (255, 255, 255))
		text_max_unit = self.font_unit.render("㌔ダイパン", True, (255, 255, 255))

		self.screen.blit(text_max, text_max.get_rect(center=(self.screen_width * 3/13, self.screen_height/6)))
		self.screen.blit(text_max_unit, text_max_unit.get_rect(center=(self.screen_width * 11/13, self.screen_height/6 + 35)))
		self.screen.blit(text_bangtableA, text_bangtableA.get_rect(center=(self.screen_width/4, self.screen_height/3 +35)))
		self.screen.blit(text_bangtableB, text_bangtableB.get_rect(center=(self.screen_width* 3/4, self.screen_height/3 + 35)))
		square_rect = pygame.Rect((self.screen_width/2, self.screen_height/3), (4, self.screen_height * 2/3))
		pygame.draw.rect(self.screen, (255, 255, 255), square_rect)
		# 単位
		for i in range(4):
			text_unit = self.font_unit.render("㌔ダイパン", True, (255, 255, 255))
			self.screen.blit(text_unit, text_unit.get_rect(center=(self.screen_width* 1/4 + 200, self.screen_height/3 + self.screen_height * 2/3 / 5 * (i + 1) + 18)))
			self.screen.blit(text_unit, text_unit.get_rect(center=(self.screen_width* 3/4 + 200, self.screen_height/3 + self.screen_height * 2/3 / 5 * (i + 1) + 18)))

		# 反映
		pygame.display.flip()

	# データ追加
	def add_data(self, index, data):
		#	データ追加
		bang_data = [data, time.strftime("%H:%M:%S", time.localtime())]
		(self.bang_data_list[index]).enqueue(bang_data)
		print(self.bang_data_list[index].get_contents())
		# 表示クリア
		if index == 0:
			square_rect = pygame.Rect((0, self.screen_height * 13/31), (self.screen_width* 10/31, self.screen_height * 2/3))
		else:
			square_rect = pygame.Rect((self.screen_width/2 + 5, self.screen_height * 13/31), (self.screen_width* 10/31, self.screen_height * 2/3))
		pygame.draw.rect(self.screen, (0, 0, 0), square_rect)
		# データ表示
		for i in range(self.size):
			# データ表示
			if i < len(self.bang_data_list[index].get_contents()):
				text_data = self.font_text.render(str(self.bang_data_list[index].get_contents()[i][0]), True, (255, 255, 255))
				text_time = self.font_unit.render(str(self.bang_data_list[index].get_contents()[i][1]), True, (255, 255, 255))
				self.screen.blit(text_data, text_data.get_rect(center=(self.screen_width * (1/4 + index/2), self.screen_height/3 + self.screen_height * 2/3 / 5 * (i + 1))))
				self.screen.blit(text_time, text_time.get_rect(center=(self.screen_width * (1/4 + index/2) - 200, self.screen_height/3 + self.screen_height * 2/3 / 5 * (i + 1) + 13)))

		# 最高得点表示
		if data > self.max_bang_data:
			self.max_bang_data = data
			square_rect = pygame.Rect((self.screen_width * 4/10, 0), (400, self.screen_height/6 + 100))
			pygame.draw.rect(self.screen, (0, 0, 0), square_rect)
			text_max_data = pygame.font.Font(self.font_path, 130).render(str(data), True, (255, 255, 255))
			self.screen.blit(text_max_data, text_max_data.get_rect(center=(self.screen_width * 6/11, self.screen_height/6)))

		# 反映
		pygame.display.flip()

  
	async def main(self):
		while True:
			for event in pygame.event.get():
				# ウィンドウを閉じるイベント処理
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					print("ESC")
					return
				# 仮トリガ
				if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
					print("SPACE")
					self.add_data(1, random.randint(0, 999))
			await asyncio.sleep(0.1)


async def run():
	start_task = asyncio.create_task(Projector().main())
	await start_task

asyncio.run(run())