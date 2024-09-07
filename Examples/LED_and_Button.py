import machine
import time
import utime

#Pico default LED
green_led = machine.Pin(25, machine.Pin.OUT)

red_led = machine.Pin(11, machine.Pin.OUT)
red_btn = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP)

#blue_led = machine.Pin(7, machine.Pin.OUT)
#blue_btn = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_UP)

red_last = time.ticks_ms()
#blue_last = time.ticks_ms()

red_state = False

def button_handler(pin):
    global red_last, red_btn, red_state
    #global blue_last, blue_btn
      
    if pin is red_btn:
        #debouncing by checking if last interrupt was more than 150 ms
        if time.ticks_diff(time.ticks_ms(), red_last) > 500:
            #red_led.toggle()
            red_state = True
            red_last = time.ticks_ms()
#     elif pin is blue_btn:
#         if time.ticks_diff(time.ticks_ms(), blue_last) > 500:
#             blue_led.toggle()
#             blue_last = time.ticks_ms()

red_led.value(0)  #turn LED off
red_btn.irq(trigger = machine.Pin.IRQ_FALLING, handler = button_handler)
# blue_led.value(0)
# blue_btn.irq(trigger = machine.Pin.IRQ_RISING, handler = button_handler)

#State Machine
while True:
    if red_state:
        red_state = False
        for i in range(5):
            red_led.value(1)
            time.sleep_ms(250)
            red_led.value(0)
            time.sleep_ms(250)
            print("loop #: " + str(i+1))
    #machine.lightsleep(1000)
