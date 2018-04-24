# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 19:32:11 2018

@author: Rudy
"""

import measure
import markov
import pickle
import pretty_midi

def load_markov(filename):
    fileObject = open(filename,'r')  
    markov = pickle.load(fileObject)
    return markov

def markov_learn(markov, filename):
    #by default, learns channel 0
    midi = pretty_midi.PrettyMIDI(filename)
    channel = midi.instruments[0]
    markov.learn(channel)

def save_markov(markov, filename):    
    fileObject = open(filename,'wb')
    pickle.dump(markov,fileObject)
    fileObject.close()