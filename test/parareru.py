import RPi.GPIO as GPIO
import sys
import os
import time

class pareru:
  def __init__(self) -> None:
    self.data_PIN_list = list(range(4,11))
    self.data_list = [8]
    self.stat_PIN = 19
    self.CE_PIN = 20
    self.R_W_PIN = 21
    self.result = []
    
  def set_up(self) -> None:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.data_list, GPIO.IN)
    GPIO.setup(self.stat_PIN, GPIO.IN)
    GPIO.setup(self.CE_PIN, GPIO.OUT)
    GPIO.setup(self.R_W_PIN, GPIO.OUT)
    
  def get_data(self) -> list:
    for i in range(0,7):
      self.data_list[i] = GPIO.input(self.data_PIN_list[i])
    return self.data_list
  
  def seigyo(self):
    GPIO.output(self.CE_PIN,GPIO.HIGH)
    GPIO.output(self.R_W_PIN, GPIO.LOW)
    GPIO.output(self.CE_PIN,GPIO.LOW)
    GPIO.output(self.R_W_PIN,GPIO.HIGH)
    if GPIO.input(self.stat_PIN) == GPIO.LOW:
      self.data_list = self.get_data()
    return self.data_list
  
if __name__ == "__main__":
  para = pareru()
  para.set_up()
  add = para.seigyo()
  print(add)