class calc:
  def __init__(self,data) -> None:
    self.data = data
    self.maximum = None
    self.power_data = None
    
  def GetPowerMax(self) -> int:
    maximumdata = 0
    for onedata in self.power_data:
      if onedata > maximumdata:
        maximumdata = onedata
      elif onedata <= maximumdata:
        pass
      else:
        raise ValueError("なんかよくわからんエラーが出たぞ")
    self.maximum = maximumdata
    return self.maximum
  
  def GetAlldata(self) -> None:
    print(self.data)
  
  def GetAllPowerData(self) -> list:
    # adの出力結果が分かり次第後で作る。