import json

freqData=[]
scales=json.load(open("chords.json"))
tuning=json.load(open("tuning.json"))
baseNotes=json.load(open("basenotes.json"))

baseFreq=440
currentBaseNoteNum=0
pitchSteps=12
currentBaseNote=0
currentTuning=tuning[1]
currentScale=scales[13]



def setOctave(num):
    global currentOctave
    currentOctave=num
    setBaseNote(currentBaseNoteNum)

def setScale(num):
    global currentScale,currentScaleNum
    currentScale=scales[num]
    currentScaleNum=num
    setFreqs()

def setTuning(num):
    global currentTuning,currentTuningNum
    currentTuning=tuning[num]
    currentTuningNum=num
    setFreqs()

def setPitchSteps(steps):
    global pitchSteps
    pitchSteps=steps
    setFreqs()

def setBaseNote(num):
    global currentBaseNote,currentBaseNoteNum
    currentBaseNote=baseNotes[num]
    currentBaseNoteNum=num
    if currentOctave==4:
        mult=1
    if currentOctave>4:
        mult=(currentOctave-4)+1
    if currentOctave<4:
        mult=1/((4-currentOctave)+1)
    setBaseFreq(currentBaseNote.get("freq")*mult)

def setBaseFreq(freq):
    global baseFreq
    baseFreq=freq
    setFreqs()


def getFreqFromPos(onePos):
        tpos=round(float(float(onePos)/240)*pitchSteps)
        return freqData[int(tpos)]


def setFreqs():
    global freqData
    tempfreqData=[]
    curT=0
    bFreq=baseFreq
    tune=currentTuning.get("ratios")
    for x in range(0,512):
        if tune[curT]==2:
            bFreq=bFreq*2
            curT=0
        else:
            tempfreqData.append(bFreq*tune[curT])
            curT+=1
    freqData=[]
    curT=0
    pitches=currentScale.get("intv")
    for x in range(0,pitchSteps):
        for p in pitches:
            num=int(p)+int(curT)
            try:
                freqData.append(tempfreqData[num])
            except IndexError:
                pass
        curT+=len(currentTuning.get("ratios"))-1
    freqData.sort()


# defaults
setScale(26)
setTuning(1)
setOctave(4)
