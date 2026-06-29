<<<<<<< HEAD
from psychopy import core

=======
import numpy as np
from psychopy import core, visual
import pyaudio

from rcp_task_acquisition.tasks.ReachGrasp.constants import (MIN_REST_VAL,
                                                             MAX_REST_VAL, 
                                                             TRIALS_PER_BLOCK, 
                                                             GRASP_THRESHOLD,
                                                             CORRECT_IMG,
                                                             INCORRECT_IMG)
>>>>>>> 7ea9515 (updated reach grasp system)
from rcp_task_acquisition.tasks import bases
from rcp_task_acquisition.utils.logger import get_logger
logger = get_logger("./tasks/ReachGrasp") 



class ReachGrasp(bases.StimulusBase):

    def __init__(self, base_vars):
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
        timing_list = np.linspace(MIN_REST_VAL, MAX_REST_VAL, TRIALS_PER_BLOCK)
        np.random.shuffle(timing_list
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

        # clock = core.Clock()
        # while self.finish.value == 0:
        #     self.display.draw_patch()
        #     self.display.flip()        
        #     self.timer.value = int(clock.getTime())


        for rest_time in range(0, TRIALS_PER_BLOCK):
            if self.finish.value == 2:
                self.display.switch_patch()
                self.display.draw_patch()
                self.display.flip()        
                self.play_tone()
                return
            
            self.trial_dict[f"trial_{self.trial_count}"]["rest_timings"].append(timing_list[rest_time])
            #wait to get the ready signal
            import time
            time.sleep(4)
            # while not self.grasp_ready.value:
            #     if self.finish.value == 2:
            #         break
            logger.debug(f"max_value {self.max_value.value}")
            self.grasp_count.value = rest_time+1
            if self.max_value.value > GRASP_THRESHOLD:
                correct_img.draw()
                self.display.draw_patch()
                self.display.flip()
            else:
                incorrect_img.draw()
                self.display.draw_patch()
                self.display.flip()
            #start countdown once hand is resting
            self.grasp_ready.value = False
            clock = core.Clock() 
            logger.debug(f"rest_time = {self.rest_time.value}")
            while clock.getTime() < timing_list[rest_time]-self.rest_time.value:
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
        # while not self.grasp_ready.value:
        #     if self.finish.value == 2:
        #     break
        self.display.switch_patch()
        self.display.draw_patch()
        self.display.flip()        
        self.play_tone()

        
        
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
            