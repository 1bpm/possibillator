import pyo
import json,looper

bpm=120
metronomeEnabled=False
out=pyo.Metro(0.5).play()
metroSound=pyo.SfPlayer("metro.wav").stop()


autoTrig=pyo.Beat(0.125)
autoTrigEnabled=0
trigPresets=json.load(open("beatPresets.json"))




def setMetronome(state):
    global metronomeEnabled
    metronomeEnabled=state

def _metroTrigger():
    if metronomeEnabled==1:
        metroSound.out()
metroTrig=pyo.TrigFunc(out,_metroTrigger)

def setLoopLength(loopLength):
    loopLength=loopLength
    time=loopLength*(bpm/60)
    looper.setTime(time)


def setAutoTrigStatus(isEnabled):
    global autoTrigEnabled
    autoTrigEnabled=isEnabled

def setAutoTrig(num):
    autoTrig.recall(num)

def setBpm(bpm):
    bpm=bpm
    timing=60/bpm
    autoTrig.setTime(timing/4)
    out.setTime(timing)
    looper.setTime(timing*loopLength)

def setupPatterns():
    autoTrig.setPresets(trigPresets)
    setAutoTrig(0)
    #pyo.TrigFunc(self.autoTrig)



setupPatterns()
autoTrigNum=0
loopLength=4