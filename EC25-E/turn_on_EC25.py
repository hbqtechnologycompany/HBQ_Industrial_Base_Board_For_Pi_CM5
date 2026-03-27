from gpiozero import LED
from time import sleep

TurnOn_Pin = LED(27)

TurnOn_Pin.on()
sleep(0.5)
TurnOn_Pin.off()