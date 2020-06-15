import pylab
import numpy as np
from scipy.signal import butter, lfilter, fftconvolve

from parabolic import parabolic
from note_utils import number_to_freq
from config import (
    SAMPLE_RATE,
    FRAMES_PER_FFT,
    SAMPLES_PER_FRAME
)

# Derived quantities from configuration constants. Note that as
# SAMPLES_PER_FFT goes up, the frequency step size decreases (sof
# resolution increases); however, it will incur more delay to process
# new sounds.
SAMPLES_PER_FFT = SAMPLES_PER_FRAME * FRAMES_PER_FFT
FREQ_STEP = float(SAMPLE_RATE) / SAMPLES_PER_FFT


def find(condition):
    # https://stackoverflow.com/questions/57100894/matplotlib-versions-3-does-not-inlclude-a-find
    res, = np.nonzero(np.ravel(condition))
    return res


def freq_from_autocorr(sig, fs):
    """Estimate fundamental frequency using autocorrelation
    From: https://gist.github.com/endolith/255291
    """
    # Calculate autocorrelation (same thing as convolution, but with
    # one input reversed in time), and throw away the negative lags
    corr = fftconvolve(sig, sig[::-1], mode='full')
    corr = corr[len(corr)//2:]

    # Find the first low point
    d = np.diff(corr)
    start = find(d > 0)[0]

    # Find the next peak after the low point (other than 0 lag).  This bit is
    # not reliable for long signals, due to the desired peak occurring between
    # samples, and other peaks appearing higher.
    # Should use a weighting function to de-emphasize the peaks at longer lags.
    peak = np.argmax(corr[start:]) + start
    px, py = parabolic(corr, peak)

    return fs / px


def plot(data: np.array, title='') -> None:
    pylab.plot(np.linspace(0, 1, len(data)), data)
    pylab.title(title)
    pylab.show()


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


def note_to_fftbin(n):
    return number_to_freq(n) / FREQ_STEP
