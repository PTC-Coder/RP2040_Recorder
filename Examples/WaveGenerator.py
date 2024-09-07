#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      ptcha
#
# Created:     02/09/2024
# Copyright:   (c) ptcha 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import math
import matplotlib.pyplot as plt




SAMPLE_RATE = 16000

def sound_wave(frequency, num_seconds, volume, bit):
    num_samples = int(SAMPLE_RATE * num_seconds)
    for k in range(num_samples):

        samples = volume * math.sin(2 * math.pi * k * frequency / SAMPLE_RATE)
        yield round((samples + 1) / 2 * (2 ** bit))


def main():
    data = sound_wave(261.63, 0.2, 0.5, 8)
    ys = []


    for sample in data:
        ys.append(sample)

    print("sample_count: " + str(round(0.2 * SAMPLE_RATE)))

    xs = [x for x in range(len(ys))]

    plt.plot(xs, ys)
    plt.show()
    # Make sure to close the plt object once done
    plt.close()

if __name__ == '__main__':
    main()
