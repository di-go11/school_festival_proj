import spidev
import time
import sys

class data:
  
  def __init__(self) -> None:
    self.data_input_pin,
    self.read_addr = 0x00
    self.write_adde = 0x1E
    self.write_data = 0x08
    self.spi = apidev.SpiDev()
    
  def init_conf(self) -> None:
    self.spi.open(0,0)
    self.spi.mode = 3
    self.spi.max_speed_hz = 1000000
    
  def readaddr(self) -> list:
    read_data = spi.xfer2([0x80 | self.read_addr, 0x00])
    self.spi