import pygame
import pitch
import timing

pygame.font.init()


current=None

class popup(object):
    def __init__(self):
        self.overlaySurface=pygame.Surface([280,240])
        self.surfaceMain=pygame.Surface([320,240])
    def eventHandle(self,event):
        pass
    def poll(self):
        self.surfaceMain.fill((0,0,0))
        self.overlaySurface.fill((0,0,0))
        closer=pygame.Surface([40,40])
        pygame.draw.line(closer,(255,0,0),[5,5],[35,35],5)
        pygame.draw.line(closer,(255,0,0),[35,5],[5,35],5)
        self.surfaceMain.blit(closer,[280,0])
        self.renderInner()
        self.surfaceMain.blit(self.overlaySurface,[0,0])
        return self.surfaceMain
    
class fatalPopup(popup):
    def __init__(self,message):
        super(fatalPopup, self).__init__()    
        self.mainFont=pygame.font.Font(pygame.font.match_font("bitstreamverasans"), 15)
        self.bigFont=mainFont=pygame.font.Font(pygame.font.match_font("bitstreamverasans"), 24)
        
    def renderInner(self):
        bLabel=self.bigfont.render("caught fatal!",1,(200,0,0))
        sLabel=self.mainFont.render(str(message),1,(120,120,120))
        self.overlaySurface.blit(bLabel,[10,10])
        self.overlaySurface.blit(sLabel,[10,50])

