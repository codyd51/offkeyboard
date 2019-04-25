import time
import collections

import numpy as np
from numpy import argmax, diff
from matplotlib.mlab import find
from scipy.signal import butter, lfilter, fftconvolve

from tonedeaf_composer.parabolic import parabolic
from tonedeaf_composer.frame_provider import WavFileFrameProvider, MicrophoneFrameProvider


NOTE_MIN = 40        # E2
NOTE_MAX = 64        # E4

SAMPLE_RATE = 22050         # sampling frequency in Hz
FRAMES_PER_FFT = 16         # run FFT over how many frames?
SAMPLES_PER_FRAME = 2048    # samples per frame

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


class NoteReader:
    def __init__(self):
        # Only register a note if we hear it > 5 times in a row
        self.ringbuf_size = 20
        self.last_notes = collections.deque(maxlen=self.ringbuf_size)
        # Incur a delay before we allow more notes to be processed
        self.register_delay = 0.0
        self.last_registered_note_time = 0

    def process_note(self, note: str):
        if time.time() - self.register_delay < self.last_registered_note_time:
            # skip note
            return
        self.last_notes.append(note)
        # should we register this note?
        if self.last_notes.count(note) > self.ringbuf_size*0.75:
            self.register_note(note)

    def register_note(self, note: str):
        self.last_registered_note_time = time.time()

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
        keymap = dict(zip(notes, keys))
        from pprint import pprint
        # pprint(keymap)
        # print(keymap)

        if note not in keymap:
            return
            raise RuntimeError(f'Unknown note {note}')

        # print(f'{keymap[note]} ({note})')
        print(f'{keymap[note]}', end='')
        import sys
        sys.stdout.flush()


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
    # plot(raw_frame, title='before bandpass')
    # band-pass the frame to remove data outside guitar frequencies
    audio_frame = butter_bandpass_filter(audio_frame, guitar_min_freq, guitar_max_freq, SAMPLE_RATE)
    # plot(raw_frame, title='after bandpass')

    # Shift the buffer down and new data in
    buf[:-SAMPLES_PER_FRAME] = buf[SAMPLES_PER_FRAME:]
    buf[-SAMPLES_PER_FRAME:] = audio_frame
    num_frames += 1
    # Do nothing until buffer fills for the first time
    if num_frames < FRAMES_PER_FFT:
        continue

    freq = freq_from_autocorr(buf, SAMPLE_RATE)

    # Get note number and nearest note
    n = freq_to_number(freq)
    n0 = int(round(n))

    # print('{:>3s} {:+.2f} ({:7.2f}) @ {:7.2f} Hz'.format(note_name(n0), n - n0, n, freq))

    note = note_name(n0)
    print(note)
    # reader.process_note(note)
    # plot(buf)

    continue
