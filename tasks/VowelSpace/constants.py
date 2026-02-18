# -*- coding: utf-8 -*-
import os
from utils.constants import CODE_DIR

VOLUME = 0.7
STIM_DIR = os.path.join(CODE_DIR, "tasks/VowelSpace/stimuli")
PHRASE_LIST = ["hod", "heed", "who'd", "hoad"]
VS_NUM_TRIALS = 20
VS_PATHS = {
    "hoad":  "say_hoad_again.wav",
    "heed":  "say_heed_again.wav",
    "who'd": "say_whod_again.wav",
    "hod":   "say_hod_again.wav"
    }