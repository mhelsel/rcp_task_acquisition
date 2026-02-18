from psychopy import core, sound #, visual
from tasks import bases
# from utils.logging import logger
from  utils.stimulus_utils import thread_event
import logging
# Get a logger instance (or the root logger)
logger = logging.getLogger(__name__) # Or logging.getLogger() for the root logger
logger.setLevel(logging.DEBUG)


# Parameters
PARAMS = {
    "number_of_trials": 0,
    "hand_used": {},
    "grasp_object": {}
    }


class ReachGrasp(bases.StimulusBase):
    def __init__(self, window, frame, show_panel):
        super().__init__(window, frame)
        self.show_panel = show_panel
        self.trial_count = 0
        self.hand = None
        self.grasp_object = None
        
    def present(self):        
        self.trial_count+=1
        PARAMS["hand_used"][f"trial_{self.trial_count}"] = self.hand
        PARAMS["grasp_object"][f"trial_{self.trial_count}"] = self.grasp_object
        self.play_tone()
        self.display.switch_patch()
        self.display.draw_patch()
        self.display.flip()


        thread_event.wait()
        thread_event.clear()
        

        self.display.switch_patch()
        self.display.draw_patch()
        self.display.flip()        
        self.play_tone()

        
        
    def update_values(self, hand, grasp_object):
        self.hand = hand    
        self.grasp_object = grasp_object   
                 
        
    def saveMetadata(self, name, sessionFolder):
        PARAMS["number_of_trials"] = self.trial_count
        return PARAMS
            
            