from psychopy import core, sound #, visual
from . import bases
# from utils.logging import logger
from  utils.stimulus_utils import thread_event
import logging
# Get a logger instance (or the root logger)
logger = logging.getLogger(__name__) # Or logging.getLogger() for the root logger
logger.setLevel(logging.DEBUG)



class HardwareTest(bases.StimulusBase):
    def __init__(self, window, is_finished, frame, video_status):
        super().__init__(window, frame, video_status)
        self.finish = is_finished
        self.flash_time = 5
        
        
    def present(self):
        self.display.switch_patch()
        self.display.draw_patch()
        self.display.flip()
        clock = core.Clock()   
        while True:
            
            while clock.getTime() < self.flash_time:
                self.display.draw_patch()
                self.display.flip()
                if self.finish.value == 2:
                    print(self.finish.value)
                    self.display.switch_patch()
                    self.display.draw_patch()
                    self.display.flip()
                    self.finish.value = 0
                    return
            clock.reset(0)
            self.display.switch_patch()
            self.display.draw_patch()
            while clock.getTime() < self.flash_time:
                self.display.flip()
                if self.finish.value == 2:
                    self.finish.value = 0
                    return
            self.display.switch_patch()
            clock.reset()

        
    def saveMetadata(self, name, sessionFolder):
        pass
            