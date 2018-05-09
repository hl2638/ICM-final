# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 22:12:57 2018

@author: Rudy
"""

import measure
import markov
import pickle
import pretty_midi
import random
import os
import copy as cp
from pylab import *
import librosa             # The librosa library
import librosa.display     # librosa's display module (for plotting features)
import IPython.display     # IPython's display module (for in-line audio)
import matplotlib.pyplot as plt # matplotlib plotting functions
import matplotlib.style as ms   # plotting style
import numpy as np              # numpy numerical functions
ms.use('seaborn-muted')         # fancy plot designs

#midi = pretty_midi.PrettyMIDI('Life_drums.mid')
#print(midi.instruments)
##midi.instruments[0].program = 13
#print(midi.instruments)
#for note in midi.instruments[0].notes[:20]:
#    print(note)
##midi.write("Life_drums1.mid")
y, sr = librosa.load("C:\CloudMusic\Tobu - Life.mp3", sr=44100)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
print(tempo)
print(beats)