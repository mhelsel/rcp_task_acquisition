import wx
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from dataclasses import dataclass
from utils.constants import PLOT_CONSTANTS, LINE_STYLES, COLORS
from utils.logger import get_logger
logger = get_logger("./models/GraphPanel") 

@dataclass
class Input:
    name: str
    labjack: str
    color: str
    is_visible=True


class GraphPanel(wx.Panel):
    def __init__(self, parent, gui_size, hardware, min_max):
        self.hardware= hardware
        self.min_max = min_max
        self.color_index = 0
        self.hardware_indices = [-1] * 3
        wx.Panel.__init__(self, parent, -1,style=wx.SUNKEN_BORDER)
        self.constants =[]
        self.lines = []
        if gui_size[0] > gui_size[1]:
            ctrlsizer = wx.BoxSizer(wx.HORIZONTAL)
        else:
            ctrlsizer = wx.BoxSizer(wx.VERTICAL)
        self.figC = Figure(figsize=(3, 3))
        self.figC.patch.set_facecolor((0.01, 0.01, 0.01))
        
        self.canC = FigureCanvas(self, -1, self.figC)
        ctrlsizer.Add(self.canC, 1, wx.ALL)
        
        setup_axes = self.figC.add_subplot(1, 1, 1)
        setup_axes.set_position((0, 0, 1, 1))
        plot, = setup_axes.plot([0,0,40000,40000,np.nan,40000,80000,80000], [-2,-1.75,-1.75,-2,np.nan,-1.75,-1.75,-2], 'white', lw=1)
        setup_axes.text(0, -4,'0',ha='center', color='white')
        setup_axes.text(40000, -4,'1',ha='center', color='white')
        setup_axes.text(80000, -4,'2',ha='center', color='white')
        setup_axes.text(40000, -6,'Seconds',ha='center', color='white')
        setup_axes.set_ylim([-10,15])
        setup_axes.invert_xaxis()
        
        setup_axes.yaxis.set_visible(False)
        setup_axes.set_frame_on(False)
        self.axes = setup_axes
        
        self.SetSizer(ctrlsizer)
        ctrlsizer.Fit(self)
        self.Layout()
        
        
    def update_hardware(self, hardware):
        
        self.hardware = list(hardware[0])
        self.min_max = list(hardware[2])
        self.voltage = list(hardware[3])
        options = self.hardware
        options.insert(0, " ")
        defaults = ["Microphone 1", "Audio", "Microphone 2"]
        self.default_index = []
        for item in defaults:
            try:
                self.default_index.append(options.index(item))
            except:
                pass
        for choice in self.labjack_choices:
            choice.SetItems(options)
        count = 0
        for index in self.default_index:
            self.labjack_choices[count].SetSelection(index)
            count +=1
            
    
    
    def create_labjack_panel(self, panel):
        wSpace = 5
        button_width = 150
        self.input_checkboxes = []
        labjack_box = wx.StaticBox(panel, label="Labjack Graphing")
        bsizer = wx.StaticBoxSizer(labjack_box, wx.HORIZONTAL)
        labjack_sizer = wx.GridBagSizer(5, 5)
        options = self.hardware
    
        options.insert(0, " ")
        self.labjack_stream_button = wx.ToggleButton(panel, id=wx.ID_ANY, label="Stream Labjack", size=(button_width, -1))
        labjack_sizer.Add(self.labjack_stream_button,pos=(0,0), span=(0,2), flag=wx.ALL, border=wSpace)
        
        # self.default_index = [options.index(item) for item in defaults]
        self.labjack_choices = []
        
        labjack_choice = wx.Choice(panel, id=wx.ID_ANY, choices=options, size=(button_width, -1))
        self.labjack_choices.append(labjack_choice)
        labjack_sizer.Add(labjack_choice, pos=(0,2), span=(0,2), flag=wx.ALL, border=wSpace)
        
        labjack_choice = wx.Choice(panel, id=wx.ID_ANY, choices=options, size=(button_width, -1))
        self.labjack_choices.append(labjack_choice)
        labjack_sizer.Add(labjack_choice, pos=(1,0), span=(0,2), flag=wx.ALL, border=wSpace)
        
        labjack_choice = wx.Choice(panel, id=wx.ID_ANY, choices=options, size=(button_width, -1))
        self.labjack_choices.append(labjack_choice)
        labjack_sizer.Add(labjack_choice, pos=(1,2), span=(0,2), flag=wx.ALL, border=wSpace)

        
        bsizer.Add(labjack_sizer, 1, wx.EXPAND | wx.ALL, 5)
        return bsizer
        
    def set_constants(self, constants):
        self.constant_labels = constants
    
    def plot_constants(self, arr_size):
        '''
        Function to plot the "mandatory" inputs

        Returns
        -------
        None.

        '''
        y_coords = list(np.array([np.nan]*arr_size))
        x_coords = list(np.arange(0, arr_size))
        for index, _ in enumerate(PLOT_CONSTANTS):
            plot, = self.axes.plot(x_coords, y_coords, label=PLOT_CONSTANTS[index], linestyle=LINE_STYLES[index], lw=1)
            # plot.set_visible(False)
            self.color_index+=1
            self.constants.append(plot)
        
            
            
    def update_constants(self, y_points, index, lj_value):
        min_old = float(self.voltage[lj_value][0])#float(self.min_max[lj_value][0])
        max_old = float(self.voltage[lj_value][1])#float(self.min_max[lj_value][1])
        min_new = 8
        max_new = 14
        y_points = np.array(y_points)
        y_points = (((y_points -min_old)* (max_new-min_new))/(max_old - min_old))  +min_new
        # y_points = y_points+5

        self.constants[index].set_ydata(y_points)
    
    def getHandles(self):
        return self.labjack_stream_button, self.labjack_choices
    
    
    def get_choices(self):
        return self.labjack_choices

        
    def set_visible(self,index, is_visible=True):
        self.lines[index].set_visible(is_visible)
        
    def set_visible_const(self,index, is_visible=True):
        self.constants[index].set_visible(is_visible)
        
    def update_yaxis(self, y_points, index, lj_value):
        if index != -1 and lj_value != -1:
            min_old = float(self.voltage[lj_value][0])#float(self.min_max[lj_value][0])
            max_old = float(self.voltage[lj_value][1])#float(self.min_max[lj_value][1])
            min_new = 0
            max_new =7
            y_points = np.array(y_points)
            y_points = (((y_points -min_old)* (max_new-min_new))/(max_old - min_old))  +min_new

            self.lines[index].set_ydata(y_points)


        
    def create_plot(self, arr_size):
        self.lines = []
        self.x_size = arr_size
        y_coords = list(np.array([np.nan]*arr_size))
        x_coords = list(np.arange(0, arr_size))
        for index, lj_input in enumerate(self.hardware_indices):
            plot, = self.axes.plot(x_coords, y_coords, color=COLORS[self.color_index], lw=1)
            
            self.lines.append(plot)
            # self.labjack_choices.SetBackGroundColour(self.color_index)
            self.color_index+=1
        self.plot_constants(arr_size)
        self.axes.legend(loc="upper left", fontsize=8, 
                         edgecolor='black', facecolor=(0.78, 0.78, 0.78))
        for constant in self.constants:
            constant.set_visible(False)
        # self.hardware_test(arr_size)


    def draw(self):
        self.figC.canvas.draw()
         
    def setup_hardware_test(self, panel):
        panel = wx.Panel(panel, -1,style=wx.BORDER_NONE)
        wSpace = 5
        button_width = 150
        self.input_checkboxes = []
        cam_box = wx.StaticBox(panel, label="Camera Tests")
        bsizer = wx.StaticBoxSizer(cam_box, wx.HORIZONTAL)
        cam_sizer = wx.GridBagSizer(1, 4)
        options = self.hardware
    
        options.insert(0, " ")
        self.contrast_test = wx.ToggleButton(panel, id=wx.ID_ANY, label="Test Contrast", size=(button_width, -1))
        
        self.focus_test = wx.ToggleButton(panel, id=wx.ID_ANY, label="Test Focus", size=(button_width, -1))
        # self.default_index = [options.index(item) for item in defaults]

        

        cam_sizer.Add(self.contrast_test, pos=(0,0), span=(0,2), flag=wx.ALL, border=wSpace)
        cam_sizer.Add(self.focus_test, pos=(0,2), span=(0,2), flag=wx.ALL, border=wSpace)
        
        

        
        bsizer.Add(cam_sizer, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(bsizer)
        panel.Fit()
        return panel

    def hardware_test(self, arr_size, cam_num, cam_names):
        for plot in self.lines:
            plot.set_visible(False)
        self.test_lines = []
        for cam in range(cam_num):
            
            x_coords = np.linspace(0, self.x_size, num=arr_size)
            y_coords = list(np.full(arr_size, np.nan))
            # x_coords = list(np.arange(0, arr_size))     
            plot, = self.axes.plot(x_coords, y_coords, lw=1, label=cam_names[cam] )
            self.test_lines.append(plot)
        y_coords = list(np.full(self.x_size, 0.5))
        x_coords = list(np.arange(0, self.x_size))     
        plot, = self.axes.plot(x_coords, y_coords, color="white", lw=1, label="Goal Focus" )
        self.test_focus = plot
        self.test_focus.set_visible(False)


    def plot_hardware(self, cam_vals, max_old, threshold = 0.5):
        self.test_focus.set_visible(True)
        
        # print("here")
        for index, line in enumerate(self.test_lines):
            # x_spacing = self.x_size/len(cam_vals[index])
            # x_vals = np.linspace(0, self.x_size, num=len(cam_vals[index]), endpoint=True)
            # print(x_vals)
            
            min_old = 0
            max_old = max_old
            min_new = 0
            max_new =10
            y_points = np.array(cam_vals[index])
            y_points = (((y_points -min_old)* (max_new-min_new))/(max_old - min_old))  +min_new
            line.set_ydata(y_points)
        # print(cam_vals[0])
        self.draw()


    def remove_hardware(self):
        self.test_focus.set_visible(False)
        
        print("here")
        for index, line in enumerate(self.test_lines):
            line.set_ydata(np.full(60, np.nan))

        self.draw()

















