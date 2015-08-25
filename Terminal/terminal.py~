from Tkinter import *
#from threading import Thread
import time
import logging

from gpio.gpiopins import GpioPins

TOS_IN_BITS = 14
TOS_WRITE_STATUS = 15
TOS_READ_STATUS = 18
TERMINAL_OUT_BITS = 25
TERMINAL_WRITE_STATUS = 8
TERMINAL_READ_STATUS = 7

class Application(Frame):
    
    '''
    def WriteToOutput(self):
        while not self.done:
            inputs = "TOS> " + "".join(self.comm.get_input()) + "\n"
            self.TerminalOutput.insert(END, inputs)
            self.TerminalOutput.see(END)
            time.sleep(2)
     
    def CreateDaemon(self):
        self.thread.start()
        
    def QuitDaemon(self):
        self.done = True
    '''   
        
    def CreateTerminalOuput(self):
        self.TerminalOutputLabel = Label(self, text="Output:")
        self.TerminalOutput = Text(self, width="100", height="15", bg="grey") 
        self.scrollbar = Scrollbar(self, orient=VERTICAL, command=self.TerminalOutput.yview)
        self.TerminalOutputLabel.grid(row=0, sticky=NW)
        self.TerminalOutput.grid(row=1, column=0, padx=5, pady=2)
        self.scrollbar.grid(row=1, column=1, sticky=N+S)
        self.TerminalOutput["yscrollcommand"] = self.scrollbar.set
        
    def sendText(self):
        input_text = self.InputString.get()
        inputs = "TOS> {0}\n".format(self.comm.get_reply(input_text))
        self.TerminalOutput.insert(END, inputs)
        #self.TerminalOutput.insert(END, self.InputString.get())
        self.TerminalOutput.see(END)
        logger.debug("Insert string {0}".format(self.InputString.get()))
        self.TerminalInput.delete(0, END)
        
        
    def keyEvent(self, event):
        if event.keysym == 'Return':
            self.sendText()
            
    def cleanup(self):
        self.comm.cleanup()
        
    def CreateTerminalInput(self):
        self.InputString = StringVar()
        self.TerminalIutputLabel = Label(self, text="Input:")
        self.TerminalInput = Entry(self, width="100", textvariable=self.InputString)
        self.SendButton = Button(self, text="Send", command=self.sendText)
        self.TerminalInput.bind("<Return>", self.keyEvent)
        self.TerminalIutputLabel.grid(row=2, sticky=NW)
        self.TerminalInput.grid(row=3, column=0, padx=5, pady=2)
        self.SendButton.grid(row=3, column=1)
        

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.CreateTerminalOuput()
        self.CreateTerminalInput()
        self.comm = GpioPins(input_bits=TOS_IN_BITS, output_bits=TERMINAL_OUT_BITS, tos_read=TOS_READ_STATUS, tos_write=TOS_WRITE_STATUS, terminal_read=TERMINAL_READ_STATUS, terminal_write=TERMINAL_WRITE_STATUS)
        #self.thread = Thread(target=self.WriteToOutput)
        self.done = False

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logger = logging.getLogger("tos")
    root = Tk()
    root.title("TOS Terminal")
    app = Application(master=root)
    #app.CreateDaemon()
    app.mainloop()
    #app.QuitDaemon()
    app.cleanup()
    
    
