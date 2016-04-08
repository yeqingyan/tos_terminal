from Tkinter import *
from threading import Thread
import logging
import SocketServer

app = None
SOCKET_PORT = 8989


class GpioHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(255)
        app.show_msg(data)
        response = "OK"            
        self.request.sendall(response)


class Application(Frame):
    def show_msg(self, msg):
        inputs = "TOS> " + msg + "\n"
        self.TerminalOutput.insert(END, inputs)
        self.TerminalOutput.see(END)

    def create_terminal_output(self):

        self.TerminalOutputLabel.grid(row=0, sticky=NW)
        self.TerminalOutput.grid(row=1, column=0, padx=5, pady=2)
        self.scrollbar.grid(row=1, column=1, sticky=N+S)
        self.TerminalOutput["yscrollcommand"] = self.scrollbar.set
                    
    def cleanup(self):
        print "Clean thread"
        self.done = True
        self.gpio_server.shutdown()
        self.gpio_server.server_close()
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.done = False
        self.TerminalOutputLabel = Label(self, text="Output:")
        self.TerminalOutput = Text(self, width="100", height="15", bg="grey")
        self.scrollbar = Scrollbar(self, orient=VERTICAL, command=self.TerminalOutput.yview)

        self.pack()
        self.create_terminal_output()

        # Setup GPIO server thread
        SocketServer.TCPServer.allow_reuse_address = True
        self.gpio_server = SocketServer.TCPServer(("127.0.0.1", SOCKET_PORT), GpioHandler)
        self.server_thread = Thread(target=self.gpio_server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
            
if __name__ == "__main__":
    global app
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logger = logging.getLogger("tos")
    root = Tk()
    root.title("TOS Terminal")
    app = Application(master=root)    
    app.mainloop()
    app.cleanup()
