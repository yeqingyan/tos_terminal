import RPI_stub as GPIO

class GpioPins():
   
    def setup_input(self, channels):
        """Setup input channel.
        
        Keyword arguments:
        channels -- input channel list, their order must match the GPIO pin pairs on the circult board
        """
        if not isinstance(channels, list):
            raise TypeError('Channels should be list type')
        
        for channel in channels:
            GPIO.setup(channel, GPIO.IN)
        
        self.input_channels = channels
          
    def get_input(self):
        """Get value from input channels"""
        return [GPIO.input(channel) for channel in self.input_channels]
                
        
    def __init__(self, input_channels=None, output_channels=None):
        GPIO.setmode(GPIO.BCM)
        self.setup_input(input_channels)
        self.input_channels = input_channels
        self.output_channels = output_channels