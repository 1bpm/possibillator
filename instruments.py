import pyo,pyclbr,random,os,audio,instance,pitch,timing,looper
    

class instrumentTemplate(object):
    def __init__(self):
        self._mouseDown=0
        self._setupControl()
    def _outputRouting(self):
        audio.mainOut.setInstr(self.out)
        looper.setInput(self.out)
    def _setupControl(self):
        self._env=pyo.Adsr(attack=self.__class__.attack,
                       decay=self.__class__.decay,
                       sustain=self.__class__.sustain,
                       release=self.__class__.release)
        if self.__class__.duration>0:
            self._hold=0
            self._env.setDur(self.__class__.duration)
        else:
            self._hold=1
        
    def eventHandle(self,event):
        if event.type==5:
            self.currentpos=event.pos
        if timing.autoTrigEnabled==1 and event.type==5:
            self.trigger=pyo.TrigFunc(timing.autoTrig,self.trigMouseDown)
            self._mouseDown=1
            self._env.play()
            timing.autoTrig.play()
        if timing.autoTrigEnabled==1 and event.type==6:
            self.trigger=None
            self._mouseDown=0
            self._env.stop()
            timing.autoTrig.stop()
        else:
            self.mouseHandle(event)
            
    def mouseHandle(self,event):
        if event.type == 5:
            self._mouseDown=1
            self.mouseDown(event.pos)
            self._env.play()
        if event.type == 6:
            self._mouseDown=0
            self.mouseUp(event.pos)
            if self._hold:
                self._env.stop()
        if event.type == 4:
            self.mouseMotion(event.pos)
    def trigMouseDown(self):
        self.mouseDown(self.currentpos)
    def mouseDown(self,pos):
        pass
    def mouseUp(self,pos):
        pass
    def mouseMotion(self,pos):
        pass
    
    
    
class instr1(instrumentTemplate):
    attack=0.1
    decay=2
    sustain=0.1
    release=0.1
    duration=0

    def __init__(self):
        super(instr1, self).__init__()
        self.out=pyo.FM(440,ratio=0.4,mul=self._env,index=3)
        self._outputRouting()
    def mouseMotion(self,pos):
        self.out.setCarrier(pitch.getFreqFromPos(pos[0]))
        self.out.setIndex((pos[1]/100)+0.1)
    def mouseDown(self,pos):
        self.mouseMotion(pos)
        self._env.play()
        
class instr2(instrumentTemplate):
    attack=0.01
    decay=0.1
    sustain=0.1
    release=0.3
    duration=0

    def __init__(self):
        super(instr2, self).__init__()
        self.fm1=pyo.FM(440,ratio=0.4,index=3,mul=self._env)   
        self.fm2=pyo.FM(220,ratio=0.8,index=2,mul=self._env)
        self.mix=pyo.Mixer(outs=1,chnls=2)
        self.mix.addInput(0,self.fm1)
        self.mix.addInput(1,self.fm2)
        self.mix.setAmp(0,0,0.5)
        self.mix.setAmp(1,0,0.5)
        self.out=self.mix[0]
        self._outputRouting()
    def mouseMotion(self,pos):
        self.fm1.setCarrier(pitch.getFreqFromPos(pos[0]))
        self.fm1.setRatio(pos[1]/10)
        self.fm2.setCarrier(pitch.getFreqFromPos(pos[0])*0.5)
        self.fm2.setRatio(pos[1]/10)
    def mouseDown(self,pos):
        self.mouseMotion(pos)
        self._env.play()      

class instr3(instrumentTemplate):
    attack=0.01
    decay=10
    sustain=10
    release=0.4
    duration=0

    def __init__(self):
        super(instr3, self).__init__()
        self.fm=pyo.FM(440,ratio=1.67,index=0.08,mul=self._env)
        self.out=pyo.Freeverb(self.fm,size=0.9,damp=0.1,bal=1)
        self._outputRouting()
    def mouseMotion(self,pos):
        self.fm.setCarrier(pitch.getFreqFromPos(pos[0]))
        self.out.setBal((pos[1]/240)+0.1)
    def mouseDown(self,pos):
        self.mouseMotion(pos)
        self._env.play()  

