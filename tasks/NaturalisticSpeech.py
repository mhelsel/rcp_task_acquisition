from psychopy import visual
import os
from . import bases
# from utils.logging import logger
from utils.stimulus_utils import thread_event
import logging
# Get a logger instance (or the root logger)
logger = logging.getLogger(__name__) # Or logging.getLogger() for the root logger
logger.setLevel(logging.DEBUG)


basedir = "/home/rld/task-acquisition/tasks"
imdir = os.path.join(basedir, "PhotoTest_Stimuli")

# Sets up display window, fixation cross, text pages and image stimuli
class NaturalisticSpeech(bases.StimulusBase):
    def __init__(self, window, frame, finish):
        super().__init__(window, frame)
        self.photo = None
        self.photo_dict = {}
        self.finish = finish
        self.trial =0
        
    def present(self, test=True):
        # Load and draw the photo being presented
        if not self.photo:
            logger.warn("No Photo is selected")
            return
        
        self.trial+=1
        logger.debug(self.photo)
        print(self.trial)
        self.photo_dict[f"trial_{self.trial}"] = self.photo
        stim = visual.ImageStim(self.display, image=self.photo, name=self.photo, size=[1200, 1200])
        stim.draw()
        self.play_tone()
        #switch the photodiode patch to be "On" while the photo is being shown
        self.display.switch_patch()
        self.display.draw_patch()
        self.display.flip()
        #wait for "cancel session" button to be pressed in the main gui to stop session
        thread_event.wait()
        thread_event.clear()
        
        #turn the patch to off and flip the display to black
        self.display.switch_patch()
        self.display.draw_patch()
        
    def saveMetadata(self, name, sessionFolder):
        data = {"photo_paths": self.photo_dict}
        return data
    
    
    def update_data(self, trial_data):
        self.photo = trial_data[0]
        # self.trial = trial_data[1]