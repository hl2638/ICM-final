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

midi = pretty_midi.PrettyMIDI('Shingeki no Koyojin Jiyuu no Tsubasa.mid')
print(midi.instruments)
#midi.instruments[0].program = 13
#print(midi.instruments)
midi.instruments = [midi.instruments[0]]
midi.write("jiyuu_main.mid")