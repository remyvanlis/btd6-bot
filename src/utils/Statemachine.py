from .Console import Console
import pytesseract as tesser
from PIL import Image
from .GameStateEnum import GameState
from .Screen import Screen


class Statemachine:
    def __init__(self, console: Console):
        tesser.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
        self.console: Console = console

    def check_victory_state(self):
        image: Image = Screen.screen_grab([700, 120, 515, 110], "gold")
        text: str = tesser.image_to_string(image, config="--psm 6", nice=1)
        text = ''.join([c for c in text.upper() if c in "VICTORY"])
        if "VICTORY" in text:
            return True

    def check_defeat_state(self):
        image: Image = Screen.screen_grab([723, 288, 473, 117], "red")
        text: str = tesser.image_to_string(image, config="--psm 6", nice=1)
        text = ''.join([c for c in text.upper() if c in "DEFEAT"])
        if "DEFEAT" in text:
            return True

    def check_pause_state(self):
        image: Image = Screen.screen_grab([870, 15, 175, 65])
        text: str = tesser.image_to_string(image, config="--psm 6", nice=1)
        text = ''.join([c for c in text.upper() if c in "PAUSE"])
        if "PAUSE" in text:
            return True

    def check_leveled_up_state(self):
        image: Image = Screen.screen_grab([827, 534, 276, 105])
        text: str = tesser.image_to_string(image, config="--psm 6", nice=1)
        text = ''.join([c for c in text.upper() if c in "LEVEL UP!"])
        if "LEVEL" in text:
            return True

    def check_insta_state(self):
        image: Image = Screen.screen_grab([764, 647, 389, 56], "yellow")
        text: str = tesser.image_to_string(image, config="--psm 6", nice=1)
        text = ''.join([c for c in text.upper() if c in "INSTA-MONKEY!"])
        if "INSTA-MONKEY!" in text:
            return True

    def check_current_round_standard(self):
        image: Image = Screen.screen_grab([1380, 30, 180, 45])
        text: str = tesser.image_to_string(image, config=f"-c tessedit_char_whitelist=0123456789/ --psm 6", nice=1)
        text = ''.join([c for c in text if c in "0123456789/"])

        return text.split('/')[0] if len(str(text)) > 0 else None

    def check_current_round_freeplay(self):
        image: Image = Screen.screen_grab([1464, 28, 101, 45])
        text: str = tesser.image_to_string(image, config=f"-c tessedit_char_whitelist=0123456789/ --psm 6", nice=1)
        text = ''.join([c for c in text if c in "0123456789"])

        return text if len(str(text)) > 0 else None

    def check_current_state(self):
        if self.check_victory_state():
            return GameState.VICTORY
        if self.check_defeat_state():
            return GameState.DEFEAT
        if self.check_pause_state():
            return GameState.PAUSED
        if self.check_insta_state():
            return GameState.INSTA
        if self.check_leveled_up_state():
            return GameState.LEVELUP

    def currend_round(self, isFreeplay: bool):
        if isFreeplay:
            return self.check_current_round_freeplay()
        else:
            return self.check_current_round_standard()
