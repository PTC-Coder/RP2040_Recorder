import machine
import time
import utime
import sdcard
import uos
import math
import random
import time, array, uctypes, rp_devices as devs
import gc

global fileCount

fileCount = 0

def enum(**enums: int):
    return type('Enum', (), enums)

Channel = enum(MONO=1, STEREO=2)

AUDIO_BUFFER_SIZE = const(48000)  #number of samples

# ======= AUDIO CONFIGURATION =======
WAV_FILE = "RP2040_Recorder_" + str(fileCount) + ".wav"
RECORD_TIME_IN_SECONDS = 10
WAV_SAMPLE_SIZE_IN_BITS = 16
FORMAT = Channel.MONO
SAMPLE_RATE_IN_HZ = 16000

SD_SPI_PORT = 0
SD_SPI_SCK_PIN = 18
SD_SPI_MOSI_PIN = 19
SD_SPI_MISO_PIN = 16
SD_SPI_CS_PIN = 17
SD_SPI_BAUD_RATE = 40000000

   
def create_wav_header(sampleRate, bitsPerSample, num_channels, num_samples):
    datasize = num_samples * num_channels * bitsPerSample // 8
    o = bytes("RIFF", "ascii")  # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(
        4, "little"
    )  # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE", "ascii")  # (4byte) File type
    o += bytes("fmt ", "ascii")  # (4byte) Format Chunk Marker
    o += (16).to_bytes(4, "little")  # (4byte) Length of above format data
    o += (1).to_bytes(2, "little")  # (2byte) Format type (1 - PCM)
    o += (num_channels).to_bytes(2, "little")  # (2byte)
    o += (sampleRate).to_bytes(4, "little")  # (4byte)
    o += (sampleRate * num_channels * bitsPerSample // 8).to_bytes(4, "little")  # (4byte)
    o += (num_channels * bitsPerSample // 8).to_bytes(2, "little")  # (2byte)
    o += (bitsPerSample).to_bytes(2, "little")  # (2byte)
    o += bytes("data", "ascii")  # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4, "little")  # (4byte) Data size in bytes
    return o

@micropython.viper   
def process_buff(buffer):
#     count = 0
#     #vals = []
#     for sample in buffer:
#         # subtract half of 16-bit to center the signal at 0
#         buffer[count] = sample - 4096  #round((sample + 1200) / 4096 * 256)
#         count += 1
    bufferPt = ptr16(uctypes.addressof(buffer))
    for n in range(int(len(buffer))):
        bufferPt[n] = ((bufferPt[n] - 0x0800))    

#======================== LED and Push Button =======================
#Pico default LED
green_led = machine.Pin(25, machine.Pin.OUT)

red_led = machine.Pin(11, machine.Pin.OUT)
red_btn = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP)

red_last = time.ticks_ms()
red_state = False

def button_handler(pin):
    global red_last, red_btn, red_state
      
    if pin is red_btn:
        #debouncing by checking if last interrupt was more than 150 ms
        if time.ticks_diff(time.ticks_ms(), red_last) > 250:
            #red_led.toggle()
            print("Allocating Memory.  Please wait ...")
            red_led.value(1)
            red_state = True
            red_last = time.ticks_ms()

red_led.value(0)  #turn LED off
red_btn.irq(trigger = machine.Pin.IRQ_FALLING, handler = button_handler)

def blink_redLED(times):
    for i in range(times):
        red_led.value(1)
        time.sleep_ms(250)
        red_led.value(0)
        time.sleep_ms(250)
        red_led.value(1)

# ===================================================================

#============================ ADC & DMA Setup ============================
ADC_CHAN = 0
ADC_PIN  = 26 + ADC_CHAN

adc = devs.ADC_DEVICE
pin = devs.GPIO_PINS[ADC_PIN]
pad = devs.PAD_PINS[ADC_PIN]
pin.GPIO_CTRL_REG = devs.GPIO_FUNC_NULL
pad.PAD_REG = 0

adc.CS_REG = adc.FCS_REG = 0
adc.CS.EN = 1
adc.CS.AINSEL = ADC_CHAN

DMA_CH0 = 0
DMA_CH1 = 1

NSAMPLES = AUDIO_BUFFER_SIZE   #24000 max
RATE = SAMPLE_RATE_IN_HZ
dma_chan0 = devs.DMA_CHANS[DMA_CH0]
dma0 = devs.DMA_DEVICE

# dma_chan1 = devs.DMA_CHANS[DMA_CH1]
# dma1 = devs.DMA_DEVICE
actual_samples = NSAMPLES * WAV_SAMPLE_SIZE_IN_BITS // 8

# ===========================================================
# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(17, machine.Pin.OUT)


while True:
    if red_state:
        red_state = False        
        
        gc.enable()
        
        adc.FCS.EN = adc.FCS.DREQ_EN = 1
        
        adc_buff0 = array.array('H', (0 for _ in range(actual_samples)))
        #adc_buff0 = bytearray(actual_samples)
        adc_buff0_mv = memoryview(adc_buff0)

        blink_redLED(2)
        
        print("Initializing SPI0 ... ")
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
        
        print("Communicating with SD Card ...")        
        sd=sdcard.SDCard(spi, cs)
        # Mount filesystem, FAT32
        vfs = uos.VfsFat(sd)
        print("Mounting SD Card")
        uos.mount(vfs, "/sd")

        format_to_channels = {Channel.MONO: 1, Channel.STEREO: 2}
        NUM_CHANNELS = format_to_channels[FORMAT]
        WAV_SAMPLE_SIZE_IN_BYTES = WAV_SAMPLE_SIZE_IN_BITS // 8
        RECORDING_SIZE_IN_BYTES = (
            RECORD_TIME_IN_SECONDS * SAMPLE_RATE_IN_HZ * WAV_SAMPLE_SIZE_IN_BYTES * NUM_CHANNELS
        )
        
        print("Creating WAV File Header ...")
        
        with open("/sd/{}".format(WAV_FILE), "wb") as wav: #write in bytes
            wav_header = create_wav_header(
                SAMPLE_RATE_IN_HZ,
                WAV_SAMPLE_SIZE_IN_BITS,
                NUM_CHANNELS,
                SAMPLE_RATE_IN_HZ * RECORD_TIME_IN_SECONDS,
            )
            num_bytes_written = wav.write(wav_header)        
        num_sample_bytes_written_to_wav = 0
        
        print("closing header write")
        wav.close

        print("Sample Rate (kHz): " + str(SAMPLE_RATE_IN_HZ//1000) + ", Total Time (s): " + str(RECORD_TIME_IN_SECONDS))
        print("Recording size: {} Bytes".format(RECORDING_SIZE_IN_BYTES))
        print("==========  START RECORDING ==========")
               
        green_led.value(1) 
        try:
            
            #=================== Configure ADC and DMA Triggers ============
            #Section 4.9 RP2040 datasheet - set integer part of the clock and
            #ignore the fractional part ( <<8  is used for that)
            adc.DIV_REG = (48000000 // RATE - 1) << 8
            adc.FCS.THRESH = adc.FCS.OVER = adc.FCS.UNDER = 1

            dma_chan0.READ_ADDR_REG = devs.ADC_FIFO_ADDR
            dma_chan0.WRITE_ADDR_REG = uctypes.addressof(adc_buff0_mv)
            dma_chan0.TRANS_COUNT_REG = NSAMPLES * WAV_SAMPLE_SIZE_IN_BITS // 8

            dma_chan0.CTRL_TRIG_REG = 0
            dma_chan0.CTRL_TRIG.CHAIN_TO = DMA_CH0
            dma_chan0.CTRL_TRIG.INCR_WRITE = dma_chan0.CTRL_TRIG.IRQ_QUIET = 1
            dma_chan0.CTRL_TRIG.TREQ_SEL = devs.DREQ_ADC
            #Data size. 0=byte, 1=halfword, 2=word
            dma_chan0.CTRL_TRIG.DATA_SIZE = 1   
            dma_chan0.CTRL_TRIG.EN = 1
           
            
            try:
                    
                #Clear down ADC FIFO so no data mixing
                while adc.FCS.LEVEL:
                    x = adc.FIFO_REG

                adc.CS.START_MANY = 1
                
                while num_sample_bytes_written_to_wav < RECORDING_SIZE_IN_BYTES:
                    
                    #print("Byte written: " + str(num_sample_bytes_written_to_wav) + "/" + str(RECORDING_SIZE_IN_BYTES))

                    
                    if(not dma_chan0.CTRL_TRIG.BUSY):
                        adc.CS.START_MANY = 0
                        dma_chan0.CTRL_TRIG.EN = 0
                        # Each sample is a 16-bit value or 2 bytes
                        num_bytes_read_from_mic = NSAMPLES * WAV_SAMPLE_SIZE_IN_BITS
#                         if num_bytes_read_from_mic > 0:
# #                             num_bytes_to_write = min(
# #                                 num_bytes_read_from_mic, RECORDING_SIZE_IN_BYTES - num_sample_bytes_written_to_wav
# #                             )
                        num_bytes_to_write = num_bytes_read_from_mic 
                        process_buff(adc_buff0_mv)

                        # write samples to WAV file
                        with open("/sd/{}".format(WAV_FILE), "ab") as wav:
                            num_bytes_written = wav.write(adc_buff0_mv[:num_bytes_to_write])
                        
                        print("Writing from buff0: " + str(num_bytes_written) + " bytes")
                        
                        num_sample_bytes_written_to_wav += num_bytes_written
                        
                        print("Total Byte written: " + str(num_sample_bytes_written_to_wav) + "/" + str(RECORDING_SIZE_IN_BYTES))
                        
                        
#                         dma_chan0.READ_ADDR_REG = devs.ADC_FIFO_ADDR
#                         dma_chan0.WRITE_ADDR_REG = uctypes.addressof(adc_buff0_mv)

                        dma_chan0.READ_ADDR_REG = devs.ADC_FIFO_ADDR
                        dma_chan0.WRITE_ADDR_REG = uctypes.addressof(adc_buff0_mv)
                        dma_chan0.TRANS_COUNT_REG = NSAMPLES * WAV_SAMPLE_SIZE_IN_BITS // 8

                        dma_chan0.CTRL_TRIG_REG = 0
                        dma_chan0.CTRL_TRIG.CHAIN_TO = DMA_CH0
                        dma_chan0.CTRL_TRIG.INCR_WRITE = dma_chan0.CTRL_TRIG.IRQ_QUIET = 1
                        dma_chan0.CTRL_TRIG.TREQ_SEL = devs.DREQ_ADC
                        #Data size. 0=byte, 1=halfword, 2=word
                        dma_chan0.CTRL_TRIG.DATA_SIZE = 1  
                        dma_chan0.CTRL_TRIG.EN = 1
                                    
#                         dma_chan0.CTRL_TRIG.EN = 1
                        adc.CS.START_MANY = 1
                       
                    #print("Next Buffer: (" + str(nextBuffer) + "), waiting for trigger: DMA0 Busy: [" + str(dma_chan0.CTRL_TRIG.BUSY) + "]" + ", DMA1 Busy: [" + str(dma_chan1.CTRL_TRIG.BUSY) + "]")

            except (KeyboardInterrupt, Exception) as e:
                print("Exception {} {}".format(type(e).__name__, e))
                               

            adc.CS.START_MANY = 0
            dma_chan0.CTRL_TRIG.EN = 0
            
            #wav.write(buffer_mv)
            
            print("==========  DONE RECORDING ==========")

        except (KeyboardInterrupt, Exception) as e:
            print("caught exception {} {}".format(type(e).__name__, e))

                
        green_led.value(0)
        red_led.value(0)
                
        
        print("Unmounting SD Card ...")
        uos.umount("/sd")
        
        print("Freeing up memory ...")
        del adc_buff0_mv
        del adc_buff0
        
        del vfs
        del sd
        
        gc.mem_free()
        gc.collect()
        gc.disable()
        print("Done")
    else:
        time.sleep_ms(250)






