import  ast
import math

def transmission(data_str):
	data_list = data_str.split(',')
	data_tuple = tuple(int(item.strip()) for item in data_list)
	return data_tuple

class CALC:
	data_tuple = None
	sikiti = 0
 
 
	# コンストラクタ
	def __init__(self, sikiti, path) -> None:
		with open(path, 'r',encoding='utf-8') as data_file:
			self.data_tuple = transmission(data_file.read())
		self.power_data = None
		self.sikiti = sikiti
	
	# 最大値取得
	def GetMax(self) -> list:
		"""_summary_

		Returns:
				list: [最大値, そのインデックス]
		"""
		maximumdata = 0
		index = 0
		#for onedata in self.data:
		for row in range(len(self.data_tuple)):
			#print(self.data_tuple[row])
			# マックス値を取得
			if self.data_tuple[row] > maximumdata:
				index = row
				maximumdata = self.data_tuple[row]
			elif self.data_tuple[row] <= maximumdata:
				pass
			else:
				raise ValueError("なんかよくわからんエラーが出たぞ")
		data = [maximumdata, index]
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

