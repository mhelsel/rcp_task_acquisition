# -*- coding: utf-8 -*-

import wx
# from utils.logging import logger
from datetime import datetime
from panels.TrialPanel import TrialPanel
import logging
# Get a logger instance (or the root logger)
logger = logging.getLogger(__name__) # Or logging.getLogger() for the root logger
logger.setLevel(logging.DEBUG)


class VowelSpacePanel(TrialPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tap_hand = None
        self.repeat = True
        self.seconds = 0
        self.trial_number = 0
        self.timestamps ={}
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        vertical_sizer.Add(self._setup_vs(), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        self.SetSizerAndFit(vertical_sizer)
        
        self.rest_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.rest_timer)

        
    def _setup_vs(self):
        self.trial_text = wx.StaticText(self, label="Trial # 1")
        self.current_text = wx.StaticText(self, label="")
        self.current_text.Wrap(299)
        # self.current_text.Hide()
        # self.seconds_text = wx.StaticText(self, label= "Trial Time: 0 secs")
        
        self.finish_text = wx.StaticText(self, label="")
        
        self.finish_text.Wrap(299)
        # self.seconds_text.SetLabel(f"Time: {self.seconds} secs")
        # 
        self.continue_button = wx.ToggleButton(self, label="Begin Trial")
        # self.continue_button.Bind(wx.EVT_BUTTON, self.continue_event)
        # self.continue_button.Enable(False)
        
        self.repeat_trial = wx.ToggleButton(self, label="Repeat Trial")
        # self.repeat_trial.Bind(wx.EVT_TOGGLEBUTTON, self.repeat_event)
        self.repeat_trial.Enable(False)
        grid_sizer = wx.GridBagSizer(5, 6)
        
        grid_sizer.Add(self.trial_text, pos=(0, 0), span=(0,6), flag=wx.ALIGN_LEFT | wx.ALL, border=5)
        grid_sizer.Add(self.current_text, pos=(1, 0), span=(0,6), flag=wx.ALIGN_LEFT  | wx.ALL, border=5)
        
        grid_sizer.Add(self.finish_text, pos=(2, 0), span=(0,6), flag=wx.ALIGN_LEFT | wx.ALL, border=5)
        grid_sizer.Add(self.repeat_trial, pos=(3,0), span=(0,2), flag=wx.ALIGN_LEFT  | wx.TOP, border=5)  
        grid_sizer.Add(self.continue_button, pos=(3,2), span=(0,2), flag=wx.ALIGN_LEFT  | wx.TOP, border=5)  
        return grid_sizer
    
    
    def continue_event(self, event):
        self.rest_timer.Stop()
        self.continue_button.SetValue(True)
        self.repeat_trial.Enable(False)
        # self.EndModal(wx.ID_OK)
        # self.timestamps[f'{date1time.utcnow().strftime("%Y%m%d%H%M%S")}Z'] = "next_trial_selected"
    

    def is_finish(self):
        # self.continue_button.Enable(False)
        # self.repeat_trial.Enable(False)
        self.finish_text.SetLabel("Task Finished! Press End Task to continue.")
    
        
        
    def repeat_event(self):
        self.repeat= True
        
        self.rest_timer.Stop()
        self.continue_button.SetValue(True)
        
        self.repeat_trial.Enable(False)
        pass
        # self.timestamps[f'{datetime.utcnow().strftime("%Y%m%d%H%M%S")}Z'] = "repeats_selected"
        # self.cancel = True
        # self.rest_timer.Stop()
        # self.EndModal(wx.YES_DEFAULT)
    
    def run_trial(self, number):
        # self.trial_text.SetLabel(f"Trial # {number}")
        pass
    
    
    # def destroy(self):
    #     self.Destroy()
    
    def end_event(self, event):
        # self.timestamps[f'{datetime.utcnow().strftime("%Y%m%d%H%M%S")}Z'] = "finish_selected"
        self.cancel = True
        # self.rest_timer.Stop()
        # self.EndModal(wx.CANCEL)
    
    def reset(self, number):
        self.timestamps = {}
        # self.seconds_text.SetLabel(f"Trial Time: {self.seconds} secs")
        # self.current_text.SetLabel(f"Say {prompt} again")
        # self.continues_button.Enable(False)
        
        # self.trial_text.SetLabel(f"Trial # {number}")
        # self.repeat_button.Enable(True)
    
    def on_timer(self, event):
        self.seconds+=1
        # self.seconds_text.SetLabel(f"Time: {self.seconds} secs")
        # if self.seconds > 60:
        #     self.continue_button.Enable(True)

        
    def update_trial(self, trial, syllable):
        # self.current_text.Show()
        self.current_text.SetLabel(f"Say {syllable} again")
        self.trial_text.SetLabel(f"Trial # {trial}")
            
    
