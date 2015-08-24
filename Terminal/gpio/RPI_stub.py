import random

BCM = "BCM"
IN = "IN"
OUT = "OUT"
LOW = 0
HIGH = 1
PUD_DOWN = 1
PUD_UP = 1

TERMINAL_READ_STATUS = 0
TERMINAL_WRITE_STATUS = 0
TERMINAL_READ_CHANNEL = 7
TERMINAL_WRITE_CHANNEL = 8

def hello():
    print "Alan! Hello World!"
    
def setmode(mode_name):
    print "Set mode to {0}".format(mode_name)

def setup(channel, in_out, initial=None, pull_up_down=1):
    print "Set channel {0} to {1}, initial={2}".format(channel, in_out, initial)

def input(channel, pull_up_down=1):
    if channel == TERMINAL_READ_CHANNEL:
        return TERMINAL_READ_STATUS
    elif channel == TERMINAL_WRITE_CHANNEL:
        return TERMINAL_WRITE_STATUS
    else:
        return random.randint(0,1)

def output(channel, value):
    if channel == TERMINAL_READ_CHANNEL:
        TERMINAL_READ_STATUS = value
    elif channel == TERMINAL_WRITE_CHANNEL:
        TERMINAL_WRITE_STATUS = value
    
    print "Channel {0} set to {1}".format(channel, value)
    
def cleanup():
    print "Clean GPIO Setting!"
