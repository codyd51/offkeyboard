import time
import asyncio
import keyboard
import collections
from typing import List

import numpy as np
from numpy import argmax, diff
from matplotlib.mlab import find
from scipy.signal import butter, lfilter, fftconvolve

from parabolic import parabolic
from frame_provider import WavFileFrameProvider, MicrophoneFrameProvider


class Keymap:
    def __init__(self, notes: List[str], keys: List[str]):
        self.keymap = dict(zip(notes, keys))

    def key_for_note(self, note: str):
        if note not in self.keymap:
            return None
        return self.keymap[note]


class Keymap1(Keymap):
    def __init__(self):
        notes = [
            'E2', 'F2', 'F#2', 'G2', 'G#2',
            'A2', 'A#2', 'B2', 'C3', 'C#3',
            'D3', 'D#3', 'E3', 'F3', 'F#3',
            'G3', 'G#3', 'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4'
        ]
        keys = [
            'E', 'T', 'A', 'O', 'I',
            'N', 'S', 'R', 'H', 'D',
            'L', 'U', 'C', 'M', 'F',
            ' ', '\n', '.', ',', 'Y', 'W', 'G', 'P', 'B', 'V', 'K', 'X', 'Q'
        ]
        super().__init__(notes, keys)


class Keymap2(Keymap):
    def __init__(self):
        notes = [
            'E2', 'F2', 'F#2', 'G2', 'G#2',
            'A2', 'A#2', 'B2', 'C3', 'C#3',
            'D3', 'D#3', 'E3', 'F3', 'F#3',
            'G3', 'G#3', 'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4'
        ]
        keys = [
            ###--|1|--|2|--|3|--|4|
            'A', 'B', 'P', ' ', '\n', 'G', 'W', 'V', 'I', 'X', 'Q', '.', ','
            'O', 'U', 'C', 'M', 'F',
            'N', 'S', 'R', 'K', 'D',
            'E', 'T', 'Y', 'L', 'H',
            #                                   Usable to here
        ]
        keys = [
            ###--|1|--|2|--|3|--|4|
            'E', 'T', 'Y', 'L', 'H',
            'N', 'S', 'R', 'K', 'D',
            'O', 'U', 'E', 'M', 'F',
            'A', 'B', 'P', ' ', '\n', 'G', 'W', 'V', 'I', 'X', 'Q', '.', ','
            #                                   Usable to here
        ]
        # keyboards for sale


        keys = [x.lower() for x in keys]
        super().__init__(notes, keys)
    pass


class MinecraftMap(Keymap):
    def __init__(self):
        notes = [
            'E2', 'F2', 'F#2', 'G2', 'G#2',
            'A2', 'A#2', 'B2', 'C3', 'C#3',
            'D3', 'D#3', 'E3', 'F3', 'F#3',
            'G3', 'G#3', 'A3', 'A#3', 'B3', 'Cd', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4'
        ]
        keys = [
            ###--|1|--|2|--|3|--|4|
            ' ', 'left', 'down', 'up', 'right',
            'e', 'S', 'R', 'K', 'D',
            'esc', 'U', 'E', 'M', 'F',
            'A', 'B', 'P', ' ', '\n', 'G', 'W', 'V', 'I', 'X', 'Q', '.', ','
            #                                   Usable to here
        ]
        super().__init__(notes, keys)


NOTE_MIN = 40        # E2
NOTE_MAX = 64        # E4

SAMPLE_RATE = 22050         # sampling frequency in Hz
FRAMES_PER_FFT = 16         # run FFT over how many frames?
SAMPLES_PER_FRAME = 1024    # samples per frame

# Derived quantities from constants above. Note that as
# SAMPLES_PER_FFT goes up, the frequency step size decreases (sof
# resolution increases); however, it will incur more delay to process
# new sounds.
SAMPLES_PER_FFT = SAMPLES_PER_FRAME * FRAMES_PER_FFT
FREQ_STEP = float(SAMPLE_RATE) / SAMPLES_PER_FFT

# Note/frequency conversion functions come from:
# https://newt.phys.unsw.edu.au/jw/notes.html


def freq_to_number(f):
    return NOTE_MAX + 12 * np.log2(f / 329.63)


def number_to_freq(n):
    return 329.63 * 2.0**((n - NOTE_MAX) / 12.0)


def note_name(n):
    NOTE_NAMES = 'E F F# G G# A A# B C C# D D#'.split()
    return NOTE_NAMES[n % NOTE_MIN % len(NOTE_NAMES)] + str(int(n / 12 - 1))


def note_to_fftbin(n):
    return number_to_freq(n) / FREQ_STEP


