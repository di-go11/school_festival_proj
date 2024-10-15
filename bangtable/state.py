import time
import calc

class state:
  START = 0
  READY = 1
  BANG = 2
  JUDGE = 3
  SHOW = 4
  
  def __init__(self) -> None:
    self.state = None
    
    
  #生データ参照の状態遷移メソッド
  def BangObserver(self,data) -> None:
    match self.state:
      case state.START:
        if len(data) > 0:
          self.state = state.READY
        elif len(data) == 0:
          self.state = state.START
        else:
          raise ValueError("圧力センサーの数値がおかしい!!")
        
      case state.BANG:
        print(data)
        result = calc.calc(data)
        maximum = result.GetPowerMax()
        print(maximum)
        self.state = state.SHOW
        
      case state.SHOW:
        
  #ノーマル状態遷移メソッド
  def BangObserver(self) -> None:
    match self.state:
      case state.READY:
        time.sleep(5)
        self.state = state.BANG
      
      