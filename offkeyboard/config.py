# #####
# Settings you should feel free to play around with.
# #####

JUMP_NOTE = 'F#3'

STRAFE_LEFT_NOTE = 'F2'
STRAFE_DOWN_NOTE = 'F#2'
STRAFE_UP_NOTE = 'G2'
STRAFE_RIGHT_NOTE = 'G#2'

ONE_NOTE = 'G#3'
TWO_NOTE = 'A4'
THREE_NOTE = 'A#4'
FOUR_NOTE = 'B4'
FIVE_NOTE = 'C4'
SIX_NOTE = 'C#4'
SEVEN_NOTE = 'D4'
EIGHT_NOTE = 'D#4'
NINE_NOTE = 'E4'
ZERO_NOTE = 'F4'

ESC_NOTE = 'D3'

COMBO_KEYS_TO_NOTES = {
    'F3': ['up', 'left'],
    'F#4': ['up', 'right'],
}

MIN_VOLUME = 100000  # Any audio below this value is considered silence. Chosen through experimentation

# #####
# You probably won't need to modify things in this section, as they deal with signal processing
# #####

NOTE_MIN = 40        # E2
NOTE_MAX = 64        # E4


SAMPLE_RATE = 22050         # sampling frequency in Hz
FRAMES_PER_FFT = 16         # run FFT over how many frames?
SAMPLES_PER_FRAME = 1024    # samples per frame


# #####
# For Minecraft
# #####

MOUSE_LEFT_NOTE = 'D#3'
MOUSE_DOWN_NOTE = 'E3'
MOUSE_UP_NOTE = 'F3'
MOUSE_RIGHT_NOTE = 'F#3'
MOUSE_CLICK_NOTE = 'G3'
MOUSE_SPEED = 30

CRAFT_NOTE = 'A3'
ATTACK_NOTE = 'A#3'
PICK_BLOCK_NOTE = 'B3'
PLACE_BLOCK_NOTE = 'C3'

