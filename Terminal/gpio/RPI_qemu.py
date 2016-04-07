import random
import sys
import struct
import socket
import threading
import traceback
import time

SOCKET_PORT = 8989
#size = 160
GPIO_SET_OFFSET = 28
GPIO_CLR_OFFSET = 40
GPIO_GPLEV_OFFSET = 52
#gpio_socket = None

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

def setmode(mode_name):
    print "Set mode to {0}".format(mode_name)

def setup_socket():
    gpio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gpio_socket.connect(("127.0.0.1", SOCKET_PORT))
    return gpio_socket
    
def setup(channel, in_out, initial=None, pull_up_down=1):
    #global gpio_socket
    print "Set channel {0} to {1}, initial={2}".format(channel, in_out, initial)
    #if gpio_socket == None:

def input(channel, pull_up_down=1):
    #global gpio_socket
    gpio_socket = setup_socket()
    if (channel > 53) or (channel < 0):
        print "Error! Channel %d out of range!".format(channel)
    
    '''
    if channel == 15:
        # Do not use pulling here.
        gpio_socket.send("TOS_WRITE#R")
        # Server will reply till TOS_WRITER == 1
        value = int(gpio_socket.recv(255))
        return 1
    else:
    '''
    msg = ""
    if 0 <= channel < 32:
        msg += "GPLEV0#R" 
        #value = int(GPLEV0[31-channel])
    elif 32 <= channel < 54:
        msg += "GPLEV1#R"
        #value = int(GPLEV1[63-channel])
    gpio_socket.send(msg)
    value = int(gpio_socket.recv(255))
    gpio_socket.close()
    if (value & (1 << channel % 32)) > 0:
        return 1
    else:
        return 0

def output(channel, value):
    #global gpio_socket
    gpio_socket = setup_socket()
    if (channel > 53) or (channel < 0):
        print "Error! Channel%d out of range!".format(channel)

    if (value != 0) and (value != 1):
        print "Error! Value %d must be 0 or 1!".format(value)

    #thread_lock.acquire()
    msg = ""
    bit_value = 1 << (channel%32) 
    if 0 <= channel < 32:
        if value == 0:
            msg += "GPCLR0#W#{0}".format(bit_value)
        else:
            msg += "GPSET0#W#{0}".format(bit_value) 
        #GPLEV0[31-channel] = str(value)
    elif 32 <= channel < 54:
        if value == 0:
            msg += "GPCLR1#W#{0}".format(bit_value)
        else:
            msg += "GPSET1#W#{0}".format(bit_value)
        #GPLEV1[63-channel] = str(value)
    #thread_lock.release()

    gpio_socket.send(msg)
    response = str(gpio_socket.recv(255))
    gpio_socket.close()
    if response != "OK":
        print "Warnning! Unknown response"
    return  
    # IF channel is 15 notify waiting thread

def cleanup():
    print "Clean GPIO Setting!"
