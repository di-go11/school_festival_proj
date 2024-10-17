import  ast

def transmission(data_str):
  data_list = data_str.split(',')
  data_tuple = tuple(int(item.strip()) for item in data_list)
  return data_tuple

class CALC:
  def __init__(self,sikiti) -> None:
    with open('./data/data.txt','r',encoding='utf-8') as data_file:
      self.data_tuple = transmission(data_file.read())
    self.power_data = None
    self.sikiti = sikiti
    
  def GetMax(self) -> int:
    maximumdata = 0
    #for onedata in self.data:
    for row in range(len(self.data_tuple)):
      #print(self.data_tuple[row])
      if self.data_tuple[row] > maximumdata:
        maximumdata = self.data_tuple[row]
      elif self.data_tuple[row] <= maximumdata:
        pass
      else:
        raise ValueError("なんかよくわからんエラーが出たぞ")
    data = [maximumdata,len(self.data_tuple)]
    return data

  # def GetAlldata(self) -> tuple:

  
  def GetPowerData(self) -> list:
    maximum = (self.GetMax())[0]
    count = (self.GetMax())[1]
    self.power_data = (maximum - self.sikiti) / (count + 1)
    print(self.power_data)
    #return self.power_data
    # adの出力結果が分かり次第後で作る。