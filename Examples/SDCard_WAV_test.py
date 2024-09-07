import machine
import sdcard
import uos
import math
import random

def enum(**enums: int):
    return type('Enum', (), enums)

Channel = enum(MONO=1, STEREO=2)

#AUDIO_BUFFER_SIZE = 5000

# ======= AUDIO CONFIGURATION =======
WAV_FILE = "test.wav"
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

def sound_wave(frequency, buffer_size, volume, bit):
    #num_samples = int(SAMPLE_RATE * num_seconds)
    for k in range(buffer_size):
        samples = volume * math.sin(2 * math.pi * k * frequency / SAMPLE_RATE_IN_HZ)
        yield round((samples + 1) / 2 * (2 ** bit))
        
def audio_readinto(buffer):
        
    note = random.randint(1, 12)
    vol = random.randint(4,8) / 10
    note_str = ""
    
    if note == 1:
        freq = 261.63
        note_str = "C"
    elif note == 2:
        freq = 277.18
        note_str = "C#"
    elif note == 3:
        freq = 293.66
        note_str = "D"
    elif note == 4:
        freq = 311.13
        note_str = "Eb"
    elif note == 5:
        freq = 329.63
        note_str = "E"
    elif note == 6:
        freq = 349.23
        note_str = "F"
    elif note == 7:
        freq = 369.99
        note_str = "F#"
    elif note == 8:
        freq = 392.00
        note_str = "G"
    elif note == 9:
        freq = 415.30
        note_str = "Ab"
    elif note == 10:
        freq = 440.00
        note_str = "A"
    elif note == 11:
        freq = 466.16
        note_str = "Bb"
    elif note == 12:
        freq = 493.88
        note_str = "B"
    else:
        freq = 261.63     
    
    print(note_str)
    data = sound_wave(freq, AUDIO_BUFFER_SIZE, vol, WAV_SAMPLE_SIZE_IN_BITS)
    count = 0
    for sample in data:
        buffer[count] = sample
        count += 1
    return count


random.seed()

#Pico default LED
green_led = machine.Pin(25, machine.Pin.OUT)
green_led.value(0) 

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

wav = open("/sd/{}".format(WAV_FILE), "wb")  #write in bytes
wav_header = create_wav_header(
    SAMPLE_RATE_IN_HZ,
    WAV_SAMPLE_SIZE_IN_BITS,
    NUM_CHANNELS,
    SAMPLE_RATE_IN_HZ * RECORD_TIME_IN_SECONDS,
)
num_bytes_written = wav.write(wav_header)


# allocate sample arrays
# memoryview used to reduce heap allocation in while loop
AUDIO_BUFFER_SIZE = random.randint(20000, 50000)

mic_samples = bytearray(AUDIO_BUFFER_SIZE)
mic_samples_mv = memoryview(mic_samples)


num_sample_bytes_written_to_wav = 0

print("Recording size: {} bytes".format(RECORDING_SIZE_IN_BYTES))
print("==========  START RECORDING ==========")
green_led.value(1) 
try:
    while num_sample_bytes_written_to_wav < RECORDING_SIZE_IN_BYTES:
        # read a block of samples from the I2S microphone
        #num_bytes_read_from_mic = audio_in.readinto(mic_samples_mv)
        num_bytes_read_from_mic = audio_readinto(mic_samples_mv) // 8
        if num_bytes_read_from_mic > 0:
            num_bytes_to_write = min(
                num_bytes_read_from_mic, RECORDING_SIZE_IN_BYTES - num_sample_bytes_written_to_wav
            )
            # write samples to WAV file
            num_bytes_written = wav.write(mic_samples_mv[:num_bytes_to_write])
            num_sample_bytes_written_to_wav += num_bytes_written

    print("==========  DONE RECORDING ==========")
except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))

green_led.value(0) 
# cleanup
wav.close()
uos.umount("/sd")

print("Done")
