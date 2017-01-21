from gpio_96boards import GPIO


recbut = GPIO.gpio_id('GPIO_I') # GPIO_35, pin = 31
actbut = GPIO.gpio_id('GPIO_E') # GPIO_115, pin = 27
recled = GPIO.gpio_id('GPIO_L') # GPIO_33, pin = 34
actled = GPIO.gpio_id('GPIO_J') # GPIO_34, pin = 32
actbutstate = False
actledstate = False
pins = (
	(recbut, 'in'),
	(actbut, 'in'),
	(recled, 'out'),
	(actled, 'out')
)


def record(GPIO):
	if __name__ == '__main__':
		recbut = gpio.digital_read(recbut)
		while recbut == True:
			gpio.digital_write(recled, GPIO.HIGH)
			# code for recording sound
			gpio.digital_write(recled, GPIO.LOW)


def activate(GPIO):
	if __name__ == '__main__':
		actbut = gpio.digital_read(recbut)
		if actbut == True & actbutstate == False:
			if actledstate == True:
				actledstate = False
				gpio.digital_write(actled, GPIO.LOW)
				# Turn off microphone
			else:
				actledstate = True
				gpio.digital_write(actled, GPIO.HIGH)
				# Turn on microphone
		actbutstate = actbut