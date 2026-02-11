'''
A class to store the labjack events and functions that are controlled from the 
frontend. 
'''

import numpy as np
import ctypes
from multiprocessing import Queue, Array, Value
from utils.constants import PLOT_CONSTANTS
from models.LabjackProcess import LabJackDataStream
# from models.FlipDetection import FlipDetection
import wx
from models.Warnings import Warning
from utils.logger import get_logger
logger = get_logger("./models/LabjackFrontend") 

 


class LabjackFrontend():
    def __init__(self, array_length, ctrl_panel, timer, args, button_pressed, press_count, hardware_test):
        
        self.constants = []
        #getting labjack constants
        # print(f"args: {args[1]}")
             
        self.button_pressed = button_pressed #Value(ctypes.c_bool, False)
        self.labjack_list = [item for item in list(args[1]) if item not in self.constants] #list(args[1])
        self.hardware = [item for item in list(args[0]) if item not in PLOT_CONSTANTS] #list(args[0])
        self.hardware_indices=[Value(ctypes.c_int, -1), Value(ctypes.c_int, -1), Value(ctypes.c_int, -1)]
        self.prev_graph_list = [-1, -1, -1]
        self.digital_list = []
        self.analog_list = []
        self.button_list = []
        self.extended_list = []
        self.array_length = array_length
        for index, item in enumerate(self.labjack_list):
            if "F" in item:
                self.digital_list.append(int(item[-1]))
                logger.debug(f"hardware: {self.hardware[index]}")
                if "Button" in self.hardware[index]:
                    self.button_list.append(int(item[-1])) 
            else:
                self.analog_list.append(item)
        self.inputs_list = [self.analog_list, self.digital_list]     
        self.labjack_arr = Array('d', array_length*(len(self.hardware_indices)+3))
        self.labjack_queue = Queue()
        self.labjack_is_csv  = Value(ctypes.c_bool, False)
        self.stream_started = Value(ctypes.c_bool, False)
        self.labjack_is_finished = Value(ctypes.c_bool, True)
        self.scan_rate = Value(ctypes.c_float, 0)
        self.hardware_test = hardware_test
        self.graph_panel = ctrl_panel
        self.labjack_choices = self.graph_panel.get_choices()
        self.labjack_timer = timer
        self.press_count = press_count
        logger.debug(f"button {self.button_list}")
        self.graph_panel.set_constants(self.constants)
        for choice in self.labjack_choices:
            choice.Bind(wx.EVT_CHOICE, self._update_graph_list)
        self.serial_state = 0
        self.serial_bool = False
        self.ser_success = False


    def labjack_stream(self, event):
        labjack_button, junk = self.graph_panel.getHandles()
        if labjack_button.GetValue():
            labjack_button.SetLabel("Stop Labjack")
            self.stop_labjack()
            self.start_labjack()
        else:
            self.stop_labjack()
            labjack_button.SetLabel("Stream Labjack")
            labjack_button.SetValue(False)
       
    def update_hardware(self,hardware_lists):
        self.all_hardware = hardware_lists
        self.graph_panel.update_hardware(hardware_lists)
        self.constant_index = []
        self.constants = []
        if list(hardware_lists[1]):
            for index, constant in enumerate(PLOT_CONSTANTS):
                hardware_index = list(hardware_lists[0]).index(constant)
                self.constants.append(hardware_lists[1][hardware_index])
                self.constant_index.append(hardware_index)
               
        self.labjack_list = [item for item in list(hardware_lists[1]) if item not in self.constants] #list(args[1])
        self.hardware = [item for item in list(hardware_lists[0]) if item not in PLOT_CONSTANTS] #list(args[0])
        self.labjack_list = self.all_hardware[1]
        self.hardware = self.all_hardware[0]      
        # self.labjack_list = list(hardware_lists[1])
        # self.hardware = list(hardware_lists[0])
        self.digital_list = []
        self.analog_list = []
        self.button_list = []
        self.extended_list = []
        for index, item in enumerate(list(self.all_hardware[1])):
            if "F" in item:
                self.digital_list.append(int(item[-1]))
                logger.debug(f"hardware: {self.all_hardware[1][index]}")
                if "Button" in self.all_hardware[0][index]:
                    self.button_list.append((int(item[-1]), "f")) 
            elif "E" in item:
                self.extended_list.append(int(item[-1]))
                if "Button" in self.all_hardware[0][index]:
                    self.button_list.append((int(item[-1]), "e")) 
            else:
                self.analog_list.append(item)
        self.inputs_list = [self.analog_list, self.digital_list, self.extended_list]     
        logger.debug(self.button_list)
        self._update_graph_list('')
        
        
    def start_labjack(self):
        if not self.labjack_is_finished.value:
            logger.info("labjack is currently runninng")
            return True
        self.scan_rate.value = 0
        self.labjack_is_finished.value = False
        self.labjack_process = LabJackDataStream(self.array_length, 
                                                 self.labjack_is_finished,
                                                 self.labjack_arr, 
                                                 self.labjack_is_csv, 
                                                 self.labjack_queue,
                                                 self.labjack_list,
                                                 self.hardware_indices,
                                                 self.button_pressed,
                                                 self.inputs_list,
                                                 self.button_list,
                                                 self.press_count,
                                                 self.constant_index,
                                                 self.all_hardware[3],
                                                 self.stream_started,
                                                 self.scan_rate)
        if self.labjack_process.is_successful():
            
            self.labjack_process.start()
            self.labjack_timer.Start(200)
            return True

        else:
            Warning("labjack").display()
            labjack_button, junk = self.graph_panel.getHandles()
            labjack_button.SetValue(False)
            return False
        


    def stop_labjack(self):
        # print(self.labjack_process.actualscanRate)
        # labjack_rate = self.labjack_process.actualscanRate
        self.labjack_is_finished.value = True
        self.labjack_is_csv.value = False
        self.stream_started.value = False
        # print(labjack_rate, "Process rate")
        self.labjack_timer.Stop()
        for index, lj_input in enumerate(self.hardware_indices):
            self.graph_panel.update_yaxis([np.nan]*self.array_length, index, lj_input.value)
        # print(f"constants: {self.constant_index}")
        # print(self.constants)
        for index, constant_inputs in enumerate(self.constants):
            
            self.graph_panel.update_constants([np.nan]*self.array_length, index, self.constant_index[index])
        new_arr = np.empty(80000*(len(self.hardware_indices)+3))

        new_arr.fill(np.nan)
        
        np.frombuffer(self.labjack_arr.get_obj(), dtype=ctypes.c_double).reshape(len(new_arr.flatten()))[:] = new_arr.flatten()
        self.graph_panel.draw()
        try:
            self.labjack_process.join()
        except:
            logger.info("No open Labjack process")
        logger.info('labjack_stopped')
        return self.scan_rate.value

    def labjack_event(self, event):

        if not self.labjack_is_finished.value and self.stream_started.value:

            arr_step = 0
            y_plot_points = np.frombuffer(self.labjack_arr.get_obj(), 'd', len(self.labjack_arr))
            # print(np.isnan(y_plot_points[-1]))
            if not np.isnan(y_plot_points[-1]) and self.serial_bool:
                self.serial_state += 1
                # print(self.serial_state)
                if self.ser_success and self.serial_state > 0:
                    # while not self.lj.is_ready:
                    #     time.sleep(0.1)
                    # msg = f"P{self.date_string}_{self.user_cfg['unitRef']}_{self.sess_string}x"
                    self.ser.write(self.msg.encode())
                    # time.sleep(1)
                    self.ser_success = False
                    self.serial_bool = False
            
                
            # print('here-2')
            # print(y_plot_points[0], " ", y_plot_points[-1])
            if not self.hardware_test.value:
                for index, lj_input in enumerate(self.hardware_indices):
                    # print("here-1")   
                    
                    # print(lj_input.value, "plot: ", y_plot_points[arr_step], " ", y_plot_points[self.array_length-1])
                    if lj_input.value == -1:
                        # print("here")
                        # self.graph_panel.set_visible(index, is_visible=False)
                        self.graph_panel.update_yaxis([np.nan]*self.array_length, index, lj_input.value)
                        y_plot_points[arr_step:arr_step+self.array_length] = np.nan
                        arr_step+= self.array_length
                        # print(f"input: {lj_input.value}")
                        self.graph_panel.set_visible(index, False)
                    else:
                        # print("here1")
                        # print(f"input: {lj_input.value}")
                        # print(f"prev : {self.prev_graph_list[index]}")
                        if lj_input.value != self.prev_graph_list[index]:
                            # self.graph_panel.update_min_max(index, lj_input.value)
                            self.prev_graph_list[index] = lj_input.value
                            y_plot_points[arr_step:arr_step+self.array_length] = np.nan
                            self.graph_panel.update_yaxis([np.nan]*self.array_length, index, lj_input.value)
                            # logger.debug(f"Prev: {self.prev_graph_list}")
                        # print("here2")
                        self.graph_panel.update_yaxis(y_plot_points[arr_step:arr_step+self.array_length], index, lj_input.value)
                        self.graph_panel.set_visible(index)
                        arr_step+= self.array_length
                        # print("here3")
                # print("constants", self.constants)
                # print("arrStep: ",self.arr_step)
            else:
                for index, lj_input in enumerate(self.hardware_indices):
                    self.graph_panel.set_visible(index, False)
                arr_step = self.array_length*len(self.hardware_indices)
                # print("hardwareStep: ", self.arr_step)
            for index, constants_input in enumerate(self.constants):
                # print("here4")
                # print(arr_step)
                # self.prev_graph_list[index] = constants_input
                # y_plot_points[arr_step:arr_step+self.array_length] = np.nan
                # self.graph_panel.update_constants([np.nan]*self.array_length, index, self.constant_index[index])
                # print(self.constant_index[index], "plot: ", y_plot_points[arr_step], " ", y_plot_points[self.array_length-1])
                self.graph_panel.update_constants(y_plot_points[arr_step:arr_step+self.array_length], index, self.constant_index[index])
                self.graph_panel.set_visible_const(index)
                arr_step+= self.array_length
            # print('here5')
            np.frombuffer(self.labjack_arr.get_obj(), dtype=ctypes.c_double).reshape(len(y_plot_points.flatten()))[:] = y_plot_points.flatten()
            
            self.graph_panel.draw()

        
    def add_csv(self, labjack_file, ser_success, ser, msg):
        self.labjack_csv = labjack_file
        self.labjack_queue.put(labjack_file)
        self.labjack_is_csv.value = True
        
        self.serial_state = 0
        self.serial_bool = True
        self.ser_success = ser_success
        self.ser = ser
        self.msg = msg
        
        
    def is_active(self):
        return not self.labjack_is_finished.value
    
    def _update_graph_list(self, event):
        selected_list = []

        for choice in self.labjack_choices:
            if choice.GetSelection() !=-1 and choice.GetSelection() !=0:
                selection = choice.GetSelection()
                choices =  choice.GetStrings()
                selection = choices[selection]
                original_selection = self.hardware.index(selection)
                selected_list.append(original_selection)
        for index, choice in enumerate(self.labjack_choices):
            try:
                selection = choice.GetSelection() if choice.GetSelection() != 0 else -1
                if selection != -1:
                    choices =  choice.GetStrings()
                    selection = choices[selection]
                    original_selection = self.hardware.index(selection)
                    # print(f"choice: {choice}, original_selection: {original_selection}")
                else:
                    original_selection = -1
                new_options = [hardware for index, hardware in enumerate(self.hardware) if index not in selected_list or index == original_selection]
                new_options.insert(0, " ")
                choice.SetItems(new_options)
                
                if selection !=-1:
                    choice.SetSelection(new_options.index(selection))
                #set the balue to all hardware list
                self.hardware_indices[index].value = original_selection
            except Exception as e:
                logger.error(e)
    