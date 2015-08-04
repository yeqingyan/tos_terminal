import random

BCM = "BCM"
IN = "IN"
OUT = "OUT"
LOW = 0
HIGH = 1

def hello():
    print "Alan! Hello World!"
    
def setmode(mode_name):
    print "Set mode to {0}".format(mode_name)

def setup(channel, in_out, initial=None):
    print "Set channel {0} to {1}, initial={2}".format(channel, in_out, initial)

def input(channel):
    return random.randint(0,1)

def output(channel, value):
    print "Channel {0} set to {1}".format(channel, value)
    
def cleanup():
    print "Clean GPIO Setting!"