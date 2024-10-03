# RP2040_Recorder
A simple mono channel recorder using an RP2040 Pico connected to an electret mic with pre-amp.  The recorder can write the audio to a FAT32 formatted SD Card at 16kHz sampling
![Pico Recorder](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/Breadboard2.png?raw=true)

![RPi2040 Recorder](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/RPi2040Recorder.png?raw=true)

## Components:
* QTY 1 [RP2040 Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/)
* QTY 1 [Electret Microphone Amplifier Module MAX4466 Adjustable Gain Blue Breakout Board](https://www.amazon.com/dp/B08N4FNFTR)
* QTY 1 [Full Size SD Card Reader](https://www.amazon.com/dp/B0CRDT3CGQ)
* QTY 1 [SDXC Card, At least 90 MB/s transfer](https://www.bhphotovideo.com/c/product/1692701-REG/sandisk_sdsdxxu_064g_ancin_64gb_extreme_pro_uhs_i.html)
* QTY 1 [2-pin Tact Push Button Switch N.O.](https://www.amazon.com/dp/B07WF76VHT)
* QTY 1 LED
* QTY 1 10k-Ohm Resistor
* QTY 1 150-Ohm Resistor
* QTY 1 [Breadboard](https://www.amazon.com/dp/B0B1XFQDQY)
* QTY 1 [Breadboard Jumper Kit](https://www.amazon.com/dp/B08YRGVYPV)
* QTY 1 [Micro-USB to USB-A power+data cable](https://www.amazon.com/Amazon-Basics-Charging-Transfer-Gold-Plated/dp/B0711PVX6Z)

## RP2040 Pico Setup
1. Clone or download the Zip file from this repository.  If you download the Zip file, extract it to a location on your computer that you can find later.

![Clone or download](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/Clone_download.png?raw=true)

2. Hold down the push button on the RP2040 Pico and plug it into a computer via the micro USB connector. Make sure that you have a power + data cable since many micro USB cables are power only.  Let go of the push button after a drive (RPI-RP2) is mounted on your system.  Drag and drop a RP2040 Pico Micropython Firmware (*.uf2) obtained either from [Micropython_FW](/Micropython_FW) folder in your cloned or extracted project directory or from the [Micropython official website under RP2040 Pico](https://micropython.org/download/RPI_PICO/)
3. RP2040 Pico will automatically close the mounted drive and reboot itself with the new Firmware.  A good thing to note if you ever run into a bricked RP2040 from coding, you can load [flash_nuke.uf2](/Micropython_FW/flash_nuke.uf2) from the same folder you found the FW to clear all memory of the Pico.
4. Download and install [Thonny IDE](https://thonny.org/) on your system.  Select the appropriate O/S to download.
5. Launch Thonny after completing the installation.  If your Pico is still connected to the computer, you should be able to select the BoardCDC @ COM port option in the lower right corner of the IDE to connect to the Read–eval–print loop (REPL) on the Pico.

![Thonny Connect](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/ConnectToThonny.png?raw=true)

6. It's a good idea to show the File viewing window.  Select View -> File to check the option.  You'll need this to load codes into Pico's flash memory.

![Thonny View Files](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/Thonny_view_file.png?raw=true)

7. Test that you now have MicroPython running via REPL on the Pico.  You can type the following code in the REPL window:
```
print("Hello Micropython!")
```
8. Load the following file from [Src](/Src) into Pico's memory:
      - rp_devices.py
      - sdcard.py
	  
9. It might be a good idea to save the source code to your computer first so you can easily find the file in the file browser we enabled in Step 5.  Make sure that your Pico is connected and you can see REPL working.  Right click on the file you want to load to the Pico and select the "Upload To /" option.  The file should appear on the Pico device after a successful upload.

![Thonny View Files](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/LoadFile.png?raw=true)

## Understanding Breadboard
1. First we need to understand how the breadboard is laid out.  We'll be working with a standard-size breadboard with power rails on the top and bottom sides of the board.  Pay attention to the label or colored lines indicating the rail polarity.  The negative rail is usually connected across the entire row from left to right.  The same is true for the positive rail. Different breadboards have different rail labels so please carefully note the labels. In the center of the breadboard, each hole in the same column is connected to each other, separated by the center gap in the middle. None of the columns are connected to each other.

![Breadboard Layout](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/Understanding_Breadboard.png?raw=true)

2. On some boards, there's a center gap between the rails with the same polarity, so you need to bridge it with a connecting wire. Our board doesn't need an extra bridging wire, but the illustration below shows the bridging wires for each power rail.

![Breadboard Jumpers](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/Breadboard_power_jumpers.png?raw=true)

## Initial Breadboard Setup
1. Place a RP2040 Pico module in the middle and at the far right edge of the board with the micro USB connector to the right.
2. Connect Power and GND from RP2040 Pico module to the power rail.  3V3 to (+) rail and GND to (-) Rail.  Typically, a Red wire should be used for (+) and a Black wire for (-).  In our case a Green wire can be used for the (-) since we are treating (-) as GND in our circuit.
3. Bridge the top positive and bottom positive rails with a connection wire.
![Breadboard Power](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/Wireup_board_power.png?raw=true)

## LED and Push Button Circuit
1. Plug the LED into the breadboard.  LED has a polarity and the one we are using is called a TO package.  Note that the longer leg is a (+) positive terminal and the shorter leg is the (-) negative terminal.  Some LEDs might have the leads clipped to equal length, but you can still determine the polarity by looking at the LED from the top view.  The flat cut side is the (-) negative terminal.

![LED Details](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/LED_details.png?raw=true)

2. Add the 150-ohm resistor to the (-) negative pin of the LED and connect it to the ground (-) rail of the breadboard.

![LED Circuit](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/LEDcircuit.png?raw=true)

3. Now add the tactile push button switch to the breadboard.  Note that there are only two pins on this version of the switch.  Connect it across the middle channel of the breadboard. Add the 10k-Ohm resistor to top pin of the switch and then connect that to the positive (+) rail of the breadboard.

![LED Switch Circuit](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/LED_pushbutton_circuit.png?raw=true)

4. Test this circuit by copying the code from [LED_and_Button.py](/Examples/LED_and_Button.py) and run the code on the Pico.  If everything is correctly connected, the LED should blink and turn off when you push the button.

![LED Test](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/LEDtest.gif?raw=true)

## Microphone Circuit
1. Add the microphone component to board.  Note that the physical component doesn't exactly match the diagram here, but you should be able to follow the pin labels.  This microphone component is an omnidirection electret condensor with a pre-amp circuit.

![SDCard Prep](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/MicrophoneCircuit.png?raw=true)

2. Wire the connections according to the shown image.  Note that VCC pin is connected to the VBUS pin (Pin 40) on the Pico to get the 5V for VCC.  This gives the mic a higher bias voltage, resulting in a better SNR.

3. You can test this circuit portion by running the [ADC_DMA_doublebuff.py](/Examples/ADC_DMA_doublebuff.py) code to continuously grab data from the microphone to the ADC and transfer them to the Direct Memory Access (DMA) channels on the Pico. This code will not work if don't have the [rp_devices.py](/Src/rp_devices.py) loaded into the Pico already.

![Mic ADC Test](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/Mictest.gif?raw=true)

## SD Card Circuit
1. Add the SD Card slot component to the breadboard.  To make wiring easier to use and troubleshoot, place the component on the top side of the breadboard and then use short jumper wires to connect it across the center slot of the breadboard.  This gives you the entire column to connect to the component pins.  The 5V pin can be skipped since we'll only use the 3V3 for power.

![SDCard Prep](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/SDCardprep.png?raw=true)

2. Connect the wires to the designated pins on the Pico pins.  Note that the diagram here doesn't match the physical component exactly, but you should be able to follow the same pin labels.  No need to connect the 5V pin.  Connect all the GND pins on the SD Card slot to the (-) rail on the breadboard.

![SDCard Connection](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/SDcard_connection.png?raw=true)

Here's the physical board layout connection for the SD Card Slot to the Pico

![SDCard SPI Connection](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/SDcard_SPI_connections.png?raw=true)
![Pico SPI Connection](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/Pico_SPI_connections.png?raw=true)

3. Test this circuit by copying the code from [SDCard_test.py](Examples/SDCard_test.py) and run the code on the Pico.  This will test the reading and writing of the SD card.  This code will not work if you don't have the [sdcard.py](/Src/sdcard.py) uploaded to the Pico already.  Before running the code, make sure you have a FAT32 formatted SD card inserted into the SD Card slot.

*** Important *** Some breadboard might have poor connections due to the poor quality of the grid lattice and you will keep on getting "OSError: timeout waiting for v2 card" even with the SD Card inserted. The clock timing and data exchanges are critical and require a solid connection. The pins might need to be soldered directly from the SD Card holder to the Pico pins.  Please let us know if you ran into this issue, and we can help solder the pins.

![Soldered Connections](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/SolderedPins.png?raw=true)

## Final Circuit
1. Load [main.py](/Src/main.py) into the Pico along with the other 2 files [rp_devices.py](/Src/rp_devices.py), [sdcard.py](/Src/sdcard.py) we uploaded earlier from the setup step.
2. Power cycle the Pico by unplugging the USB connector, wait 2 seconds, and plug it back in.  
3. Because we now have main.py in the Pico memory, it'll automatically execute the code in main.py script.  *Optional* Being able to execute from internal flash memory on the Pico allows us to run the Pico without the USB cable plugged in.  However, you do need to supply the circuit with an external battery (at least 4.5V) to the Pico SYS power pin (Pin 39) and any GND pin (Pin 38, Pin23, Pin 3)
4. If you have everything wired up correctly, you should be able to just insert a FAT32 formatted SD card into the Card Reader and click the push button to activate recording. There should be some system messages on the REPL panel indicating what's going on. Note that the LED will turn on solid for a few second to indicate that memory is being allocated for the recording.  The LED will flash twice and then turn solid at the same time as the Green LED on the Pico turns on.  This indicate that the recording started and it'll go for 10 seconds and all the light will turn off.  SD Card can be checked for the WAV file of the recording.  Please also note that the Pico has to be power cycled to do another recording.  There's some additional work to be done to allow multiple recordings without power cycling.
5. This recorder doesn't have the greatest audio quality due to using the built-in 12-bit ADC on the Pico.  The recording runs at 16kHz sampling rate and this is the best that this recorder can do without doing a DMA Ping-Pong buffering technique.  You can push the button again to start another recording.  The file name will have an automatic incrementing number to not overwrite the previous file.  If the Pico is power cycled, the file numbering with start again at 000.

![Pico Recorder](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/PicoRecorder.gif?raw=true)

6. Eject the SD Card and use a card reader on your computer to read the recorded audio files in WAV format. The WAV file can be opened with the [Raven Software](https://store.birds.cornell.edu/collections/raven-sound-software) to analyze the audio.  You can also use [Audacity](https://www.audacityteam.org/download/).

![Sample Spectrogram](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/spectrogram.png?raw=true)

7. The audio quality could be significantly improved if you use a higher quality electret element.

![Better Microphone](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/BetterElectret.png?raw=true)




