import pyo,json,audio

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
        
class time():
    def __init__(self):
        self.bpm=120
        self.metronomeEnabled=0
        self.out=pyo.Metro(0.5).play()
        self.metroSound=pyo.SfPlayer("metro.wav").stop()
        self.metroTrig=pyo.TrigFunc(self.out,self._metroTrigger)
        self.autoTrig=pyo.Beat(0.125)
        self.autoTrigEnabled=0
        self.setupPatterns()
        self.autoTrigNum=0
        self.looper=looper(4)
        self.loopLength=4
    def setMetronome(self,state):
        self.metronomeEnabled=state
    def _metroTrigger(self):
        if self.metronomeEnabled==1:
            self.metroSound.out()
    def setLoopLength(self,loopLength):
        self.loopLength=loopLength
        time=loopLength*(self.bpm/60)
        self.looper.setTime(time)
    def getLoopLength(self):
        return self.loopLength
    def setAutoTrigStatus(self,isEnabled):
        self.autoTrigEnabled=isEnabled
    def setAutoTrig(self,num):
        self.autoTrig.recall(num)
    def setBpm(self,bpm):
        self.bpm=bpm
        timing=60/bpm
        self.autoTrig.setTime(timing/4)
        self.out.setTime(timing)
        self.looper.setTime(timing*self.loopLength)
    def setupPatterns(self):
        self.trigPresets=json.load(open("beatPresets.json"))
        self.autoTrig.setPresets(self.trigPresets)
        self.setAutoTrig(0)
        #pyo.TrigFunc(self.autoTrig)
        

class pitch():
    def __init__(self):
        self.freqData=[]
        self.scales=json.load(open("chords.json"))
        self.tuning=json.load(open("tuning.json"))
        self.baseNotes=json.load(open("basenotes.json"))
        self.baseFreq=440
        self.currentBaseNoteNum=0
        self.pitchSteps=12
        self.currentBaseNote=0
        self.currentTuning=self.tuning[1]
        self.setScale(26)
        self.setTuning(1)  
        self.setOctave(4)
    def setOctave(self,num):
        self.currentOctave=num
        self.setBaseNote(self.currentBaseNoteNum)
    def setScale(self,num):
        self.currentScale=self.scales[num]
        self.currentScaleNum=num
        self.setFreqs()
    def setTuning(self,num):
        self.currentTuning=self.tuning[num]
        self.currentTuningNum=num
        self.setFreqs()
    def setPitchSteps(self,steps):
        self.pitchSteps=steps
        self.setFreqs()
    def setBaseNote(self,num):
        self.currentBaseNote=self.baseNotes[num]
        self.currentBaseNoteNum=num
        if self.currentOctave==4:
            mult=1
        if self.currentOctave>4:
            mult=(self.currentOctave-4)+1
        if self.currentOctave<4:
            mult=1/((4-self.currentOctave)+1)
        self._setBaseFreq(self.currentBaseNote.get("freq")*mult)
    def _setBaseFreq(self,freq):
        self.baseFreq=freq
        self.setFreqs()
    def getFreqFromPos(self,onePos):
        tpos=round(float(float(onePos)/240)*self.pitchSteps)
        return self.freqData[int(tpos)]
    def setFreqs(self):
        _freqData=[]
        curT=0
        bFreq=self.baseFreq
        tune=self.currentTuning.get("ratios")
        for x in range(0,512):
            if tune[curT]==2:
                bFreq=bFreq*2
                curT=0
            else:
                _freqData.append(bFreq*tune[curT])
                curT+=1
        self.freqData=[]
        curT=0
        pitches=self.currentScale.get("intv")
        for x in range(0,self.pitchSteps):
            for p in pitches:
                num=int(p)+int(curT)
                try:
                    self.freqData.append(_freqData[num])
                except IndexError:
                    pass
            curT+=len(self.currentTuning.get("ratios"))-1
        self.freqData.sort()
        
        
