import machine
import sdcard
import uos

#import wave
 
#Initialize the onboard LED as output
led = machine.Pin(25,machine.Pin.OUT)

# Toggle LED functionality
def BlinkLED(timer_one):
    led.toggle()

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(17, machine.Pin.OUT)

# Initialize the SD card
spi=machine.SPI(0,
        baudrate=40000000,
        polarity=0,
        phase=0,
        bits=8,
        firstbit=machine.SPI.MSB,
        sck=machine.Pin(18),
        mosi=machine.Pin(19),
        miso=machine.Pin(16))

sd=sdcard.SDCard(spi, cs)

# Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

# Create a file and write something to it
print("Writing to SD ...\n")
with open("/sd/test01.txt", "w") as file:
    file.write("Hello, SD World!\r\n")
    file.write("This is a test\r\n")

print("Reading from SD ...\n")
# Open the file we just created and read from it
with open("/sd/test01.txt", "r") as file:
    data = file.read()
    print(data)