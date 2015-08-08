import RPi.GPIO as GPIO
#import RPI_stub as GPIO
import TosMsg
import utils

class GpioPins():

    def setup_output(self, channels):
        """Setup output channels. Initial value is Low
        
        Keyword arguments:
        channels -- output channels list, their order must match the GPIO pin pairs on the circult board
        """   
        for channel in channels:
            GPIO.setup(channel, GPIO.OUT, initial=GPIO.LOW)
    def setup_input(self, channels):
        """Setup input channel.
        
        Keyword arguments:
        channels -- input channel list, their order must match the GPIO pin pairs on the circult board
        """
        if not isinstance(channels, list):
            raise TypeError('Channels should be list type')
        
        for channel in channels:
            GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        self.input_channels = channels
          
    def get_reply(self, send_msg):
        
        reply_msg = ""
        for char in send_msg:
            # Step 1. SendMessage 
            output_values = utils.char_to_bin(char)
            print "Send message {0}".format(output_values)
            for channel, value in zip(self.output_channels, output_values):
                GPIO.output(channel, value)
                
            # Step 2. Set Terminal Status to MSG_SENT
            GPIO.output(self.terminal_status_channel, TosMsg.MSG_SENT)
            
            # Step 3. Check until Tos got msg (Tos Status == MSG_RECEIVED)
            while GPIO.input(self.tos_status_channel) != TosMsg.MSG_RECEIVED:
                continue
            
            # Step 4. Set Terminal Status to MSG_CLEAR
            GPIO.output(self.terminal_status_channel, TosMsg.MSG_CLEAR)
            
            # Step 5. Check until Tos echo msg (Tos Status == MSG_REPLIED)
            while GPIO.input(self.tos_status_channel) != TosMsg.MSG_REPLIED:
                continue
            
            # Step 6. Got reply message and return 
            """Get value from input channels"""
            reply_bin = [GPIO.input(channel) for channel in self.input_channels]
            reply_msg += utils.bin_to_char(reply_bin)
        return reply_msg
             
        '''
        # Step 1. SendMessage 
        output_list = [int(value) for value in "{0:0=2b}".format(ord(send_msg[0]) % 4)]
        for channel, value in zip(self.output_channels, output_list):
            print "Send message {0} to pin {1}".format(value, channel)
            GPIO.output(channel, value)
            
        # Step 2. Set Terminal Status to MSG_SENT
        print "Send {0} to pin {1}".format(TosMsg.MSG_SENT, self.terminal_status_channel)
        GPIO.output(self.terminal_status_channel, TosMsg.MSG_SENT)
        
        # Step 3. Check until Tos got msg (Tos Status == MSG_RECEIVED)
        print "Pin {1} value is {0}".format(GPIO.input(self.tos_status_channel), self.tos_status_channel)
        while GPIO.input(self.tos_status_channel) != TosMsg.MSG_RECEIVED:
            continue
        
        # Step 4. Set Terminal Status to MSG_CLEAR
        GPIO.output(self.terminal_status_channel, TosMsg.MSG_CLEAR)
        
        # Step 5. Check until Tos echo msg (Tos Status == MSG_REPLIED)
        while GPIO.input(self.tos_status_channel) != TosMsg.MSG_REPLIED:
            continue
        
        # Step 6. Got reply message and return 
        """Get value from input channels"""
        return [str(GPIO.input(channel)) for channel in self.input_channels]
	'''
        
        
    def __init__(self, input_channels=None, output_channels=None, terminal_status_channel=None, tos_status_channel=None):
        GPIO.setmode(GPIO.BCM)
        self.setup_input(input_channels+[tos_status_channel])
        self.setup_output(output_channels+[terminal_status_channel])
        self.input_channels = input_channels
        self.output_channels = output_channels
        self.terminal_status_channel = terminal_status_channel
        self.tos_status_channel = tos_status_channel
        
    def cleanup(self):
        GPIO.cleanup()