class pitchPopup(popup):
    def __init__(self):
        super(pitchPopup, self).__init__()
        self.surfaceTuning=pygame.Surface([280,60])
        self.surfaceScale=pygame.Surface([280,60])
        self.surfaceSteps=pygame.Surface([140,60])
        self.surfaceBase=pygame.Surface([140,60])
        self.mainFont=pygame.font.Font(pygame.font.match_font("bitstreamverasans"), 15)
        self.bigFont=mainFont=pygame.font.Font(pygame.font.match_font("bitstreamverasans"), 24)
        
    def renderInner(self):
        # tuning select
        
        self.surfaceTuning.fill((0,0,0))
        pygame.draw.polygon(self.surfaceTuning,(0,100,0),[[10,30],[30,10],[30,50]])
        pygame.draw.polygon(self.surfaceTuning,(0,100,0),[[270,30],[250,10],[250,50]])
        tLabel=self.bigFont.render(pitch.currentTuning.get("name"),1,(200,200,200))
        hLabel=self.mainFont.render("tuning",1,(110,190,110))
        self.surfaceTuning.blit(hLabel,[40,0])
        self.surfaceTuning.blit(tLabel,[60,20])          
        # scale select
        self.surfaceScale.fill((0,0,0))
        pygame.draw.polygon(self.surfaceScale,(0,100,0),[[10,30],[30,10],[30,50]])
        pygame.draw.polygon(self.surfaceScale,(0,100,0),[[270,30],[250,10],[250,50]])
        tLabel=self.bigFont.render(pitch.currentScale.get("name"),1,(200,200,200))
        hLabel=self.mainFont.render("scale",1,(110,190,110))
        self.surfaceScale.blit(hLabel,[40,0])
        self.surfaceScale.blit(tLabel,[40,20])       
        # steps select
        self.surfaceSteps.fill((0,0,0))
        pygame.draw.polygon(self.surfaceSteps,(0,100,0),[[10,30],[30,10],[30,50]])
        pygame.draw.polygon(self.surfaceSteps,(0,100,0),[[130,30],[110,10],[110,50]])
        tLabel=self.bigFont.render(str(pitch.pitchSteps),1,(200,200,200))
        hLabel=self.mainFont.render("steps",1,(110,190,110))
        self.surfaceSteps.blit(hLabel,[40,0])
        self.surfaceSteps.blit(tLabel,[55,20])      
        # base select
        self.surfaceBase.fill((0,0,0))
        pygame.draw.polygon(self.surfaceBase,(0,100,0),[[10,30],[30,10],[30,50]])
        pygame.draw.polygon(self.surfaceBase,(0,100,0),[[130,30],[110,10],[110,50]])
        tLabel=self.bigFont.render(pitch.currentBaseNote.get("name"),1,(200,200,200))
        hLabel=self.mainFont.render("base",1,(110,190,110))
        self.surfaceBase.blit(hLabel,[40,0])
        self.surfaceBase.blit(tLabel,[55,20])
        # show all
        self.overlaySurface.blit(self.surfaceTuning,[0,0])
        self.overlaySurface.blit(self.surfaceScale,[0,60])
        self.overlaySurface.blit(self.surfaceSteps,[0,120])
        self.overlaySurface.blit(self.surfaceBase,[140,120])
        # line left for 180
    
    def eventHandle(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x=event.pos[0]
            y=event.pos[1]
            if x<60 and y<60:
                self.tuningDown()
            if x>220 and x<280 and y<60:
                self.tuningUp()
            if x<60 and y>60 and y<120:
                self.scaleUp()
            if x>220 and x<280 and y>60 and y<120:
                self.scaleDown()
            if x<60 and y>120 and y<180:
                self.stepsDown()
            if x>100 and x<140 and y>120 and y<180:
                self.stepsUp()
            if x>140 and x<200 and y>120 and y<180:
                self.baseDown()
            if x>220 and x<280 and y>120 and y<180:
                self.baseUp()
    
    def stepsUp(self):
        proposedNum=pitch.pitchSteps+1
        if proposedNum<32:
            pitch.setPitchSteps(proposedNum)
 
    
    def stepsDown(self):
        proposedNum=pitch.pitchSteps-1
        if proposedNum>3:
            pitch.setPitchSteps(proposedNum)
    
        
    def baseUp(self):
        proposedNum=pitch.currentBaseNoteNum+1
        try:
            checkNum=pitch.baseNotes[proposedNum]
            pitch.setBaseNote(proposedNum)
        except IndexError:
            pitch.setBaseNote(0)

            
    def baseDown(self):
        proposedNum=pitch.currentBaseNoteNum-1
        try:
            checkNum=pitch.baseNotes[proposedNum]
            pitch.setBaseNote(proposedNum)
        except IndexError:
            index=len(pitch.baseNotes)-1
            pitch.setBaseNote(index)

        
        
    def tuningUp(self):
        proposedNum=pitch.currentTuningNum+1
        try:
            checkNum=pitch.tuning[proposedNum]
            pitch.setTuning(proposedNum)
        except (IndexError,KeyError):
            pitch.setTuning(0)

            
            
    def tuningDown(self):
        proposedNum=pitch.currentTuningNum-1
        try:
            checkNum=pitch.tuning[proposedNum]
            pitch.setTuning(proposedNum)
        except (IndexError,KeyError):
            index=len(pitch.tuning)-1
            pitch.setTuning(index)

        

    def scaleUp(self):
        proposedNum=pitch.currentScaleNum+1
        try:
            checkNum=pitch.scales[proposedNum]
            pitch.setScale(proposedNum)
        except (IndexError,KeyError):
            pitch.setScale(0)

        
    def scaleDown(self):
        proposedNum=pitch.currentScaleNum-1
        try:
            checkNum=pitch.scales[proposedNum]
            pitch.setScale(proposedNum)
        except (IndexError,KeyError):
            index=len(pitch.scales)-1
            pitch.setScale(index)
       

  
       
class timePopup(popup):
    def __init__(self):
        super(timePopup, self).__init__()

        self.surfaceBpm=pygame.Surface([140,60])
        self.surfaceLoopLen=pygame.Surface([140,60])
        self.surfacePattern=pygame.Surface([140,60])
        self.surfacePatternToggle=pygame.Surface([120,40])  
        self.surfaceMetronomeToggle=pygame.Surface([120,40])
        self.mainFont=pygame.font.Font(pygame.font.match_font("bitstreamverasans"), 15)
        self.bigFont=pygame.font.Font(pygame.font.match_font("bitstreamverasans"), 24)
    def renderInner(self):
        self.surfaceBpm.fill((0,0,0))
        pygame.draw.polygon(self.surfaceBpm,(0,100,0),[[10,30],[30,10],[30,50]])
        pygame.draw.polygon(self.surfaceBpm,(0,100,0),[[130,30],[110,10],[110,50]])
        tLabel=self.bigFont.render(str(timing.bpm),1,(200,200,200))
        hLabel=self.mainFont.render("bpm",1,(110,190,110))
        self.surfaceBpm.blit(hLabel,[40,0])
        self.surfaceBpm.blit(tLabel,[55,20])        
        
        self.surfaceLoopLen.fill((0,0,0))
        pygame.draw.polygon(self.surfaceLoopLen,(0,100,0),[[10,30],[30,10],[30,50]])
        pygame.draw.polygon(self.surfaceLoopLen,(0,100,0),[[130,30],[110,10],[110,50]])
        tLabel=self.bigFont.render(str(timing.getLoopLength()),1,(200,200,200))
        hLabel=self.mainFont.render("loop length",1,(110,190,110))
        self.surfaceLoopLen.blit(hLabel,[40,0])
        self.surfaceLoopLen.blit(tLabel,[55,20])  
        
        self.surfacePattern.fill((0,0,0))
        pygame.draw.polygon(self.surfacePattern,(0,100,0),[[10,30],[30,10],[30,50]])
        pygame.draw.polygon(self.surfacePattern,(0,100,0),[[130,30],[110,10],[110,50]])
        tLabel=self.bigFont.render(str(timing.autoTrigNum),1,(200,200,200))
        hLabel=self.mainFont.render("pattern",1,(110,190,110))
        self.surfacePattern.blit(hLabel,[40,0])
        self.surfacePattern.blit(tLabel,[55,20]) 
        
        if timing.autoTrigEnabled==1:
            self.surfacePatternToggle.fill((0,200,0))
            appendage="on"
        else:
            self.surfacePatternToggle.fill((200,0,0))
            appendage="off"
        tLabel=self.bigFont.render("pattern " + appendage,1,(200,200,200))
        self.surfacePatternToggle.blit(tLabel,[5,8])
        
        if timing.metronomeEnabled==1:
            self.surfaceMetronomeToggle.fill((0,200,0))
            appendage="on"
        else:
            self.surfaceMetronomeToggle.fill((200,0,0))
            appendage="off"
        tLabel=self.bigFont.render("metro " + appendage,1,(200,200,200))
        self.surfaceMetronomeToggle.blit(tLabel,[5,8])
        
        self.overlaySurface.blit(self.surfaceBpm,[0,0])
        self.overlaySurface.blit(self.surfaceLoopLen,[140,0])
        self.overlaySurface.blit(self.surfacePattern,[0,60])
        self.overlaySurface.blit(self.surfacePatternToggle,[150,70])
        self.overlaySurface.blit(self.surfaceMetronomeToggle,[10,130])
    
    def bpmUp(self):
        proposedBpm=timing.bpm+1
        if proposedBpm<998:
            timing.setBpm(proposedBpm)
            
    def bpmDown(self):
        proposedBpm=timing.bpm-1
        if proposedBpm>0:
            timing.setBpm(proposedBpm)
            
    def loopUp(self):
        proposedLoop=timing.getLoopLength()+1
        if proposedLoop<33:
            timing.setLoopLength(proposedLoop)
    
    def loopDown(self):
        proposedLoop=timing.getLoopLength()-1
        if proposedLoop>0:
            timing.setLoopLength(proposedLoop)
 
    def toggleMetronome(self):
        if timing.metronomeEnabled==1:
            timing.setMetronome(0)
        else:
            timing.setMetronome(1)
            
    def togglePattern(self):
        if timing.autoTrigEnabled==1:
            timing.setAutoTrigStatus(0)
        else:
            timing.setAutoTrigStatus(1)
        
    def patternUp(self):
        proposedNum=timing.autoTrigNum+1
        try:
            checkNum=timing.trigPresets[proposedNum]
            timing.autoTrig.recall(proposedNum)
            timing.autoTrigNum+=1
        except (IndexError,KeyError):
            pass
            
    def patternDown(self):
        proposedNum=timing.autoTrigNum-1
        try:
            checkNum=timing.trigPresets[proposedNum]
            timing.autoTrig.recall(proposedNum)
            timing.autoTrigNum-=1
        except (IndexError,KeyError):
            pass
        
    
        
    def eventHandle(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x=event.pos[0]
            y=event.pos[1]
            if x<60 and y<60:
                self.bpmDown()
            if x>100 and x<140 and y<60:
                self.bpmUp()
            if x>140 and x<200 and y<60:
                self.loopDown()
            if x>220 and x<280 and y<60:
                self.loopUp()
            if x<60 and y>60 and y<120:
                self.patternDown()
            if x>100 and x<140 and y>60 and y<120:
                self.patternUp()
            if x>140 and x<280 and y>60 and y<120:
                self.togglePattern()
            if x<140 and y>120 and y<180:
                self.toggleMetronome()
                