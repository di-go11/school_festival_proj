from animationclass import Animation
from calc import calc

import time

class state:
	START = 0
	BANG = 1
	SHOW = 2

	state : int = None
	animation : Animation = None

	# 台パンフラグ
	bang_flag : bool = False
	bang_data : int = 0

	# タイマ割込み用
	time_start : float = None
	
	def __init__(self, animation) -> None:
		self.state = state.START
		self.animation = animation
	
	# 台パンデータセット
	def set_bang_data(self, data : int) -> None:
		self.bang_flag = True
		self.bang_data = data

		
	# 状態遷移メソッド
	def BangObserver(self) -> None:
		match self.state:
			# START
			case state.START:
				# 台パンされてたら
				if self.bang_flag:
					self.bang_flag = False
					# 台パン可能であれば、BANG状態に遷移
					if self.animation.get_can_bang_flag():
						self.animation.set_bang_flag(Animation.READY)
						self.state = state.BANG
			# BANG
			case state.BANG:
				# 台パンされてたら
				if self.bang_flag:
					self.bang_flag = False
					# 台パン可能であれば、SHOW状態に遷移
					if self.animation.get_can_bang_flag():
						# データ計算
						#print(self.bang_data)
						#result = calc.calc(self.bang_data)
						#maximum = result.GetPowerMax()
						#print(maximum)
						# 結果表示 仮でbangdata
						self.animation.set_bang_flag(Animation.RESULT, self.bang_data)
						self.state = state.SHOW
						# タイマ設定
						self.time_start = time.time()
			# SHOW
			case state.SHOW:
				# 台パンされてたら or 20秒以上経過してたら
				if self.bang_flag or (time.time() - self.time_start >= 20):
					self.bang_flag = False
					# 台パン可能であれば、first状態に遷移 or 20秒後にfirst状態に遷移
					if self.animation.get_can_bang_flag():
						self.animation.set_bang_flag(Animation.FIRST)
						self.state = state.START
