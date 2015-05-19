import pygame
import instance
import instruments
import looper

    
class gui:
    pygame = pygame
    pygame.init()
    pygame.font.init()
    pygame.mouse.set_visible(1);
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    BLUE =  (  0,   0, 255)
    GREEN = (  0, 255,   0)
    RED =   (255,   0,   0)
    screen = pygame.display.set_mode([320, 240])
    surfaceMain = pygame.Surface([320,240])
    surfaceXY=pygame.Surface([240,240])
    surfaceMenu=pygame.Surface([80,160])
    surfaceRec=pygame.Surface([80,80])
    instrNum=1
    done = False
    popup=None
    popupActive=0
    clock = pygame.time.Clock()
    imgXY=pygame.image.load("xyArea.png")
    imgPitch=pygame.image.load("selectPitch.png")
    imgTime=pygame.image.load("selectTime.png")
    imgInstr=pygame.image.load("selectInstrument.png")
    
    @staticmethod
    def setGui():
        gui.surfaceXY.fill(gui.BLACK)
        gui.surfaceXY.blit(gui.imgXY,[0,0])
        gui.surfaceMenu.fill(gui.BLACK)
        gui.surfaceMenu.blit(gui.imgInstr,[0,0])
        gui.surfaceMenu.blit(gui.imgTime,[0,40])
        gui.surfaceMenu.blit(gui.imgPitch,[0,80])
    
    
    @staticmethod
    def poll():
        gui.surfaceMain.fill(gui.BLACK)
        if instance.current!=None:
            gui.surfaceMain.blit(instance.current.poll(),[0,0])
        else:
            gui.surfaceRec.fill(gui.BLACK)
            if looper.recording==1:
                gui.pygame.draw.polygon(gui.surfaceRec,gui.GREEN,[[20,20],[20,60],[60,40]])
            else:
                gui.pygame.draw.circle(gui.surfaceRec,gui.RED,[40,40],30)
            mainFont=gui.pygame.font.Font(pygame.font.match_font("bitstreamverasans"), 15)
            iLabel=mainFont.render(str(gui.instrNum),1,(110,190,110))
            gui.surfaceMenu.blit(iLabel,[20,10])
            gui.surfaceMain.blit(gui.surfaceXY,[0,0])
            gui.surfaceMain.blit(gui.surfaceMenu,[240,0])
            gui.surfaceMain.blit(gui.surfaceRec,[240,160])
        gui.screen.blit(gui.surfaceMain,[0,0])
        gui.pygame.display.flip()
        gui.clock.tick(20)
    
    
    @staticmethod
    def colour(htmlColour):
        """convert css style colour to rgb tuple"""
        value = htmlColour.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

    @staticmethod
    def controlClick(pos):
        if pos[1]<40 and pos[0]<300:
            instruments.last()
            gui.instrNum=instruments.currentNum+1
        if pos[1]<40 and pos[0]>300:
            instruments.next()
            gui.instrNum=instruments.currentNum+1
        if pos[1]>40 and pos[1]<80:
            instance.timeOverlay()
        if pos[1]>80 and pos[1]<120:
            instance.pitchOverlay()
        if pos[1]>160:
            looper.toggleStatus()

        
    @staticmethod
    def eventHandle(event):
        if instance.current==None:
            if event.type==gui.pygame.MOUSEBUTTONDOWN and event.pos[0]>240:
                gui.controlClick(event.pos)
                if event.pos[1]<40 or event.pos[1]>160:
                    gui.setGui()
                gui.poll()
            else:
                instruments.current.eventHandle(event)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0]>280 and event.pos[1]<40:
                instance.current=None
            else:
                instance.current.eventHandle(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                gui.poll()
              
    @staticmethod
    def eventHandlx(event):
        if event.type == pygame.MOUSEMOTION:
            if event.pos[0]<240:
                gui.eventChange(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0]>240:
                    gui.controlClick(event.pos)
                else:
                    gui.eventClick(event)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.pos[0]<240:
                    gui.eventStop()
        
    @staticmethod
    def runLoop():
        #container.time.looper.createLoop()
        gui.setGui()
        gui.poll()
        while not gui.done:
            for event in pygame.event.get():
                if gui.popupActive:
                    gui.popup._eventHandle(event)
                else:
                    gui.eventHandle(event)
            gui.clock.tick(60)
                    
gui.runLoop()                  
try:
    pass
except Exception,e:
    container.pop.fatalOverlay(e)