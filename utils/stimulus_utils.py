import threading
from psychopy import core

thread_event = threading.Event()

GLOBAL_CLOCK = core.monotonicClock
