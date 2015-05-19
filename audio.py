import pyo


pyoServer=pyo.Server(nchnls=2,duplex=0).boot()
pyoServer.start()

class coreAudio():
    def __init__(self):
        self.out=pyo.Mixer(outs=1,chnls=2,mul=0.9).out()
    def setLoop(self,input):
        self.setIn(input,0)
    def setInstr(self,input):
        self.setIn(input,1)
    def setIn(self,input,inpNum=0):
#       if inpNum in self.out.getKeys():
        print "setting"+str(inpNum)
        self.out.delInput(inpNum)
        self.out.addInput(voice=inpNum,input=input)
        self.out.setAmp(inpNum,0,1)
        
mainOut=coreAudio()



