import  ast

class calc:
  def __init__(self) -> None:
    self.data = None
    self.maximum = None
    self.power_data = None
    
  def GetMax(self) -> int:
    maximumdata = 0
    for onedata in self.data:
      if onedata > maximumdata:
        maximumdata = onedata
      elif onedata <= maximumdata:
        pass
      else:
        raise ValueError("なんかよくわからんエラーが出たぞ")
    self.maximum = maximumdata
    return self.maximum
  
  def GetAlldata(self,data) -> tuple:
    with open("./data/data.txt", "r") as file:
      data_tuple = ast.literal_eval(file.strip())
    self.data = data_tuple
    return self.data  
  
  def GetPowerData(self) -> list:
    sikiti = 
    self.power_data = (self.maximum - sikiti) / (self.data.index(self.maximum) + 1)
    return self.power_data
    # adの出力結果が分かり次第後で作る。