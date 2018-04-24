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

midi = pretty_midi.PrettyMIDI('FlowerDance.mid')
midi.instruments.pop(1)
midi.write('FlowerDance_main.mid')