#!/usr/bin/python3
"""Audio handling
"""
from pydub import AudioSegment

def mixing(wavfile1, wavfile2, outputfile):
    """Mix two wav files

    Args:
    wavfile1(str): file path of the wave file
    wavfile2(str): file path of the wave file

    Returns:
    str: output file
    """
    sound1 = AudioSegment.from_file(wavfile1)
    sound2 = AudioSegment.from_file(wavfile2)
    combined = sound1.overlay(sound2)
    combined.export(outputfile, format='wav')

def main():
    wavfile1 = "data/cough.wav"    
    wavfile2 = "data/drill.wav"
    outputfile = 'out.wav'
    mixing(wavfile1, wavfile1, outputfile)

if __name__ == "__main__":
    main()

