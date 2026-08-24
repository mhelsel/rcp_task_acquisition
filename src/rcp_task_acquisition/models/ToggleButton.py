# -*- coding: utf-8 -*-
import wx

class ToggleButton(wx.ToggleButton):
    def __init__(self, parent, id, label, size):
        super().__init__(parent, 
                         id=id,
                         label=label,
                         size=size)
        self._is_active = False
        
        
    def update_button(self):
        if self.GetValue():
            self.SetValue(False)
            self._is_active = True
        else:
            self._is_active = False
            
            
    def is_active(self):
        return self._is_active
    
    
    def Enable(self, value: bool):
        print(f"button is enabled: {self._is_active}")
        super().Enable(value)
        if self._is_active:
            self.SetValue(True)
            self._is_active = False
        elif self.GetValue():
            self.SetValue(False)
            self._is_active = True
        else:
            self._is_active = False
    
    def SetValue(self, state):
        super().SetValue(state)
        if not state:
            self._is_active = False
        