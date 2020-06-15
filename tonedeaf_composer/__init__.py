import numpy as np

from config import (
    NOTE_MIN,
    NOTE_MAX,
    MIN_VOLUME,
    SAMPLE_RATE,
    SAMPLES_PER_FRAME,
)
from dsp import (
    FRAMES_PER_FFT,
    SAMPLES_PER_FFT,
    note_to_fftbin,
    freq_from_autocorr
)
from note_reader import NoteReader
from note_utils import SILENCE_NOTE, number_to_freq, freq_to_number, note_name
from frame_provider import WavFileFrameProvider, MicrophoneFrameProvider
from mouse import VirtualMouse


# Derive the frequencies which notes on the instrument will produce
GUITAR_MIN_FREQ = max(0, int(np.floor(note_to_fftbin(NOTE_MIN-1))))
GUITAR_MAX_FREQ = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX+1))))


def get_frame_provider(microphone=True):
    if microphone:
        return MicrophoneFrameProvider(SAMPLE_RATE, SAMPLES_PER_FRAME)
    else:
        filename = '/Users/philliptennen/PycharmProjects/tonedeaf_composer/c-major-scale-1-octave-open-position_mono.wav'
        return WavFileFrameProvider(filename, SAMPLES_PER_FRAME)


class AudioProcessor:
    def __init__(self, microphone=True):
        # Audio frame buffer which we'll run FFT on
        self.audio_frame_buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
        self.audio_frame_count = 0
        self.audio_frame_provider = get_frame_provider(microphone)
        self.note_reader = NoteReader()

    def process_audio_forever(self):
        while self.audio_frame_provider.has_frames():
            audio_frame = self.audio_frame_provider.get_frame()
            self.process_audio_frame(audio_frame)

    def is_audio_silence(self, audio_frame: np.ndarray) -> bool:
        volume = np.linalg.norm(audio_frame) * 10
        return volume < MIN_VOLUME

    def process_audio_frame(self, audio_frame: np.ndarray):
        # band-pass the frame to remove data outside guitar frequencies
        # audio_frame = butter_bandpass_filter(audio_frame, guitar_min_freq, guitar_max_freq, SAMPLE_RATE)

        # Shift the buffer down and new data in
        self.audio_frame_buf[:-SAMPLES_PER_FRAME] = self.audio_frame_buf[SAMPLES_PER_FRAME:]
        self.audio_frame_buf[-SAMPLES_PER_FRAME:] = audio_frame
        self.audio_frame_count += 1

        # If we don't have enough frames to run FFT yet, keep waiting
        if self.audio_frame_count < FRAMES_PER_FFT:
            return

        # Note when we get an audio frame which is below a volume threshold
        if self.is_audio_silence(audio_frame):
            self.note_reader.process_note(SILENCE_NOTE)
            return

        freq = freq_from_autocorr(self.audio_frame_buf, SAMPLE_RATE)

        # Hot-fix for when we detect a fundamental frequency which is clearly too low to be correct
        if freq < number_to_freq(NOTE_MIN):
            # Double it and assume this is the fundamental :}
            freq = freq*2

        # Get note number and nearest note
        n = freq_to_number(freq)
        n0 = int(round(n))

        note = note_name(n0)
        # We've detected a note - hand it off to the note consumer
        self.note_reader.process_note(note)
        # Let the mouse driver run any events it must do
        VirtualMouse.run_callback()


def main():
    processor = AudioProcessor()
    processor.process_audio_forever()


if __name__ == '__main__':
    main()



