#!/usr/bin/python
import time
import math
import smbus
import sys
# ============================================================================
#Raspi PCA9685 16-Channel PWM Servo Driver
# ============================================================================
class PCA9685:
  # Registers/etc.
  __SUBADR1 = 0x02
  __SUBADR2 = 0x03
  __SUBADR3 = 0x04
  __MODE1 = 0x00
  __PRESCALE = 0xFE
  __LED0_ON_L = 0x06
  __LED0_ON_H = 0x07
  __LED0_OFF_L = 0x08
  __LED0_OFF_H = 0x09
  __ALLLED_ON_L = 0xFA
  __ALLLED_ON_H = 0xFB
  __ALLLED_OFF_L = 0xFC
  __ALLLED_OFF_H = 0xFD
  def __init__(self, bus, address=0x40, debug=False):
    #self.bus = smbus.SMBus(1)
    self.bus = bus
    self.address = address
    self.debug = debug
    if (self.debug):
      print("Reseting PCA9685")
    self.write(self.__MODE1, 0x00)

  def write(self, reg, value):
    "Writes an 8-bit value to the specified register/address"
    self.bus.write_byte_data(self.address, reg, value)
    if (self.debug):
      print("I2C: Write 0x%02X to register 0x%02X" % (value, reg))

  def read(self, reg):
    "Read an unsigned byte from the I2C device"
    result = self.bus.read_byte_data(self.address, reg)
    if (self.debug):
      print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, result & 0xFF, reg))
    return result

  def setPWMFreq(self, freq):
    "Sets the PWM frequency"
    prescaleval = 25000000.0 # 25MHz
    prescaleval /= 4096.0 # 12-bit
    prescaleval /= float(freq)
    prescaleval -= 1.0
    if (self.debug):
      print("Setting PWM frequency to %d Hz" % freq)
      print("Estimated pre-scale: %d" % prescaleval)
    prescale = math.floor(prescaleval + 0.5)
    if (self.debug):
      print("Final pre-scale: %d" % prescale)
    oldmode = self.read(self.__MODE1);
    newmode = (oldmode & 0x7F) | 0x10 # sleep
    self.write(self.__MODE1, newmode) # go to sleep
    self.write(self.__PRESCALE, int(math.floor(prescale)))
    self.write(self.__MODE1, oldmode)
    time.sleep(0.005)
    self.write(self.__MODE1, oldmode | 0x80)

  def setPWM(self, channel, on, off):
    "Sets a single PWM channel"
    self.write(self.__LED0_ON_L+4*channel, on & 0xFF)
    self.write(self.__LED0_ON_H+4*channel, on >> 8)
    self.write(self.__LED0_OFF_L+4*channel, off & 0xFF)
    self.write(self.__LED0_OFF_H+4*channel, off >> 8)
    if (self.debug):
      print("channel: %d SERVO POS: %d" % (channel,off))

  def setServoPulse(self, channel, pulse):
    "Sets the Servo Pulse,The PWM frequency must be 50HZ"
    pulse = pulse*4096/20000 #PWM frequency is 50HZ,the period is 20000us
    self.setPWM(channel, 0, int(pulse))


def moveAcc(servo, pos):
	poss = pos*mbl_bots.SCALE_ACC + mbl_bots.CNT_ACC
	self.pwm.setServoPulse(int(self.actuators[int(self.acc_dic[name])].adress), poss)


if __name__=='__main__':
  bus = smbus.SMBus(1)
  driver = PCA9685(bus, 0x40, debug=True)
  driver.setPWMFreq(50)
  if len(sys.argv) == 3:
  	moveAcc(sys.argv[1], sys.argv[2])
  else:
  	print("Please follow this instructions to analyce the performance of your servos: ")
  	print(" ")
  	print("1) Run: /$ python motor_tester.py <motor_id> <angle> ")
  	print("For LoCoQuad Robot, motor_id = 0 - 7 /// angle = 0 - 180")
  	print("WARNING: Some joints have restricted movement due to mechanical construction")
  	print(" ")
  	print("2) Place your Robot on top of a box in order to give free range of motion to all the joints")
  	print(" ")
  	print("3) Start with central position (angle = 90) for each servo")
  	print(" ")
  	print("4) One by one increse/decrese by 10 the angle value till you reach the limits or a mechanical impediment")
  	print(" ")
  	print("5) Now you have reference of the range of motion of each servo, now, one by one, command the servos to place themselves into the lowes angle and then command them to go to their highest angle value")
  	print(" ")
  	print("6) Check for inconsistences or error")