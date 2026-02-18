# -*- coding: utf-8 -*-
from tasks import bases
import numpy as np
import os
from  utils.stimulus_utils import thread_event
from  tasks.VowelSpace import constants as c
from utils.logger import get_logger
logger = get_logger("./tasks/VowelSpace") 



class VowelSpace(bases.StimulusBase):
    def __init__(self, window, frame, show_panel):
        super().__init__(window, frame)
        self.show_panel = show_panel
        self.trials = None
        self.actual_data = {}
        self.create_trial_data()
        self.trial = 0
        self.trial_name = ""
        self.repeat_num = 0
        self.finish = False
        self.is_updated = True
      
        
    def present(self):
        #check if trial was repeated
        if not self.is_updated:
            self.repeat_num+=1
        self.is_updated = False
        self.trial_name =str(self.trials[self.trial])
        logger.debug(self.trial_name)
        logger.debug(self.trial)
        self.trial_bookends()
        
        self.play_vowel_phrase(str(self.trial_name))

        
        thread_event.wait()
        thread_event.clear()
        
        self.trial_bookends()
        
        self.actual_data[f"trial_{self.trial+1}"] = str(self.trial_name)
        if self.trial >= c.VS_NUM_TRIALS-1+self.repeat_num:
            self.finish = True
            self.create_trial_data()
            self.trial = -1


    def get_trial(self):
        if self.trial >= (c.VS_NUM_TRIALS-1+self.repeat_num):
            self.finish=True
        logger.debug(self.trial_name)
        return self.trial+1, self.trials[self.trial], self.finish
    
    
    def update_trial(self):
        self.trial+=1
        self.is_updated = True
        if self.trial >= c.VS_NUM_TRIALS+self.repeat_num:
            self.finish = True
            self.create_trial_data()
            self.trial = 0
        
        
    def create_trial_data(self):
        num_repeats = int(c.VS_NUM_TRIALS/len(c.PHRASE_LIST))
        trials = np.tile(c.PHRASE_LIST, num_repeats)
        np.random.shuffle(trials)
        self.trials = trials.tolist()


    def saveMetadata(self, name, sessionFolder):
        metadata = { "trial_list": self.trials,
                     "trial_number": c.VS_NUM_TRIALS,
                     "trial_data": self.actual_data
                     }
        return metadata


    def reset_task(self):
        self.trial = 0
        self.finish = False
        self.create_trial_data()


    def play_vowel_phrase(self, trial):
        logger.debug(trial)
        try:
            file = c.VS_PATHS[trial]
            path =  os.path.join(c.STIM_DIR, file)
            os.system(f'play {path} vol {c.VOLUME}')
        except:
            logger.warn("No file, continuing without....")
        

