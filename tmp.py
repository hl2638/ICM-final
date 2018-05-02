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

midi = pretty_midi.PrettyMIDI('Summer.mid')
print(midi.instruments)
midi.instruments = [midi.instruments[1]]
midi.write("Summer_accompany.mid")