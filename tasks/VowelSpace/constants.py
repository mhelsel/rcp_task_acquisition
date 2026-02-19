import os
from utils.constants import CODE_DIR


PHRASE_LIST = ["hod", "heed", "who'd", "hoad"]

VS_NUM_TRIALS = 20

#volume for the .wav files since its softer than the start/end beeps
VOLUME = 0.7
STIM_DIR = os.path.join(CODE_DIR, "tasks/VowelSpace/stimuli")
VS_PATHS = {
    "hoad":  "say_hoad_again.wav",
    "heed":  "say_heed_again.wav",
    "who'd": "say_whod_again.wav",
    "hod":   "say_hod_again.wav"
    }

#paths for the instructional videos
VIDEO_PATHS = {
    }