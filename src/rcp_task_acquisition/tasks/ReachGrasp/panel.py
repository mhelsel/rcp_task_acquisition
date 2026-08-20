# -*- coding: utf-8 -*-
import wx

from rcp_task_acquisition.panels.TrialPanel import TrialPanel



class ReachGraspPanel(TrialPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.reach_hand = None
        self.grasp_object = None
        self.type = None
        
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        vertical_sizer.Add(self._setup_reachgrasp(), 0, wx.ALIGN_LEFT | wx.ALL, self.border)
        self.SetSizer(vertical_sizer)
        
        
    def _setup_reachgrasp(self):
        self.trial_text = wx.StaticText(self, label="Trial # 1")
        
        self.hand_text = wx.StaticText(self, label='Hand to use:')
        self.left_radio = wx.RadioButton(self, label="Left Hand", style= wx.RB_GROUP)
        self.right_radio = wx.RadioButton(self, label="Right Hand")
        self.right_radio.SetValue(True)
        self.object_text = wx.StaticText(self, label='Grasp apparatus:')
        self.large_object_radio = wx.RadioButton(self, label="Large", style= wx.RB_GROUP)
        self.precision_object_radio = wx.RadioButton(self, label="Precision")
        
        self.type_text = wx.StaticText(self, label='Grasp type:')
        self.grasp_radio = wx.RadioButton(self, label="Grasp", style= wx.RB_GROUP)
        self.pinch_radio = wx.RadioButton(self, label="Poke")
        
        self.seconds_text = wx.StaticText(self, label= "Time: 0 mins, 0 secs")
        self.reaches_text = wx.StaticText(self, label= "Reaches completed in Block: 0")
        self.continue_button = wx.ToggleButton(self, label="Begin Trial", size=(self.button_width*2, -1))
        # self.threshold_button = wx.ToggleButton(self, label="Bypass Grasp Threshold", size=(self.button_width*2, -1))
        # self.threshold_button.Enable(False)
        
        grid_sizer = wx.GridBagSizer(8, 4)
        grid_sizer.Add(self.trial_text, pos=(0, 0), span=(0,4), flag=wx.ALIGN_LEFT | wx.ALL, border=self.border)
        grid_sizer.Add(self.hand_text, pos=(1, 0), span=(0,1), flag=wx.ALIGN_LEFT | wx.ALL, border=self.border)
        grid_sizer.Add(self.left_radio, pos=(1, 1), span=(0,1), flag=wx.ALIGN_LEFT | wx.ALL, border=self.border)
        grid_sizer.Add(self.right_radio, pos=(1, 2), span=(0,1), flag=wx.ALIGN_LEFT  | wx.ALL, border=self.border)
        grid_sizer.Add(self.object_text, pos=(2, 0), span=(0,1), flag=wx.ALIGN_LEFT | wx.ALL, border=self.border)
        grid_sizer.Add(self.large_object_radio, pos=(2, 1), span=(0,1), flag=wx.ALIGN_LEFT | wx.ALL, border=self.border)
        grid_sizer.Add(self.precision_object_radio, pos=(2, 2), span=(0,1), flag=wx.ALIGN_LEFT  | wx.ALL, border=self.border)
        grid_sizer.Add(self.type_text, pos=(3, 0), span=(0,1), flag=wx.ALIGN_LEFT | wx.ALL, border=self.border)
        grid_sizer.Add(self.grasp_radio, pos=(3, 1), span=(0,1), flag=wx.ALIGN_LEFT | wx.ALL, border=self.border)
        grid_sizer.Add(self.pinch_radio, pos=(3, 2), span=(0,1), flag=wx.ALIGN_LEFT  | wx.ALL, border=self.border)
        grid_sizer.Add(self.seconds_text, pos=(4, 0), span=(0,1), flag=wx.ALIGN_LEFT | wx.ALL, border=self.border)
        grid_sizer.Add(self.reaches_text, pos=(4, 1), span=(0,2), flag=wx.ALIGN_LEFT | wx.ALL, border=self.border)
        grid_sizer.Add(self.continue_button, pos=(5, 0), span=(0,2), flag=wx.ALIGN_LEFT | wx.ALL, border=self.border)
        # grid_sizer.Add(self.threshold_button, pos=(5, 1), span=(0,3), flag=wx.ALIGN_LEFT | wx.ALL, border=self.border)
        return grid_sizer
    
    def add_count(self, grasp_count):
        self.grasp_count = grasp_count
    
    def run_trial(self, number):
        self.seconds = 0
        self.left_radio.Enable(False)
        self.right_radio.Enable(False)
        self.hand_text.Enable(False)
        self.object_text.Enable(False)
        self.large_object_radio.Enable(False)
        self.precision_object_radio.Enable(False)
        self.type_text.Enable(False)
        self.grasp_radio.Enable(False)
        self.pinch_radio.Enable(False)
        self.trial_text.SetLabel(f"Trial # {number}")
        self.trial_is_active = True
    
    
    def continue_event(self, event):
        self.rest_timer.Stop()
    
        
    def get_result(self):
        self.grasp_object = "Large" if self.large_object_radio.GetValue() else "Precision"
        self.reach_hand = "Left" if self.left_radio.GetValue() else "Right"
        self.type = "Grasp" if self.grasp_radio.GetValue() else "Poke"
        return self.reach_hand,self.grasp_object, self.type#, self.pace
    
    
    def cancel_event(self, event):
        self.cancel = True
        self.rest_timer.Stop()
    

    def reset(self, number):
        self.seconds = 5
        self.grasp_count.value = 0
        self.left_radio.Enable(True)
        self.right_radio.Enable(True)
        self.hand_text.Enable(True)
        self.object_text.Enable(True)
        self.large_object_radio.Enable(True)
        self.precision_object_radio.Enable(True)
        self.type_text.Enable(True)
        self.grasp_radio.Enable(True)
        self.pinch_radio.Enable(True)
        self.seconds_text.SetLabel("Time: 0 mins, 0 secs")
        self.reaches_text.SetLabel("Reaches completed in Block: 0")
        self.continue_button.SetValue(False)
        self.continue_button.SetLabel("Begin Trial")
        self.trial_text.SetLabel(f"Trial # {number+1}")    

        
    def on_timer(self, event):
        if self.trial_is_active:
            self.seconds+=1
            self.display_mins = int(self.timer.value/60)
            self.display_secs = self.timer.value%60
            
            self.seconds_text.SetLabel(f"Time: {self.display_mins} mins, {self.display_secs} secs")
            self.reaches_text.SetLabel(f"Reaches completed in Block: {self.grasp_count.value}")


    def enable_buttons(self, enable):
        super().enable_buttons(enable)  
        
        self.trial_text.Enable(enable)
        self.hand_text.Enable(enable)
        self.left_radio.Enable(enable)
        self.right_radio.Enable(enable)
        self.object_text.Enable(enable)
        self.large_object_radio.Enable(enable)
        self.precision_object_radio.Enable(enable)
        self.type_text.Enable(enable)
        self.grasp_radio.Enable(enable)
        self.pinch_radio.Enable(enable)
        self.seconds_text.Enable(enable)
        self.reaches_text.Enable(enable)
       
        
    # def trial_buttons(self):
    #     self.left_radio.Enable(False)
    #     self.right_radio.Enable(False)
    #     self.hand_text.Enable(False)
    #     self.object_text.Enable(False)
    #     self.large_object_radio.Enable(False)
    #     self.precision_object_radio.Enable(False)
    #     self.type_text.Enable(False)
    #     self.grasp_radio.Enable(False)
    #     self.pinch_radio.Enable(False)
        
        