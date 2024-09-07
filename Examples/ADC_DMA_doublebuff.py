# Pico MicroPython: ADC test code
# See https://iosoft.blog/pico-adc-dma for description
#
# Copyright (c) 2021 Jeremy P Bentham
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import time, array, uctypes, rp_devices as devs

# Fetch single ADC sample
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
# adc.CS.START_ONCE = 1
# print(adc.RESULT_REG)

# Multiple ADC samples using DMA
DMA_CH0 = 0
DMA_CH1 = 1

NSAMPLES = const(500)
RATE = 16000
dma_chan0 = devs.DMA_CHANS[DMA_CH0]
dma0 = devs.DMA_DEVICE

dma_chan1 = devs.DMA_CHANS[DMA_CH1]
dma1 = devs.DMA_DEVICE

adc.FCS.EN = adc.FCS.DREQ_EN = 1
adc_buff0 = array.array('H', (0 for _ in range(NSAMPLES)))
adc_buff1 = array.array('H', (0 for _ in range(NSAMPLES)))

def process_buffer(adc_buffer):
    vals = []
    for val in adc_buffer:
    #vals = [("%1.3f" % (val*3.3/4096)) for val in adc_buffer]
        vals.append("%1.3f" % (val))
    print(vals)
    print(str(len(adc_buffer)))

adc.DIV_REG = (48000000 // RATE - 1) << 8
adc.FCS.THRESH = adc.FCS.OVER = adc.FCS.UNDER = 1

dma_chan0.READ_ADDR_REG = devs.ADC_FIFO_ADDR
dma_chan0.WRITE_ADDR_REG = uctypes.addressof(adc_buff0)
dma_chan0.TRANS_COUNT_REG = NSAMPLES

dma_chan0.CTRL_TRIG_REG = 0
dma_chan0.CTRL_TRIG.CHAIN_TO = DMA_CH1
dma_chan0.CTRL_TRIG.INCR_WRITE = dma_chan0.CTRL_TRIG.IRQ_QUIET = 1
dma_chan0.CTRL_TRIG.TREQ_SEL = devs.DREQ_ADC
#Data size. 0=byte, 1=halfword, 2=word
dma_chan0.CTRL_TRIG.DATA_SIZE = 0
dma_chan0.CTRL_TRIG.EN = 1

dma_chan1.READ_ADDR_REG = devs.ADC_FIFO_ADDR
dma_chan1.WRITE_ADDR_REG = uctypes.addressof(adc_buff1)
dma_chan1.TRANS_COUNT_REG = NSAMPLES

dma_chan1.CTRL_TRIG_REG = 1
dma_chan1.CTRL_TRIG.CHAIN_TO = DMA_CH0
dma_chan1.CTRL_TRIG.INCR_WRITE = dma_chan1.CTRL_TRIG.IRQ_QUIET = 1
dma_chan1.CTRL_TRIG.TREQ_SEL = devs.DREQ_ADC
dma_chan1.CTRL_TRIG.DATA_SIZE = 1
dma_chan1.CTRL_TRIG.EN = 0

nextBuffer = 1
count = 50

try:
    
    #Clear down ADC FIFO so no data mixing
    while adc.FCS.LEVEL:
        x = adc.FIFO_REG

    adc.CS.START_MANY = 1
    
    while(count > 0):
        
        if(nextBuffer == 0 and not dma_chan1.CTRL_TRIG.BUSY):
            print(count)
            count -= 1
            
            process_buffer(adc_buff1)
            
            dma_chan1.READ_ADDR_REG = devs.ADC_FIFO_ADDR
            dma_chan1.WRITE_ADDR_REG = uctypes.addressof(adc_buff1)
            
            dma_chan0.CTRL_TRIG.EN = 1
            dma_chan1.CTRL_TRIG.EN = 0            
            
            nextBuffer = 1
                                   
            
        
        if(nextBuffer == 1 and not dma_chan0.CTRL_TRIG.BUSY):
            print(count)
            count -= 1
            
            process_buffer(adc_buff0)
            
            dma_chan0.READ_ADDR_REG = devs.ADC_FIFO_ADDR
            dma_chan0.WRITE_ADDR_REG = uctypes.addressof(adc_buff0)
            
            dma_chan0.CTRL_TRIG.EN = 0
            dma_chan1.CTRL_TRIG.EN = 1

            
            nextBuffer = 0

    adc.CS.START_MANY = 0
    dma_chan0.CTRL_TRIG.EN = 0
    dma_chan1.CTRL_TRIG.EN = 0


except (KeyboardInterrupt, Exception) as e:
    print("Exception {} {}".format(type(e).__name__, e))


# EOF

