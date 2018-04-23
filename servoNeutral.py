import RPi.GPIO as GPIO
import time

def setGripClose():
	farServo=GPIO.PWM(15,50)
	p=GPIO.PWM(3,50)
	farServo.start(12.5)
	p.start(7.5)
def setGripOpen():
	farServo=GPIO.PWM(15,50)
	p=GPIO.PWM(3,50)
	farServo.start(2.5)
	p.start(7.5)
	
#GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)
#GPIO.setup(15,GPIO.OUT)
#setGripClose()
#time.sleep(3)
#setGripOpen()
pwm=GPIO.PWM(3,50)
pwm.start(2.5)
def otherStuff():
	time.sleep(10)
	print("DONE")
def SetAngle(angle):
	duty=angle/18+2
	GPIO.output(03,True)
	pwm.ChangeDutyCycle(duty)
	otherStuff()
	#time.sleep(10)
	GPIO.output(03,False)
	#pwm.ChangeDutyCycle(0)
SetAngle(90)
pwm.stop()
GPIO.cleanup()


