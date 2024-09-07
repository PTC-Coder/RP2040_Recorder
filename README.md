# RP2040_Recorder
A simple mono channel recorder using an RP2040 Pico connected to an electret mic with pre-amp.  The recorder can write the audio to a FAT32 formatted SD Card at 16kHz sampling
![alt text](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/Breadboard.png?raw=true)

## Components:
* QTY 1 [RP2040 Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/)
* QTY 1 [Electret Microphone Amplifier Module MAX4466 Adjustable Gain Blue Breakout Board](https://www.amazon.com/dp/B08N4FNFTR)
* QTY 1 [Full Size SD Card Reader](https://www.amazon.com/dp/B0CRDT3CGQ)
* QTY 1 [SDXC Card, At least 90 MB/s transfer](https://www.bhphotovideo.com/c/product/1692701-REG/sandisk_sdsdxxu_064g_ancin_64gb_extreme_pro_uhs_i.html)
* QTY 1 [2-pin Tact Push Button Switch N.O.](https://www.amazon.com/dp/B07WF76VHT)
* QTY 1 LED
* QTY 1 1k-Ohm Resistor
* QTY 1 150-Ohm Resistor
* QTY 1 [Breadboard](https://www.amazon.com/dp/B0B1XFQDQY)
* QTY 1 [Breadboard Jumper Kit](https://www.amazon.com/dp/B08YRGVYPV)
* QTY 1 [Micro-USB to USB-A power+data cable](https://www.amazon.com/Amazon-Basics-Charging-Transfer-Gold-Plated/dp/B0711PVX6Z)

## RP2040 Pico Setup
1. Hold down the push button on the RP2040 Pico and plug it into a computer via the micro USB connector. Make sure that you have a power + data cable since many micro USB cables are power only.  Let go of the push button after a drive (RPI-RP2) is mounted on your system.  Drag and drop a RP2040 Pico Micropython Firmware (*.uf2) obtained either from [Micropython_FW](/Micropython_FW) folder or from the [Micropython official website under RP2040 Pico](https://micropython.org/download/RPI_PICO/)
2. RP2040 Pico will automatically close the mounted drive and reboot itself with the new Firmware.  A good thing to note if you ever run into a bricked RP2040 from coding, you can load [flash_nuke.uf2](/Micropython_FW/flash_nuke.uf2) to clear all memory of the Pico.
3. Download and install [Thonny IDE](https://thonny.org/) on your system.  Select the appropriate O/S to download.
4. Launch Thonny after completing the installation.  If your Pico is still connected to the computer, you should be able to select the BoardCDC @ COM port option in the lower right corner of the IDE to connect to the REPL on the Pico.
5. It's a good idea to show the File viewing window.  Select View -> File to check the option.  You'll need this to load codes into Pico's flash memory.
6. Load the following file from [Src](/Src) into Pico's memory:
      - main.py
      - rp_devices.py
      - sdcard.py
7. If you have everything wired up correctly, you should be able to just insert a FAT32 formatted SD card into the Card Reader and click the push button to activate recording.  Note that the LED will turn on for a few second to indicate that memory is being allocated for the recording.  The LED will flash twice and then turn solid at the same time as the Green LED on the Pico turns on.  This indicate that the recording started and it'll go for 10 seconds and all the light will turn off.  SD Card can be checked for the WAV file of the recording.  Please also note that the Pico has to be power cycled to do another recording.  There's some additional work to be done to allow multiple recordings without power cycling.
8. This recorder doesn't have the greatest audio quality due to using the built-in 12-bit ADC on the Pico.  The recording runs at 16kHz sampling rate and this is the best that this recorder can do without doing a DMA Ping-Pong buffering technique.
9. The WAV file can be opened with the [Raven Software](https://store.birds.cornell.edu/collections/raven-sound-software) to analyze the audio.

![alt text](https://github.com/PTC-Coder/RP2040_Recorder/blob/main/Documents/spectrogram.png?raw=true)
