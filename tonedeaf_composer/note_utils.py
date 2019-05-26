import numpy as np
from config import (
    NOTE_MIN,
    NOTE_MAX,
)

# Note/frequency conversion functions come from:
# https://newt.phys.unsw.edu.au/jw/notes.html


# Special note that is sent when we detect silence
SILENCE_NOTE = 'silence'


def freq_to_number(f):
    return NOTE_MAX + 12 * np.log2(f / 329.63)


def number_to_freq(n):
    return 329.63 * 2.0**((n - NOTE_MAX) / 12.0)


def note_name(n):
    NOTE_NAMES = 'E F F# G G# A A# B C C# D D#'.split()
    return NOTE_NAMES[n % NOTE_MIN % len(NOTE_NAMES)] + str(int(n / 12 - 1))
