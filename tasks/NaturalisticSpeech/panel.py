# -*- coding: utf-8 -*-

import wx
from datetime import datetime
import os
from panels.TrialPanel import TrialPanel
import tasks.NaturalisticSpeech.constants as c
from utils.logger import get_logger
logger = get_logger("./panels/NaturalisticSpeechPanel") 


class NaturalisticSpeechPanel(TrialPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.seconds = 0
        self.display_secs = 0
        self.display_mins = 0
        self.trial_number = 1
        self.timestamps ={}
        self.countdown_start = 0
        self.button_width = 76
        self.border = 5
        self.photo = None
        # self.run_trial = False
        
        
        wx.Panel.__init__(self, parent, -1, size=wx.Size(-1,-1))
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        vertical_sizer.Add(self._set_up_photo(), 0, wx.ALIGN_LEFT | wx.ALL, self.border)
        self.SetSizer(vertical_sizer)
        self.rest_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.rest_timer)

     

    def _set_up_photo(self):
        '''
        Set up the naturalistic speech panel
        Returns:
            message (wx dialog panel)

        '''
        self.trial_text = wx.StaticText(self, label="Trial # 1")

        self.adult_image_path = os.path.join(c.IMG_DIR, c.ADULT_IMG)
        adult_image = wx.Image(self.adult_image_path, wx.BITMAP_TYPE_ANY)
        adult_image = adult_image.Scale(150, 150)
        bitmap = adult_image.ConvertToBitmap()
        # Create a StaticBitmap to display the image
        self.adult_bitmap = wx.StaticBitmap(self, wx.ID_ANY, bitmap)

        self.child_image_path = os.path.join(c.IMG_DIR, c.CHILD_IMG)
        child_image = wx.Image(self.child_image_path, wx.BITMAP_TYPE_ANY)
        child_image = child_image.Scale(150, 150)
        bitmap = child_image.ConvertToBitmap()
        # Create a StaticBitmap to display the image
        self.child_bitmap = wx.StaticBitmap(self, wx.ID_ANY, bitmap)



        
        photo_text = wx.StaticText(self, label='Choose which photo to show:')
        self.adult_button = wx.RadioButton(self, label="Resort", name=c.ADULT_IMG,  size=(150, -1))
        # self.child_button.Bind(wx.EVT_RADIOBUTTON, self.continue_event)

        self.child_button = wx.RadioButton(self, label="Park", name=c.CHILD_IMG, size=(150, -1))
        # self.adult_button.Bind(wx.EVT_RADIOBUTTON, self.continue_event)
        self.seconds_text = wx.StaticText(self, label= "Time: 0 mins, 0 secs")
        # self.cancel_button = wx.Button(message, label="Exit", size=(150, -1))
        # self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel_event)

        grid_sizer = wx.GridBagSizer(5, 4)

        grid_sizer.Add(photo_text, pos=(0, 0), span=(0, 4),flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=10)
        
        grid_sizer.Add(self.trial_text, pos=(1, 0), span=(0,4), flag=wx.ALIGN_LEFT | wx.ALL, border=self.border)
        self.continue_button = wx.ToggleButton(self, label="Begin Trial", size=(self.button_width*2, -1))
        grid_sizer.Add(self.adult_bitmap, pos=(2, 0), span=(0, 2),  flag=wx.ALIGN_LEFT | wx.ALL, border=10)
        grid_sizer.Add(self.child_bitmap, pos=(2, 2), span=(0, 2),  flag=wx.ALIGN_LEFT | wx.ALL, border=10)
        grid_sizer.Add(self.adult_button, pos=(3, 0), span=(0, 2), flag=wx.ALIGN_LEFT |  wx.ALL, border=10)
        grid_sizer.Add(self.child_button, pos=(3, 2), span=(0, 2), flag=wx.ALIGN_LEFT |  wx.ALL, border=10)
        
        grid_sizer.Add(self.seconds_text, pos=(4, 0), span=(0, 4), flag=wx.ALIGN_LEFT |  wx.ALL, border=10)
        grid_sizer.Add(self.continue_button, pos=(5, 0), span=(0, 4), flag=wx.ALIGN_LEFT | wx.ALL, border=10)
        

        return grid_sizer


    def run_trial_(self, number):
        self.seconds = 0
        self.trial_number = number
        
        self.trial_is_active = True
        self.child_button.Enable(False)
        self.adult_button.Enable(False)
        self.child_bitmap.Enable(False)
        self.adult_bitmap.Enable(False)
        self.trial_text.SetLabel(f"Trial # {self.trial_number}")


    def update_trial(self, number):
        self.trial_number = number
        self.trial_text.SetLabel(f"Trial # {self.trial_number}")
        
    def get_result(self):
        self.photo = self.child_image_path if self.child_button.GetValue() else self.adult_image_path
        print(self.photo)
        return self.photo, self.trial_number

    
    def reset(self, number):
        self.seconds = 0
        self.trial_number = number
        self.trial_is_active = False
        self.seconds_text.SetLabel(f"Time: 0 mins, 0 secs")
        self.child_button.Enable(True)
        self.adult_button.Enable(True)
        self.child_bitmap.Enable(True)
        self.adult_bitmap.Enable(True)
        self.trial_text.SetLabel(f"Trial # {self.trial_number}")
    

    def on_timer(self, event):
        self.seconds+=1
        self.display_mins = int(self.seconds/60)
        self.display_secs = self.seconds%60
        if self.trial_is_active:
            self.seconds_text.SetLabel(f"Time: {self.display_mins} mins, {self.display_secs} secs")
