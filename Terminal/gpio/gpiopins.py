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
            # Step 1. Convert char to binary 
            output_values = utils.char_to_bin(char)
            print "Send message {0}".format(output_values)
            # Write
            for bit in output_values:
                if GPIO.input(self.terminal_write) != TosMsg.IDLE:
                    print "Error! TERMINAL_WRITE channel is not idle!"
                    return 
                
                # Wait TOS ready
                while GPIO.input(self.tos_read) != TosMsg.IDLE:
                    continue
                GPIO.output(self.output_bits, bit)
                # Update terminal status, inform TOS to receive
                GPIO.output(self.terminal_write, TosMsg.MSG_SENT)
                # Wait TOS to finish read 
                while GPIO.input(self.tos_read) == TosMsg.IDLE:
                    continue
                # Change terminal status to idle
                GPIO.output(self.terminal_write, TosMsg.IDLE)
            
            # Read  
            reply_bin = []
            for _ in xrange(8):
                if GPIO.input(self.terminal_read) != TosMsg.IDLE:
                    print "Error!, TERMINAL_READ channel is not idle!"
                    return
                # Wait Tos to write message
                while GPIO.input(self.tos_write) == TosMsg.IDLE:
                    continue
                # Construct message
                reply_bin.append(GPIO.input(self.input_bits))
                
                # Tell TOS received message
                GPIO.output(self.terminal_read, TosMsg.MSG_RECEIVED)
                while GPIO.input(self.tos_write) == TosMsg.MSG_SENT:
                    continue
                # Finish read 
                GPIO.output(self.terminal_read, TosMsg.IDLE)
            # Got reply message and return 
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
        
        
    def __init__(self, input_bits=None, output_bits=None, tos_read=None, tos_write=None, terminal_read=None, terminal_write=None):
        GPIO.setmode(GPIO.BCM)
        self.setup_input([input_bits, tos_read, tos_write])
        self.setup_output([output_bits, terminal_read, terminal_write])
        self.input_bits = input_bits
        self.output_bits = output_bits
        self.tos_read = tos_read
        self.tos_write = tos_write
        self.terminal_read = terminal_read
        self.terminal_write = terminal_write
        
    def cleanup(self):
        GPIO.cleanup()
