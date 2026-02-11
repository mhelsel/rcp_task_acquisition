# -*- coding: utf-8 -*-
from enum import Enum
import os
from psychopy import core
from pathlib import Path



#Base dir
# BASE_DIR = 
BASEDIR = Path(__file__).resolve().parent.parent.parent
CODE_DIR = os.path.join(BASEDIR, "task-acquisition")
# STIM_CONFIG_FILE_PATH = '/home/rcp/task-acquisition/config_files'
# STIM_CONFIG_FILE_NAME = 'visualStimulusConfig.yaml'
# CONFIG_FILE_PATH = '/home/rcp/task-acquisition/config_files'
# SCREEN_CONFIG_FILE_NAME = "screen_config.yaml"
# DUMP_FOLDER_PATH = '/home/rld/Documents/RawDataLocal/Dump/'
DUMP_FOLDER_PATH =os.path.join(BASEDIR, 'Documents/RawDataLocal/Dump')
STIM_CONFIG_FILE_PATH = CONFIG_FILE_PATH = os.path.join(CODE_DIR, 'config_files')
STIM_CONFIG_FILE_NAME = 'visualStimulusConfig.yaml'
SCREEN_CONFIG_FILE_NAME = "screen_config.yaml"
VIDEO_DIR = os.path.join(BASEDIR, "Videos/task_videos")

# constants for graphing
PLOT_CONSTANTS = ["Cameras", "Barcode", "Photodiode"]
LINE_STYLES = ["--", "-.", ":"]
COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

# labjack constants
SCANS_PER_READ = 5000
#Hardcoded the hardware and labjack bc its much easier than pulling from somewhere for now
CAMERA_HEADERS = ["In Use","Name", "Is Primary", "Serial Number"]
HEADERS = ["In Use", "Hardware", "Labjack Pin", "Voltage Range"]#"Graph Min", "Graph Max"]
HARDWARE_LIST = ["Audio", "Cameras", "Button", "Photodiode", 
                 "Grasp Button", "Microphone 1", "Microphone 2", 
                 "String Potentiometer", "Force Sensor X", "Force Sensor Y", 
                 "Force Sensor Z", "Barcode"]
LABJACK_PIN_LIST = ["AIN0", "AIN1", "AIN2", "AIN3", "AIN4", "AIN5", "AIN6", "AIN7", 
                    "FIO0", "FIO1", "FIO2", "FIO3", "FIO4", "FIO5", "FIO6", "FIO7",
                    "EIO0", "EIO1", "EIO2", "EIO3", "EIO4", "EIO5", "EIO6", "EIO7"]
ANALOG_RANGES = [11, 9.6, 4.8, 2.4, 1.2, 0.6, 0.3, 0.15, 0.075, 0.036, 0.015]




# shorter name for the global clock
GLOBAL_CLOCK = core.monotonicClock

# constants for the tasks

# sound constants
VOLUME = 0.125       # range [0.0, 1.0]
SAMPLING_RATE = 44100 # sampling rate, Hz
DURATION = 1.0       # in seconds, can be a float
FREQUENCY = 750.0    # sine frequency, Hz, can be a float



# verbal fluency constants
TRIAL_TIME = 60
PHONEMIC_LIST = ['["F", "A", "S"]', '["C", "F", "L"]']
SEMANTIC_LIST = ["Animals", "Food and Drinks", "Fruits", "Tools"]
PHONEMIC_PHRASE = "Phonemic Fluency. Prompt the participant to say as many words beginning with the letter *"
SEMANTIC_PHRASE = "Semantic Fluency. Prompt the participant to say as many * as they can think of"
VERBAL_FLUENCY_PATHS = {
    "CFL": {
        "C": "VerbalFluency/VerbalFluency_C_instructions.mp4",
        "F": "VerbalFluency/VerbalFluency_F_CFL_instructions.mp4",
        "L": "VerbalFluency/VerbalFluency_L_instructions.mp4"
        },
    "FAS": {
        "F": "VerbalFluency/VerbalFluency_F_instructions.mp4",
        "A": "VerbalFluency/VerbalFluency_A_instructions.mp4",
        "S": "VerbalFluency/VerbalFluency_S_instructions.mp4"
        },
    "Semantic": {
        "Animals": "VerbalFluency/VerbalFluency_animals_instructions.mp4",
        "Food and Drinks": "VerbalFluency/VerbalFluency_Foodanddrink_instructions.mp4",
        "Fruits": "VerbalFluency/VerbalFluency_Fruits_instructions.mp4",
        "Tools": "VerbalFluency/VerbalFluency_tools_instructions.mp4"
        }
    }


# basic taps constants
BASIC_TAPS_TIME = 10
BASIC_TAPS_PATH = "UPDRS_finger_tap_instructions_captioned.mp4"


