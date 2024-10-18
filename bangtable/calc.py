import  ast
import math


class CALC:
	data_tuple = None
	sikiti = 0
 
 
	# コンストラクタ
	def __init__(self, sikiti, path) -> None:
		self.sikiti = sikiti
		# ファイル読み込み
		with open(path, 'r',encoding='utf-8') as data_file:
			self.transmission(data_file.read())
			print(type(self.data_tuple))
			print(self.data_tuple[:150])
			data_file.seek(0)
			data_file.close() # 明示的にファイルを閉じる
		# ファイルクリア
		with open(path, 'w', encoding='utf-8') as data_file:
			print("")
			data_file.flush()  # バッファをディスクに書き込む
			pass


	# データ整形
	def transmission(self, data_str : str):
		data_list = data_str.split(',')
		self.data_tuple = list(int(item.strip()) for item in data_list)
		print(self.data_tuple)
		# return data_tuple



	# 最大値取得
	def GetMax(self) -> list:
		"""_summary_

		Returns:
				list: [最大値, そのインデックス]
		"""
		maximumdata = 0
		index = 0
		#for onedata in self.data:
		for row in range(150):
			#print(self.data_tuple[row])
			# マックス値を取得
			if self.data_tuple[row] > maximumdata:
				index = row
				maximumdata = self.data_tuple[row]
			elif self.data_tuple[row] <= maximumdata:
				pass
			else:
				raise ValueError("なんかよくわからんエラーが出たぞ")
		del self.data_tuple
		print(self.data_tuple)
		data = [maximumdata, index]
		print(data)
		return data

	# def GetAlldata(self) -> tuple:
	# 実際に出すデータ
	def GetMaxPower(self, mode : int) -> int:
		"""_summary_

		Args:
				mode (_int_): _参号機(最大値が511)は1、弐号機(最大値が1023)は2_

		Returns:
				int: _データ出力_
		"""
		formatted_data = self.GetMax()
		maximum = formatted_data[0]
		index = formatted_data[1]
		# 計算
		data = 1000 + (maximum - self.sikiti)/mode - 25 * math.sqrt(8*index - 39)
		return round(data)

