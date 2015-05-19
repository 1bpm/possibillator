import pyo


pyoServer=pyo.Server(nchnls=2,duplex=0).boot()
pyoServer.start()

out=pyo.Mixer(outs=1,chnls=2,mul=0.9).out()

def setLoop(input):
    setIn(input,0)

def setInstr(input):
    setIn(input,1)

def setIn(input,inpNum=0):
    out.delInput(inpNum)
    out.addInput(voice=inpNum,input=input)
    out.setAmp(inpNum,0,1)



class looper():
    def __init__(self,initTime=4):
        self.setTime(initTime)
        self.createLoop()
        self.setInactive()
    def setTime(self,time):
        self.delay=time
    def toggleStatus(self):
        if self.recording==1:
            self.setInactive()
        else:
            self.setActive()
    def setActive(self):
        self.recording=1
        self.input.setAmp(0,0,1)
    def setInactive(self):
        self.recording=0
        self.inputAmp=0
        self.input.setAmp(0,0,0)
    def setInput(self,input):
        self.input.delInput(0)
        self.input.addInput(0,input)
        #self.input.setAmp(0,0,1)
        if self.recording:
            self.setActive()
        else:
            self.setInactive()
    def createLoop(self):
        defaultc=pyo.Sine(440).stop()
        self.input=pyo.Mixer(chnls=2,outs=1,mul=1)
        self.input.addInput(0,defaultc)
        self.out=pyo.Delay(self.input[0],self.delay,1,32)
        audio.mainOut.setLoop(self.out)
        #self.out.out()