class instr4(instrumentTemplate):
    attack=0.01
    decay=10
    sustain=10
    release=0.4
    duration=0

    def __init__(self):
        super(instr4, self).__init__()
        self.mix=pyo.Mixer(outs=1,chnls=2)
        self.out=self.mix[0]
        self.kicks=[]
        self.snares=[]
        self.setupPlayers()
        self._outputRouting()
    def setupPlayers(self):
        bkpath="/home/audio/BreakCuts/BreakCut-1/"
        files=[ f for f in os.listdir(bkpath) if os.path.isfile(os.path.join(bkpath,f)) ]
        for f in random.sample(files,15):
            self.kicks.append(pyo.SfPlayer(os.path.join(bkpath,f)).stop())
            key=self.mix.addInput(voice=None,input=self.kicks[-1])
            self.mix.setAmp(key,0,1.5)
          
        bkpath="/home/audio/BreakCuts/BreakCut-5"
        files=[ f for f in os.listdir(bkpath) if os.path.isfile(os.path.join(bkpath,f)) ]
        for f in random.sample(files,15):
            self.snares.append(pyo.SfPlayer(os.path.join(bkpath,f)).stop())
            key=self.mix.addInput(voice=None,input=self.snares[-1])
            self.mix.setAmp(key,0,1.5)
           
    def mouseMotion(self,pos):
        if pos[0]<120:
            nm=int(pos[0]/8)
            self.currKick=True
        else:
            nm=int((pos[0]-120)/8)
            self.currKick=False
        self.currentNum=nm
    def mouseDown(self,pos):
        self.mouseMotion(pos)
        if self.currKick:
            try:
                self.kicks[self.currentNum].play()
            except IndexError:
                pass
        else:
            try:
                self.snares[self.currentNum].play()
            except IndexError:
                pass


class instr5(instrumentTemplate):
    attack=0.4
    decay=0.1
    sustain=0.1
    release=0.3
    duration=0

    def __init__(self):
        super(instr5, self).__init__()
        self.fm1=pyo.FM(440,ratio=0.9,index=2.9,mul=self._env)   
        self.fm2=pyo.FM(220,ratio=2,index=2.3,mul=self._env)
        self.mix=pyo.Mixer(outs=1,chnls=2)
        self.mix.addInput(0,self.fm1)
        self.mix.addInput(1,self.fm2)
        self.mix.setAmp(0,0,0.5)
        self.mix.setAmp(1,0,0.5)
        self.out=self.mix[0]
        self._outputRouting()
    def mouseMotion(self,pos):
        self.fm1.setCarrier(pitch.getFreqFromPos(pos[0]))
        self.fm1.setRatio(pos[1]/10)
        self.fm2.setCarrier(pitch.getFreqFromPos(pos[0])*0.5)
        self.fm2.setRatio(pos[1]/10)
    def mouseDown(self,pos):
        self.mouseMotion(pos)
        self._env.play()     

class instr6(instrumentTemplate):
    attack=0.4
    decay=0.1
    sustain=0.1
    release=0.3
    duration=0

    def __init__(self):
        super(instr6, self).__init__()
        self.fm1=pyo.FM(440,ratio=0.4,index=1.9,mul=1)   
        self.fm2=pyo.FM(220,ratio=0.7,index=1.3,mul=1)
        self.pv1=pyo.PVAnal(self.fm1)
        self.pv2=pyo.PVAnal(self.fm2)
        self.pvc=pyo.PVMorph(self.pv1, self.pv2, fade=0.5)
        self.out=pyo.PVSynth(self.pvc,1)#self._env
        self._outputRouting()
    def mouseMotion(self,pos):
        self.fm1.setCarrier(pitch.getFreqFromPos(pos[0]))
        #self.pvc.setFade(240/pos[1])
        self.fm2.setCarrier(pitch.getFreqFromPos(pos[1])*0.5)
        
    def mouseDown(self,pos):
        self.mouseMotion(pos)
        self._env.play()   


current=instr1()

currentNum=0

instrumentList=[]
for instr in pyclbr.readmodule("instruments").keys():
    if instr!="instrumentTemplate":
        instrumentList.append(instr)

#self.current=instruments.instr1()
print instrumentList
def last():
    global current,currentNum
    proposedNum=currentNum-1
    if proposedNum<0: 
        proposedNum=len(instrumentList)-1
    theInstr=instrumentList[proposedNum]
    currentNum=proposedNum
    current=eval(theInstr+"()")
    
    
def next():
    global current,currentNum
    proposedNum=currentNum+1
    print proposedNum
    try:
        theInstr=instrumentList[proposedNum]
        currentNum=proposedNum
    except IndexError:
        theInstr=instrumentList[0]
        currentNum=0
    current=eval(theInstr+"()")