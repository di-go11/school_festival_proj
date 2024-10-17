import  ast

class CALC:
  def __init__(self,sikiti) -> None:
    self.data = None
    self.maximum = None
    self.power_data = None
    self.sikiti = sikiti
    
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
    self.power_data = (self.maximum - self.sikiti) / (self.data.index(self.maximum) + 1)
    return self.power_data
    # adの出力結果が分かり次第後で作る。