import grooves
import popups

popupActive=False
current=None


def _setState(popup,state=True):
    global popupActive,current
    current=popup
    popupActive=state


def closePopup(): _setState(None,False)
def pitchOverlay(): _setState(popups.pitchPopup())
def timeOverlay(): _setState(popups.timePopup())
def fatalOverlay(message): _setState(popups.fatalPopup(message))
