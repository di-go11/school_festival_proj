import pygame
import os
import asyncio
import random
import time

class Animation:
	FIRST = 0
	READY = 1
	BANG = 2
	RESULT = 3

	# 状況
	status = FIRST
	# スクリーン
	screen_width = 1280
	screen_height = 1024
	screen = None
	# フォントオブジェクトの作成
	font_num = None
	font_text = None
	font_path = "/home/tanaka-iiyama-linux-pc/school_festival_proj/font/DShirkg8.ttc"

	# 結果桁数
	digit = 0
	flag = True
	# 結果表示テキスト
	text_1 = None
	text_2 = None
	text_3 = None
	text = None
	# 3桁目の数字
	data_1 = 0

	# タスク
	first_task = None
	ready_task = None
	bang_task = None
	result_task = None

	# ダイパンデータ
	bang_data = 0
	# 台パン可能か
	can_bang_flag = False

	# コンストラクタ
	def __init__(self, monitor_num : int = 0):
		pos = 1920 + self.screen_width * monitor_num
		# ウィンドウの位置を設定（左上の位置を100px, 100pxに移動）
		os.environ['SDL_VIDEO_WINDOW_POS'] = str(pos) + ',0'  # x, y座標

		# Pygameを初期化
		pygame.init()
		# デイスプレイ表示
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
		# ウィンドウのタイトルを設定
		pygame.display.set_caption("Animation")
		# 背景色を黒に設定
		self.screen.fill((0, 0, 0))
		# フォントサイズ
		self.font_num = pygame.font.Font(None, 800)
		self.font_text = pygame.font.Font(self.font_path, 100)

	# ステート変更
	def set_bang_flag(self, state : int, data : int = 0):
		self.status = state
		self.bang_data = data
	# 台パン可能か
	def get_can_bang_flag(self) -> bool:
		return self.can_bang_flag

	# 状態遷移処理
	async def main(self, status : int):
		# 状態セット
		self.status = status

		# 今までのタスクをキャンセル
		if self.first_task != None:
			self.first_task.cancel()
		if self.ready_task != None:
			self.ready_task.cancel()
		if self.bang_task != None:
			self.bang_task.cancel()
		if self.result_task != None:
			self.ready_task.cancel()

		# 状態によって処理を分岐
		while True:
			if self.status == self.FIRST:
				self.first_task = asyncio.create_task(self.first())
				await self.first_task
			if self.status == self.READY:
				self.ready_task = asyncio.create_task(self.ready())
				await self.ready_task
			if self.status == self.BANG:
				self.bang_task = asyncio.create_task(self.bang())
				await self.bang_task
			if self.status == self.RESULT:
				self.result_task = asyncio.create_task(self.result())
				await self.result_task


	# 最初の状態
	async def first(self):
		# テキスト確定
		font_start = pygame.font.Font(self.font_path, 180)
		text_start = font_start.render("台パン力測定", True, (255, 255, 255))
		text_5S = font_start.render("5S", True, (255, 255, 255))
		text_start_bang = self.font_text.render("▽タッチしてスタート！", True, (255, 255, 255))

		# 描画
		self.screen.fill((0, 0, 0))
		self.screen.blit(text_start, text_start.get_rect(center=(self.screen_width/2, self.screen_height/2)))
		self.screen.blit(text_5S, text_5S.get_rect(center=(self.screen_width/2, self.screen_height * 1/4)))
		# 叩いてスタート！
		text_start_bang_height = self.screen_height * 5/6
		self.screen.blit(text_start_bang, text_start_bang.get_rect(center=(self.screen_width/2, text_start_bang_height)))
		# 反映
		pygame.display.flip()

		# アニメーションパラメータ設定
		v = -4
		a = 0.2
		pos_height = text_start_bang_height
  
		# 次の画面に遷移可能
		self.can_bang_flag = True
		# アニメーションループ
		ruuning = True
		while ruuning:
			'''
			for event in pygame.event.get():
				# ウィンドウを閉じるイベント処理
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					running = False
					return  # ループを抜けて終了
			'''
			# ステートが変わったら終了
			if self.status != self.FIRST:
				self.can_bang_flag = False
				running = False
				return	# ループを抜けて終了


			# 移動処理
			v = v + a
			pos_height = pos_height + v
			# 前の描画を消す
			square_rect = pygame.Rect((0, self.screen_height * 3/5), (self.screen_width, self.screen_height/3))
			pygame.draw.rect(self.screen, (0, 0, 0), square_rect)
			# 描画
			self.screen.blit(text_start_bang, text_start_bang.get_rect(center=(self.screen_width/2, pos_height)))
			pygame.display.flip()
			if pos_height > text_start_bang_height:
				v = -4
			# スリープ
			await asyncio.sleep(0.01)


	# 準備状態
	async def ready(self):
		# 残り秒数
		rest_time = 5

		# テキスト確定
		font_charge = pygame.font.Font(self.font_path, 180)
		text_charge = font_charge.render("力を溜めろ！", True, (255, 255, 255))
		text_to = self.font_text.render("台パンまで", True, (255, 255, 255))
		font_rest_time = pygame.font.Font(None, 800)
		text_rest_time = font_rest_time.render(str(rest_time), True, (255, 255, 255))

		# 描画
		self.screen.fill((0, 0, 0))
		self.screen.blit(text_charge, text_charge.get_rect(center=(self.screen_width/2, self.screen_height/4)))
		self.screen.blit(text_to, text_to.get_rect(center=(self.screen_width/4, self.screen_height * 5/6)))
		self.screen.blit(text_rest_time, text_rest_time.get_rect(center=(self.screen_width * 7/10, self.screen_height * 8/11)))
  
		# 反映
		pygame.display.flip()

		# アニメーションループ
		start_time = current_time = time.time()
		ruuning = True
		while ruuning:
			for event in pygame.event.get():
				# ウィンドウを閉じるイベント処理
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					running = False
					return  # ループを抜けて終了

			# 1秒経過したらフラグを立てる
			if (current_time - start_time) >= 1.0:
				start_time = current_time
				rest_time -= 1
				# 秒数を更新
				font_rest_time = pygame.font.Font(None, 800)
				text_rest_time = font_rest_time.render(str(rest_time), True, (255, 255, 255))
				text_rest_time_rect = text_rest_time.get_rect(center=(self.screen_width * 7/10, self.screen_height * 8/11))
				square_rect = pygame.Rect((self.screen_width/2, self.screen_height/3), (self.screen_width/2, self.screen_height * 23/33))
				# 配置
				pygame.draw.rect(self.screen, (0, 0, 0), square_rect)
				self.screen.blit(text_rest_time, text_rest_time_rect)
				# 反映
				pygame.display.flip()

			# 0秒になったら終了
			if rest_time == 0:
				self.status = self.BANG
				running = False
				return	# ループを抜けて終了

			# 文字切り替えアニメーション
			if(current_time - start_time) == 0:
				for i in range(20):
					index = 19 - i
					font_rest_time_alpha = pygame.font.Font(None, int(800 + 10 * (index^4)))
					text_rest_time_alpha = font_rest_time_alpha.render(str(rest_time), True, (255, 255, 255))
					text_rest_time_alpha_rect = text_rest_time_alpha.get_rect(center=(self.screen_width * 7/10, self.screen_height * 8/11))
					square_rect = pygame.Rect((self.screen_width/2, self.screen_height/3), (self.screen_width/2, self.screen_height * 23/33))
					# 配置
					pygame.draw.rect(self.screen, (0, 0, 0), square_rect)
					self.screen.blit(text_rest_time_alpha, text_rest_time_alpha_rect)
					# 反映
					pygame.display.flip()
					await asyncio.sleep(0.0001)

				# 秒数を更新
				font_rest_time = pygame.font.Font(None, 800)
				text_rest_time = font_rest_time.render(str(rest_time), True, (255, 255, 255))
				text_rest_time_rect = text_rest_time.get_rect(center=(self.screen_width * 7/10, self.screen_height * 8/11))
				square_rect = pygame.Rect((self.screen_width/2, self.screen_height/3), (self.screen_width/2, self.screen_height * 23/33))
				# 配置
				pygame.draw.rect(self.screen, (0, 0, 0), square_rect)
				self.screen.blit(text_rest_time, text_rest_time_rect)
				# 反映
				pygame.display.flip()

			# 秒数を更新
			current_time = time.time()
			await asyncio.sleep(0.01)


	# 叩く画面
	async def bang(self):
		# テキスト確定
		font_bang = pygame.font.Font(self.font_path, 260)
		text_bang = font_bang.render("たたけ！", True, (255, 255, 255))
		font_arrow = pygame.font.Font(self.font_path, 200)
		text_arrow = font_arrow.render("▼", True, (255, 255, 255))

		# 描画
		self.screen.fill((0, 0, 0))
		self.screen.blit(text_bang, text_bang.get_rect(center=(self.screen_width/2, self.screen_height/2)))
		self.screen.blit(text_arrow, text_arrow.get_rect(center=(self.screen_width/2, self.screen_height * 7/8)))

		# 反映
		pygame.display.flip()

		# 次の画面に遷移可能
		self.can_bang_flag = True
		# アニメーションループ
		ruuning = True
		while ruuning:

			# BANGステートでなくなったら終了
			if self.status != self.BANG:
				self.can_bang_flag = False
				running = False
				return	# ループを抜けて終了

			await asyncio.sleep(0.01)


	# 結果画面
	async def result(self):
		self.data_1 = self.bang_data // 100
		data_2 = (self.bang_data - self.data_1 * 100) // 10
		data_3 = self.bang_data - self.data_1 * 100 - data_2 * 10

		# 表示するテキストをレンダリング
		if self.data_1 == 0:
			self.text_1 = self.font_num.render("  ", True, (255, 255, 255))  # 白色のテキスト
		else:
			self.text_1 = self.font_num.render(str(self.data_1), True, (255, 255, 255))  # 白色のテキスト
		self.text_2 = self.font_num.render(str(data_2), True, (255, 255, 255))  # 白色のテキスト
		self.text_3 = self.font_num.render(str(data_3), True, (255, 255, 255))  # 白色のテキスト

		# グローバル変数
		self.digit = 0
		self.flag = True
	
		# 画面クリア
		self.screen.fill((0, 0, 0))
  
		# 非同期タスクを作成
		hello_task = asyncio.create_task(self.make_random())
		seconds_task = asyncio.create_task(self.display_seconds_after_delay())

		# 終了するまで実行
		await seconds_task
		# 終了した後にhello_taskをキャンセル
		hello_task.cancel()
		
		# 表示のタスクが終わるまでは待機
		await asyncio.gather(hello_task, seconds_task)

		# 次の画面に遷移可能
		self.can_bang_flag = True
		# RESULTステートでなくなったら終了
		running = True
		while running:
			if self.status != self.RESULT:
				self.can_bang_flag = False
				running = False
				return	# ループを抜けて終了
  
			await asyncio.sleep(0.01)

	# 数字フォーマット
	def formatter(self, num) -> int:
		if num > 9:
			return 10-num
		elif num < 0:
			return 10+num
		else:
			return num

	# ランダム数字表示
	async def make_random(self):
		while self.flag:
			# テキストを表示
			for i in range(3-self.digit):
				# テキスト確定
				ramdom_text = self.font_num.render(str(random.randint(0, 9)), True, (255, 255, 255))
				ramdom_text_rect = ramdom_text.get_rect(center=(self.screen_width/4 * (i+1), self.screen_height/2))

				# テキストを消す
				# テキストの位置とサイズを基に四角形を作成
				square_rect = pygame.Rect(ramdom_text_rect.topleft, (ramdom_text_rect.width, ramdom_text_rect.height))

				# 描画
				pygame.draw.rect(self.screen, (0, 0, 0), square_rect)
				self.screen.blit(ramdom_text, ramdom_text_rect)

			# 反映
			pygame.display.flip()

			# 0.1秒待機
			await asyncio.sleep(0.05)

	# 結果表示
	async def display_seconds_after_delay(self):		
		# 1秒後
		await asyncio.sleep(1)
		self.digit = 1
		text_3_rect = self.text_3.get_rect(center=(self.screen_width/4 * 3, self.screen_height/2))
		pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(text_3_rect.topleft, (text_3_rect.width, text_3_rect.height)))
		self.screen.blit(self.text_3, text_3_rect)
		pygame.display.flip()

		# 2秒後
		await asyncio.sleep(1.5)
		self.digit = 2
		text_2_rect = self.text_2.get_rect(center=(self.screen_width/4 * 2, self.screen_height/2))
		pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(text_2_rect.topleft, (text_2_rect.width, text_2_rect.height)))
		self.screen.blit(self.text_2, text_2_rect)
		pygame.display.flip()

		# 3秒後
		await asyncio.sleep(2)
		self.digit = 3
		self.flag = False

		# 減速処理
		for i in range(2):
			num = 5-(2*i)
			for j in range(num):
				# テキスト確定
				if i == 0:
					ramdom_text = self.font_num.render(str(random.randint(0, 9)), True, (255, 255, 255))
				else:
					# ゆっくり表示
					ramdom_text = self.font_num.render(str(self.formatter(self.data_1-(num-j))), True, (255, 255, 255))
				ramdom_text_rect = ramdom_text.get_rect(center=(self.screen_width/4, self.screen_height/2))

				# テキストを消す
				# テキストの位置とサイズを基に四角形を作成
				square_rect = pygame.Rect(ramdom_text_rect.topleft, (ramdom_text_rect.width, ramdom_text_rect.height))

				# 描画
				pygame.draw.rect(self.screen, (0, 0, 0), square_rect)
				self.screen.blit(ramdom_text, ramdom_text_rect)
				pygame.display.flip()

				# 0.1秒待機
				if i == 0:
					await asyncio.sleep(0.1)
				else:
					await asyncio.sleep(0.7)
		
		await asyncio.sleep(0.6)
	
		# ランク判定
		font_award = pygame.font.Font(self.font_path, 100)
		font_rank = pygame.font.Font(self.font_path, 60)
		text_rank = None
		if self.bang_data == 0 or self.bang_data == 999:
			text_rank = font_rank.render("<< もはやバグ 係員呼んで >>", True, (255, 255, 255))
		elif self.bang_data == 404:
			text_rank = font_rank.render("<< 404 Not Found >>", True, (255, 255, 255))
		elif self.bang_data == 777:
			text_rank = font_rank.render("<< ラッキー台パン！ >>", True, (255, 255, 255))
		elif self.bang_data < 100:
			text_rank = font_rank.render("< 机に優しい台パン >", True, (255, 255, 255))
		elif self.bang_data < 200:
			text_rank = font_rank.render("< お手伝い台パン >", True, (255, 255, 255))
		elif self.bang_data < 300:
			text_rank = font_rank.render("< 周囲配慮系台パン >", True, (255, 255, 255))
		elif self.bang_data < 400:
			text_rank = font_rank.render("< ムカ着火ファイヤー >", True, (255, 255, 255))
		elif self.bang_data < 500:
			text_rank = font_rank.render("< 堪忍袋炸裂 >", True, (255, 255, 255))
		elif self.bang_data < 600:
			text_rank = font_rank.render("< ストレスバイバイ >", True, (255, 255, 255))
		elif self.bang_data < 700:
			text_rank = font_rank.render("< 上級ダイパリスト >", True, (255, 255, 255))
		elif self.bang_data < 800:
			text_rank = font_rank.render("< 机破壊予備軍 >", True, (255, 255, 255))
		elif self.bang_data < 900:
			text_rank = font_rank.render("< 破壊神 >", True, (255, 255, 255))
		else:
			text_rank = font_rank.render("< 修理屋泣かせ >", True, (255, 255, 255))

		# 最終結果表示
		text_1_rect = self.text_1.get_rect(center=(self.screen_width/4 * 1, self.screen_height/2)) # 画面クリア
		pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(text_1_rect.topleft, (text_1_rect.width, text_1_rect.height)))
		# self.screen.blit(text_rank, text_rank.get_rect(center=(self.screen_width/2, self.screen_height * 2/12))) # ランク
		self.screen.blit(self.text_1, text_1_rect)

		pygame.display.flip()

		await asyncio.sleep(0.5)

		# 点滅処理
		for i in range(3):
			await asyncio.sleep(0.25) 
			pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect((0, self.screen_height * 3/12), (self.screen_width, self.screen_height * 5/11)))
			pygame.display.flip()

			await asyncio.sleep(0.15)
			self.screen.blit(self.text_3, text_3_rect)
			self.screen.blit(self.text_2, text_2_rect)
			self.screen.blit(self.text_1, text_1_rect)
			pygame.display.flip()

		# ランク表示
		text_award = font_award.render("-称号-", True, (255, 255, 255))
		self.screen.blit(text_award, text_award.get_rect(center=(self.screen_width/2, self.screen_height * 1/12)))
		self.screen.blit(text_rank, text_rank.get_rect(center=(self.screen_width/2, self.screen_height * 2/11)))
  
		text_unit = self.font_text.render("㌔ダイパン", True, (255, 255, 255))  # 単位
		self.screen.blit(text_unit, text_unit.get_rect(center=(self.screen_width * 8/11, self.screen_height * 8/10)))
		pygame.display.flip()





'''
# 全部をこの関数内で定義する必要がある
async def run(animation : Animation):
	start_task = asyncio.create_task(animation.main(Animation.FIRST))
	
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
				animation.set_bang_flag(892)
  
		await asyncio.sleep(0.1)

	print("-----")
	await start_task



asyncio.run(run(Animation()))'''
