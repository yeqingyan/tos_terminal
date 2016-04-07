import SocketServer
import threading
import sys

SOCKET_PORT = 8989

def bin_to_int(array):
    binary = "".join(map(str, array))
    return int(binary, base=2)

def value_to_pin(value):
    pin = 0
    while (pin < 32) and ((value & 1) == 0):
        value = value >> 1;
        pin += 1

    if pin >= 32:
        print "Wrong pin value!"
        return -1

    return pin

class TosHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        self.GPLEV0 = [0 for _ in range(32)]
        self.GPLEV1 = [0 for _ in range(32)]
        self.GPPUD = 1
        self.GPPUDCLK0 = [0 for _ in range(32)]
        self.GPPUDCLK1 = [0 for _ in range(32)]
        #self.TOS_WRITE_WAIT = false

    def handle(self):
        data = self.request.recv(255)
        #.split("#")
        print "Got data {0}".format(data)
        #print "{0}".format([int(i) for i in data])
        
        ''' 
        cmd = data[0]
        rw = data[1]
        if len(data) >= 3:
            value = int(data[2])
        else:
            value = 0            
        
        if rw not in 'RW':
            print "Error: RW flag is not correct, got {0}".format(rw)
            sys.exit()
        response = ""
        
        if cmd == "GPLEV0":
            response = str(bin_to_int(self.GPLEV0))
            
        elif cmd == "GPLEV1":
            response = str(bin_to_int(self.GPLEV1))
            
        elif cmd == "GPSET0":
            channel = value_to_pin(value)
            self.GPLEV0[31-channel] = '1'
            response = "OK"
            
        elif cmd == "GPSET1":
            channel = value_to_pin(value)
            self.GPLEV1[63-channel] = '1'
            response = "OK"
            
        elif cmd == "GPCLR0":
            channel = value_to_pin(value)
            self.GPLEV0[31-channel] = '0'
            response = "OK"
            
        elif cmd == "GPCLR1":        
            channel = value_to_pin(value)
            self.GPLEV1[63-channel] = '0'
            response = "OK"
        
        elif cmd == "GPPUD":
            if rw == 'R':     
                response = str(self.GPPUD)
            else:
                response = "OK"
                
        elif cmd == "GPPUDCLK0":
            response = "OK"
            
        elif cmd == "GPPUDCLK1":
            response = "OK"                            
        
        #elif cmd == "TOS_WRITE":   
        else:
            print "Meet error! Data {0}".format(data)
            sys.exit()
        '''
        response = "OK"            
        self.request.sendall(response)     
        print "Sent: {0}".format(response)           
        
class TosGPIOServer():
    def __init__(self):
        SocketServer.TCPServer.allow_reuse_address = True
        self.tos_server = SocketServer.TCPServer(("127.0.0.1", SOCKET_PORT), TosHandler)
        
    def run(self):
        print "GPIO server start running..."
        self.tos_server.serve_forever()
    
    def quit(self):
        self.tos_server.shutdown()

def main():
    tos_gpio_server = TosGPIOServer()
    tos_gpio_server.run()

if __name__ == "__main__":
    main()
