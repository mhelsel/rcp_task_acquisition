# -*- coding: utf-8 -*-

from psychopy import core #, visual
from tasks import bases
# from utils.logging import logger
from  utils.stimulus_utils import thread_event
import json
import logging
# Get a logger instance (or the root logger)
logger = logging.getLogger(__name__) # Or logging.getLogger() for the root logger
logger.setLevel(logging.DEBUG)
import numpy as np

PHRASE_LIST = ["hod", "heed", "who'd", "hoad"]
# Parameters
PARAMS = {
    "trial_number": 20,
    "trial_data": [],
    "actual_data": {}
    }

# shorter name for the global clock
GLOBAL_CLOCK = core.monotonicClock


class VowelSpace(bases.StimulusBase):
    def __init__(self, window, frame, show_panel):
        super().__init__(window, frame)
        self.show_panel = show_panel
        
        self.create_trial_data()
        self.trial = 0
        self.trial_name = ""
        self.finish = False
        
    def present(self):
        # self.create_trial_data()
        # print(PARAMS["trial_data"])
        
        # if self.trial >= PARAMS["trial_number"]:
        #     self.create_trial_data()
        #     print(PARAMS["trial_data"])
        #     self.trial = 0
        
        # while trial < 
        # for index, word in enumerate(PARAMS["trial_data"]):
        # self.play_tone()
        self.play_tone()
        self.display.switch_patch()
        self.display.draw_patch()
        self.display.flip()
        self.trial_name =str(PARAMS["trial_data"][self.trial])
        
        # print(type(self.trial_name))
        # PARAMS["actual_data"].append(str(self.trial_name))
        # self.show_panel.value=True
        thread_event.wait()
        thread_event.clear()
        
        PARAMS["actual_data"][f"trial_{self.trial+1}"] = str(self.trial_name)
        if self.trial >= PARAMS["trial_number"]-1:
            self.finish = True
            self.create_trial_data()
            # print(PARAMS["trial_data"])
            self.trial = -1
        self.display.switch_patch()
        self.display.draw_patch()
        self.display.flip()
        # self.show_panel.value = False


    def get_trial(self):
        if self.trial >= PARAMS["trial_number"]-1:
            self.finish=True
        return self.trial+1, PARAMS["trial_data"][self.trial], self.finish
    
    def update_trial(self):
        self.trial+=1
        if self.trial >= PARAMS["trial_number"]:
            self.finish = True
            self.create_trial_data()
            print(PARAMS["trial_data"])
            self.trial = 0
        
    def create_trial_data(self):
        num_repeats = int(PARAMS["trial_number"]/len(PHRASE_LIST))
        print(num_repeats)
        trials = np.tile(PHRASE_LIST, num_repeats)
        np.random.shuffle(trials)
        print(trials)
        PARAMS["trial_data"] =trials.tolist()

    def saveMetadata(self, name, sessionFolder):
        
        return PARAMS