def freq_from_autocorr(sig, fs):
    """Estimate fundamental frequency using autocorrelation
    From: https://gist.github.com/endolith/255291
    """
    # Calculate autocorrelation (same thing as convolution, but with
    # one input reversed in time), and throw away the negative lags
    corr = fftconvolve(sig, sig[::-1], mode='full')
    corr = corr[len(corr)//2:]

    # Find the first low point
    d = diff(corr)
    start = find(d > 0)[0]

    # Find the next peak after the low point (other than 0 lag).  This bit is
    # not reliable for long signals, due to the desired peak occurring between
    # samples, and other peaks appearing higher.
    # Should use a weighting function to de-emphasize the peaks at longer lags.
    peak = argmax(corr[start:]) + start
    px, py = parabolic(corr, peak)

    return fs / px


def plot(data: np.array, title='') -> None:
    import pylab
    pylab.plot(np.linspace(0, 1, len(data)), data)
    pylab.title(title)
    # pylab.axis([0, 0.4, 15000, -15000])
    pylab.show()
    pass


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


print('sampling at', SAMPLE_RATE, 'Hz with max resolution of', FREQ_STEP, 'Hz')
print()

d = collections.deque(maxlen=10)

from threading import Timer


def release_key(*args):
    key = ''.join(args)
    print(f'release_key {key}')
    keyboard.release(key)


class NoteReader:
    def __init__(self):
        self.ringbuf_size = 10
        self.last_notes = collections.deque(maxlen=self.ringbuf_size)
        self.last_detected_note = None
        self.keymap = MinecraftMap()

    def process_note(self, note: str):
        self.last_notes.append(note)
        # should we register this note?
        # If most of the notes in the ringbuffer are the same note, and this note is different from the last detected
        # note, do a state transition
        key = self.keymap.key_for_note(note)
        if note == 'silence':
            if self.last_detected_note and self.last_detected_note != 'silence':
                key = self.keymap.key_for_note(self.last_detected_note)
                if not key:
                    return
                print(f'detected silence, removing {key}')
                # release_key(self.last_detected_note)
                keyboard.release(key)
            self.last_detected_note = 'silence'
            return

        self.last_detected_note = note

        if key in ['left', 'down', 'up', 'right', ' ']:
            print(f'{note}\t({key})')

            keyboard.press(key)
            # r = Timer(0.5, release_key, str(key))
            # r.start()
        else:
            if self.last_notes.count(note) > 5 and note != self.last_detected_note:
                self.register_note(note)
                # fill the entire buffer with whatever we just registered
                for _ in range(self.ringbuf_size):
                    self.last_notes.append(note)

    def register_note(self, note: str):
        self.last_detected_note = note

        key = self.keymap.key_for_note(note)
        if not key:
            return

        # print(f'{note}\t({key})')
        print(f'{note}\t({key})')
        # keyboard.write(key)
        keyboard.send(key)


# Allocate space to run an FFT.
buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)

reader = NoteReader()

microphone = True
if microphone:
    frame_provider = MicrophoneFrameProvider(SAMPLE_RATE, SAMPLES_PER_FRAME)
else:
    filename = '/Users/philliptennen/PycharmProjects/tonedeaf_composer/c-major-scale-1-octave-open-position_mono.wav'
    frame_provider = WavFileFrameProvider(filename, SAMPLES_PER_FRAME)


num_frames = 0

guitar_min_freq = max(0, int(np.floor(note_to_fftbin(NOTE_MIN-1))))
guitar_max_freq = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX+1))))

while frame_provider.has_frames():
    audio_frame = frame_provider.get_frame()

    # band-pass the frame to remove data outside guitar frequencies
    # audio_frame = butter_bandpass_filter(audio_frame, guitar_min_freq, guitar_max_freq, SAMPLE_RATE)

    # Shift the buffer down and new data in
    buf[:-SAMPLES_PER_FRAME] = buf[SAMPLES_PER_FRAME:]
    buf[-SAMPLES_PER_FRAME:] = audio_frame
    num_frames += 1

    # Note when we get an audio frame which is below a volume threshold
    volume = np.linalg.norm(audio_frame) * 10
    # Chosen through experimentation
    if volume < 100000:
        # print(volume)
        reader.process_note('silence')
        continue
    # print(f'volume: {volume}')

    # If we don't have enough frames to run FFT, stop here
    if num_frames < FRAMES_PER_FFT:
        continue

    freq = freq_from_autocorr(buf, SAMPLE_RATE)

    # Hotfix for when we detect a fundamental frequency which is clearly too low to be correct
    if freq < number_to_freq(NOTE_MIN):
        # Double it and assume this is the fundamental :}
        freq = freq*2

    # Get note number and nearest note
    n = freq_to_number(freq)
    n0 = int(round(n))

    # print('{:>3s} {:+.2f} ({:7.2f}) @ {:7.2f} Hz'.format(note_name(n0), n - n0, n, freq))

    note = note_name(n0)
    if note == 'A1' or note == 'G#2':
        #  breakpoint()
        pass
    # print(note)
    reader.process_note(note)
    # plot(buf)

    continue
