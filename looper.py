import audio
import pyo

delay=1000
recording=False
_dummyInput=pyo.Sine(440).stop()
input=pyo.Mixer(chnls=2,outs=1,mul=1)
input.addInput(0,_dummyInput)
out=pyo.Delay(input[0],delay,1,32)
audio.mainOut.setLoop(out)



def setTime(self,time):
    global out
    out.setDelay(time)

def setActive():
    global recording
    recording=True
    input.setAmp(0,0,1)

def setInactive():
    global recording
    recording=False
    input.setAmp(0,0,0)

def setInput(newInput):
    input.delInput(0)
    input.addInput(0,newInput)
    if recording:
        setActive()
    else:
        setInactive()

def toggleStatus():
    if recording:
        setInactive()
    else:
        setActive()