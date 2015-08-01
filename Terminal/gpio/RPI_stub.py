import random

BCM = "BCM"
IN = "IN"
OUT = "OUT"

def hello():
    print "Alan! Hello World!"
    
def setmode(mode_name):
    print "Set mode to {0}".format(mode_name)

def setup(channel, in_out):
    print "Set channel {0} to {1}".format(channel, in_out)

def input(channel):
    return str(random.randint(0,1))