# -*- coding: utf-8 -*-
import os
from rcp_task_acquisition.utils.constants import CODE_DIR

MIN_REST_VAL = 1
MAX_REST_VAL = 2
TRIALS_PER_BLOCK = 20

GRASP_THRESHOLD = 0.5
POKE_THRESHOLD = 0.5

CORRECT_IMG = os.path.join(CODE_DIR, "tasks", "NBack", "stimuli", "feedback_correct.png")
INCORRECT_IMG = os.path.join(CODE_DIR, "tasks", "NBack", "stimuli", "feedback_incorrect.png")
