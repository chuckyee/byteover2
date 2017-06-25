#!/usr/bin/python3
"""Audio handling
"""
from __future__ import print_function
from pydub import AudioSegment
import librosa.util

def mixing_librosa(filename1, filename2, outputfile, crop2=True):
    import librosa
    import librosa.output

    y1, sr1 = librosa.load(filename1)
    y2, sr2 = librosa.load(filename2, sr=sr1)

    if crop2: y2 = y2[:y1.shape[0]]

    yout = (y1  + y2) / 2.0
    librosa.output.write_wav(outputfile, yout, sr1)

def mixing(wavfile1, wavfile2, outputfile, crop2=True):
    """Mix two wav files.

    Args:
    wavfile1(str): file path of the wave file
    wavfile2(str): file path of the wave file
    crop2(boolean): crop the second audio file according to the first

    Returns:
    str: output file
    """
    sound1 = AudioSegment.from_mp3(wavfile1)
    sound2 = AudioSegment.from_mp3(wavfile2)
    sec1 = sound1.duration_seconds
    sec2 = sound2.duration_seconds

    if crop2:
        sound2 = sound2[:sec1*1000]

    combined = sound1.overlay(sound2)
    combined.export(outputfile, format='mp3')

def main():
    wavfile1 = 'twiliorecording.wav'
    wavfile2 = 'data/heavymetal.mp3'
    outputfile = 'out.wav'
    #mixing(wavfile1, wavfile1, outputfile)
    mixing_librosa(wavfile1, wavfile2, outputfile)

if __name__ == "__main__":
    main()

