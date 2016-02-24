import random
import sysv_ipc
import sys
import struct
key = 6666
size = 160
shm = None

#memory = shm.read(size)
#print ":".join("{:02x}".format(ord(c)) for c in memory)
GPIO_SET_OFFSET = 28
GPIO_CLR_OFFSET = 40
GPIO_GPLEV_OFFSET = 52

BCM = "BCM"
IN = "IN"
OUT = "OUT"
LOW = 0
HIGH = 1
PUD_DOWN = 1
PUD_UP = 1

"""
TERMINAL_READ_STATUS = 0
TERMINAL_WRITE_STATUS = 0
TERMINAL_READ_CHANNEL = 7
TERMINAL_WRITE_CHANNEL = 8
"""

def hello():
    print "Alan! Hello World!"
    
def setmode(mode_name):
    print "Set mode to {0}".format(mode_name)

def setup(channel, in_out, initial=None, pull_up_down=1):
    global shm
    print "Set channel {0} to {1}, initial={2}".format(channel, in_out, initial)
    if shm == None:
        shm = sysv_ipc.SharedMemory(key)
        print "Setup share memory"

def input(channel, pull_up_down=1):
    global shm, GPIO_GPLEV_OFFSET
    offset = GPIO_GPLEV_OFFSET + (channel/32*4) 
    mask = 1 << (channel % 32)
    value = struct.unpack('<i', shm.read(4, offset))
    value = value[0] & mask
    if value > 0:
        return 1
    else:
        return 0        

def output(channel, value):
    global shm, GPIO_CLR_OFFSET, GPIO_SET_OFFSET, GPIO_GPLEV_OFFSET
    if (channel > 53) or (channel < 0):
        print "Error! Channel%d out of range!".format(channel)

    if (value != 0) and (value != 1):
        print "Error! Value %d must be 0 or 1!".format(value)

    offset = GPIO_GPLEV_OFFSET + channel/32*4

    bitValue = 1 << (channel%32)
    pre_value = int(struct.unpack('<i', shm.read(4, offset))[0])
    if value == 0:
        # Turn off pin
        new_value = pre_value & (~bitValue & 0xffffffff)        
    else:
        # Turn on pin
        new_value = pre_value | bitValue
        
    #print "Write {0:x} to {1:x}".format(new_value, offset)
    new_value = struct.pack("I", new_value)    
    shm.write(new_value, offset)   


def cleanup():
    print "Clean GPIO Setting!"
