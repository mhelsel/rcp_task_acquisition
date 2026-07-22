import numpy as np
from psychopy import core, visual
import pyaudio

from rcp_task_acquisition.tasks.ReachGrasp.constants import (MIN_REST_VAL,
                                                             MAX_REST_VAL, 
                                                             TRIALS_PER_BLOCK, 
                                                             GRASP_THRESHOLD,
                                                             CORRECT_IMG,
                                                             INCORRECT_IMG)

from rcp_task_acquisition.tasks import bases
from rcp_task_acquisition.utils.logger import get_logger
logger = get_logger("./tasks/ReachGrasp") 



class ReachGrasp(bases.StimulusBase):

    def __init__(self, base_vars, grasp, grasp_count):
        super().__init__(**base_vars)
        self.timer.value = 0
        self.trial_count = 0
        self.hand = None
        self.grasp_object = None
        self.grasp_ready = grasp[0]
        self.max_value = grasp[1]
        self.rest_time = grasp[2]
        self.grasp_count = grasp_count
        self.trial_dict = {}
        
        
    def present(self):  
        self.timer.value = 0
        self.grasp_count.value = 0
        timing_list = np.linspace(MIN_REST_VAL, MAX_REST_VAL, TRIALS_PER_BLOCK)
        np.random.shuffle(timing_list)
        self.trial_count+=1
        self.trial_dict[f"trial_{self.trial_count}"] = {"hand_used": self.hand,
                                                        "grap_object": self.grasp_object,
                                                        "trial_type": self.type,
                                                        "rest_timings": []
                                                        }
        correct_img = visual.ImageStim(self.display, image=CORRECT_IMG, name="correct", size=[300, 300])
        incorrect_img = visual.ImageStim(self.display, image=INCORRECT_IMG, name="incorrect", size=[300, 300])
       
        self.play_tone()
        self.display.switch_patch()
        self.display.draw_patch()
        self.display.flip()


        gui_clock = core.Clock()
        for rest_value in range(0, TRIALS_PER_BLOCK):
            # if rest_value > 0:
            self.timer.value = int(gui_clock.getTime())
            if self.finish.value == 2:
                self.display.switch_patch()
                self.display.draw_patch()
                self.display.flip()        
                self.play_tone()
                return
        
            self.trial_dict[f"trial_{self.trial_count}"]["rest_timings"].append(timing_list[rest_value])
            #wait to get the ready signal

            while not self.grasp_ready.value:
                self.timer.value = int(gui_clock.getTime())
                if self.finish.value == 2:
                    break
            logger.debug(f"max_value {self.max_value.value}")
            self.grasp_count.value = rest_value#+1
            
            self.timer.value = int(gui_clock.getTime())
            if rest_value > 0:
                if self.max_value.value < GRASP_THRESHOLD:
                    correct_img.draw()
                    self.display.draw_patch()
                    self.display.flip()
                else:
                    incorrect_img.draw()
                    self.display.draw_patch()
                    self.display.flip()
                
            self.timer.value = int(gui_clock.getTime())
            #start countdown once hand is resting
            self.max_value.value = 0
            self.grasp_ready.value = False
            clock = core.Clock() 
            logger.debug(f"rest_time = {self.rest_time.value}")
            while clock.getTime() < timing_list[rest_value]-self.rest_time.value:
                self.timer.value = int(gui_clock.getTime())
                if self.finish.value == 2:
                        self.display.switch_patch()
                        self.display.draw_patch()
                        self.display.flip()        
                        self.play_tone()
                        return
            
            
            self.display.draw_patch()
            self.display.flip()
            #tone to start the reach
            self.play_reach_tone()
            
        #final wait for participant to touch pad before ending the trial
        while not self.grasp_ready.value:
            self.timer.value = int(gui_clock.getTime())
            if self.finish.value == 2:
                break
        
        logger.debug(f"max_value {self.max_value.value}")
        self.grasp_count.value = TRIALS_PER_BLOCK
        final_time = 1.5 #in seconds
        final_image = incorrect_img
        if self.max_value.value < GRASP_THRESHOLD:
            final_image = correct_img
        clock = core.Clock()
        while clock.getTime() < final_time:
            final_image.draw()
            self.display.draw_patch()
            self.display.flip()
                    
        self.display.switch_patch()
        self.display.draw_patch()
        self.display.flip()        
        self.play_tone()
        self.timer.value = 0
        self.grasp_count.value = 0
        self.grasp_ready.value = False

        
        
    def update_data(self, data):
        self.hand = data[0]    
        self.grasp_object = data[1]   
        self.type = data[2]
                 
        
    def saveMetadata(self, name, sessionFolder):       
        return self.trial_dict 
            
    
    def play_reach_tone(self, frequency=500, duration=0.5, sample_rate=44100):
        """
        Generates and plays a sine wave tone.
        """
        try:
            # Generate time values
            t = np.linspace(0, duration, int(sample_rate * duration), False)
    
            # Generate sine wave
            tone = np.sin(frequency * t * 2 * np.pi)
    
            # Normalize to 16-bit range
            audio = ((tone * 32767)*0.1).astype(np.int16)
            
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=sample_rate,
                output=True)
            # Play audio
            stream.write(audio.tobytes())

            # 5. Clean up
            stream.stop_stream()
            stream.close()
            p.terminate()
    
        except Exception as e:
            logger.error(f"Error generating tone: {e}")
            