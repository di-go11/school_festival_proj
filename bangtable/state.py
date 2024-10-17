from animationclass import Animation
from calc import CALC

import time

class state:
	START = 0
	BANG = 1
	SHOW = 2

	state : int
	animation : Animation

	# 台パンフラグ
	bang_flag : bool = False

	# タイマ割込み用
	time_start : float
	
	# データファイルパス
	data_path : str
	threshold : int
	
	def __init__(self, animation, path, threshold) -> None:
		self.state = state.START
		self.animation = animation
		self.data_path = path
		self.threshold = threshold
	
	# 台パンデータセット
	def set_bang_flag(self) -> None:
		self.bang_flag = True

		
	# 状態遷移メソッド
	def BangObserver(self) -> None:
		# START
		if self.state == state.START:
			# 台パンされてたら
			if self.bang_flag:
				self.bang_flag = False
				# 台パン可能であれば、BANG状態に遷移
				if self.animation.get_can_bang_flag():
					self.animation.set_bang_flag(Animation.READY)
					self.state = state.BANG
		# BANG
		elif self.state == state.BANG:
			# 台パンされてたら
			if self.bang_flag:
				self.bang_flag = False
				# 台パン可能であれば、SHOW状態に遷移
				if self.animation.get_can_bang_flag():
					# データ計算
					calc = CALC(self.threshold, self.data_path)
					maximum = (calc.GetMax())[0]
					print(maximum)
					# 結果表示 仮でbangdata
					self.animation.set_bang_flag(Animation.RESULT, maximum)
					self.state = state.SHOW
					# タイマ設定
					self.time_start = time.time()
		# SHOW
		elif self.state == state.SHOW:
			# 台パンされてたら or 20秒以上経過してたら
			if self.bang_flag or (time.time() - self.time_start >= 40):
				self.bang_flag = False
				# 台パン可能であれば、first状態に遷移 or 20秒後にfirst状態に遷移
				if self.animation.get_can_bang_flag():
					self.animation.set_bang_flag(Animation.FIRST)
					self.state = state.START
