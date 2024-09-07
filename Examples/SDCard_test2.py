import machine
import sdcard
import uos

def enum(**enums: int):
    return type('Enum', (), enums)

Channel = enum(MONO=1, STEREO=2)

#AUDIO_BUFFER_SIZE = 5000

# ======= AUDIO CONFIGURATION =======
WAV_FILE = "testSD.wav"
RECORD_TIME_IN_SECONDS = 1
WAV_SAMPLE_SIZE_IN_BITS = 8
FORMAT = Channel.MONO
SAMPLE_RATE_IN_HZ = 16000

   
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
format_to_channels = {Channel.MONO: 1, Channel.STEREO: 2}
NUM_CHANNELS = format_to_channels[FORMAT]
WAV_SAMPLE_SIZE_IN_BYTES = WAV_SAMPLE_SIZE_IN_BITS // 8
RECORDING_SIZE_IN_BYTES = (
    RECORD_TIME_IN_SECONDS * SAMPLE_RATE_IN_HZ * WAV_SAMPLE_SIZE_IN_BYTES * NUM_CHANNELS
)
# Create a file and write something to it
print("Writing to SD ...\n")
wav = open("/sd/{}".format(WAV_FILE), "wb")  #write in bytes
wav_header = create_wav_header(
    SAMPLE_RATE_IN_HZ,
    WAV_SAMPLE_SIZE_IN_BITS,
    NUM_CHANNELS,
    SAMPLE_RATE_IN_HZ * RECORD_TIME_IN_SECONDS,
)
wav.write(wav_header)
wav.close()

# print("Reading from SD ...\n")
# # Open the file we just created and read from it
# with open("/sd/test01.txt", "r") as file:
#     data = file.read()
#     print(data)