# ddk constants
DDK_TRIAL_TIME = 10
DDK_TRIALS_PER_SYLLABLE = 3
DDK_TRIALS = ["puh", "tuh", "kuh", "puhtuhkuh", "butterfly"]
DDK_PATHS = {
    "introduction": "task_videos/FIRSTVID_trial_structure_instructions.mp4",
    "puh_1": "DDK/puh_instructions_captioned.mp4",
    "puh":   "DDK/puh_trials2and3_instructions_captioned.mp4",
    "tuh_1": "DDK/tuh_instructions_captioned.mp4",
    "tuh":   "DDK/tuh_trials2and3_instructions_captioned.mp4",
    "kuh_1": "DDK/kuh_instructions_captioned.mp4",
    "kuh":   "DDK/kuh_trials2and3_instructions_captioned.mp4",
    "puhtuhkuh_1": "DDK/puhtuhkuh_instructions_captioned.mp4",
    "puhtuhkuh":   "DDK/puhtuhkuh_trials2and3_instructions_captioned.mp4",
    "butterfly_1": "DDK/butterfly_instructions_captioned.mp4",
    "butterfly":   "DDK/butterfly_trials2and3_instructions_captioned.mp4"
    }


# nBack constants
NBACK_TYPES = ["1-back", "2-back"]

# tone taps
TAP_DURATION = 0.05  # seconds
TAP_FREQUENCY = 1000 # Hz



# SARA constants
# in assesments lists, first list is the scoring criteria, while the second is whether or not to include hand choice
ASSESMENTS = {
    "gait": {
             0: "Normal, no difficulties in walking, turning, and walking tandem (up to one misstep allowed)",
             1: "Slight difficulties, only visible when walking 10 consecutive steps in tandem",
             2: "Clearly abnormal, tandem walking >10 steps not possible",
             3: "Considerable staggering, difficulties in half-turn, but without support",
             4: "Marked staggering, intermittent support of the wall required",
             5: "Severe staggering, permanent support of one stick or light support by one arm required",
             6: "Walking >10 m only with strong support (two special sticks or stroller or accompanying person)",
             7: "Walking <10 m only with strong support (two special sticks or stroller or accompanying person)",
             8: "Unable to walk, even supported"
             },
    "stance": {
             0: "Normal, able to stand in tandem for >10 s",
             1: "Able to stand with feet together without sway, but not in tandem for >10 s",
             2: "Able to stand with feet together for >10 s, but only with sway",
             3: "Able to stand for >10 s without support in natural position, but not with feet together",
             4: "Able to stand for >10 s in natural position only with intermittent support",
             5: "Able to stand >10 s in natural position only with constant support of one arm",
             6: "Unable to stand for >10 s even with constant support of one arm"
             },
    "sitting": {
             0: "Normal, no difficulties sitting >10 s",
             1: "Slight difficulties, intermittent sway",
             2: "Constant sway, but able to sit >10 s without support",
             3: "Able to sit for >10 s only with intermittent support",
             4: "Unable to sit for >10 s without continuous support"
             },
    "speech disturbance": {
             0: "Normal",
             1: "Suggestion of speech disturbance",
             2: "Impaired speech, but easy to understand",
             3: "Occasional words difficult to understand",
             4: "Many words difficult to understand",
             5: "Only single words understandable",
             6: "Speech unintelligible / anarthria"
             },
    "finger chase left": {
             0: "No dysmetria",
             1: "Dysmetria, under/overshooting target <5 cm",
             2: "Dysmetria, under/overshooting target <15 cm",
             3: "Dysmetria, under/overshooting target >15 cm",
             4: "Unable to perform 5 pointing movements"
             },
    "finger chase right": {
             0: "No dysmetria",
             1: "Dysmetria, under/overshooting target <5 cm",
             2: "Dysmetria, under/overshooting target <15 cm",
             3: "Dysmetria, under/overshooting target >15 cm",
             4: "Unable to perform 5 pointing movements"
             },
    "nose-finger test left": {
             0: "No tremor",
             1: "Tremor with an amplitude <2 cm",
             2: "Tremor with an amplitude <5 cm",
             3: "Tremor with an amplitude >5 cm",
             4: "Unable to perform 5 pointing movements"
             },
    "nose-finger test right": {
             0: "No tremor",
             1: "Tremor with an amplitude <2 cm",
             2: "Tremor with an amplitude <5 cm",
             3: "Tremor with an amplitude >5 cm",
             4: "Unable to perform 5 pointing movements"
             },
    "fast alternating hand movements left": {
             0: "Normal, no irregularities (performs <10 s)",
             1: "Slightly irregular (performs <10 s)",
             2: "Clearly irregular, single movements difficult to distinguish or relevant interruptions, but performs <10 s",
             3: "Very irregular, single movements difficult to distinguish or relevant interruptions, performs >10 s",
             4: "Unable to complete 10 cycles"
            },
    "fast alternating hand movements right": {
             0: "Normal, no irregularities (performs <10 s)",
             1: "Slightly irregular (performs <10 s)",
             2: "Clearly irregular, single movements difficult to distinguish or relevant interruptions, but performs <10 s",
             3: "Very irregular, single movements difficult to distinguish or relevant interruptions, performs >10 s",
             4: "Unable to complete 10 cycles"
            },
    "heel-shin slide left": {
             0:"Normal",
             1: "Slightly abnormal, contact to shin maintained",
             2: "Clearly abnormal, goes off shin up to 3 times during 3 cycles",
             3: "Severely abnormal, goes off shin 4 or more times during 3 cycles",
             4: "Unable to perform the task"
             },
    "heel-shin slide right": {
             0:"Normal",
             1: "Slightly abnormal, contact to shin maintained",
             2: "Clearly abnormal, goes off shin up to 3 times during 3 cycles",
             3: "Severely abnormal, goes off shin 4 or more times during 3 cycles",
             4: "Unable to perform the task"
             },
    }

