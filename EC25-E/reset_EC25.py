from gpiozero import LED
from time import sleep

resetPin = LED(26)

resetPin.on()
sleep(0.5)
resetPin.off()