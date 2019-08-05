## change frequency for changing the output and fixed pwm value.
import i2cdev
import numpy
import time

pwm=i2cdev.I2C(0x40,1)

# Reset PWM
pwm.write(bytes([0xFA, 0]))     # zero all pin
pwm.write(bytes([0xFB, 0]))     # zero all pin
pwm.write(bytes([0xFC, 0]))     # zero all pin
pwm.write(bytes([0xFD, 0]))     # zero all pin
pwm.write(bytes([0x01, 0x04]))  # The 16 LEDn outputs are configured with a totem pole structure.
pwm.write(bytes([0x00, 0x01]))  #PCA9685 responds to LED All Call I2C-bus address
time.sleep(0.01)  # wait for oscillator

'''
Set the PWM frequency to the provided value in hertz.
The maximum PWM frequency is 1526 Hz if the PRE_SCALE register is set "0x03h".
The minimum PWM frequency is 24 Hz if the PRE_SCALE register is set "0xFFh".
he PRE_SCALE register can only be set when the SLEEP bit of MODE1 register is set to logic 1.
'''

freq_hz=100 # change frequency for changing the output and fixed pwm value.
freq_hz=freq_hz*0.9 #correction
prescale = int(numpy.floor(25000000.0/(4096.0*float(freq_hz))-1))    # datasheet equation
print("prescale = " , prescale )
pwm.write(bytes([0x00, 0x10]))
time.sleep(0.01)
pwm.write(bytes([0xFE, prescale]))
pwm.write(bytes([0x00, 0x80]))
time.sleep(0.01)
pwm.write(bytes([0x00, 0x00]))
time.sleep(0.01)
pwm.write(bytes([0x01, 0x04]))
time.sleep(0.01)

def set_pwm(channel, value):
  x=min(4095,value)
  x=max(0,x)
  """Sets a single PWM channel."""
  LED0_ON_L          = 0x06
  LED0_ON_H          = 0x07
  LED0_OFF_L         = 0x08
  LED0_OFF_H         = 0x09
  pwm.write(bytes([(LED0_ON_L+4*channel), 0]))
  pwm.write(bytes([(LED0_ON_H+4*channel), 0]))
  pwm.write(bytes([(LED0_OFF_L+4*channel), (x & 0xFF)]))
  pwm.write(bytes([(LED0_OFF_H+4*channel), (x >> 8)]))
  time.sleep(0.1)
'''
print('test')
i=0
for i in range (0,4095,50):
	set_pwm(0, i)
	print(i)'''

set_pwm(0,2500)
time.sleep(3)
set_pwm(0,0)
'''for i in range (4095,0,-25):
	set_pwm(1, i)
	print(i)'''

print('finished')
