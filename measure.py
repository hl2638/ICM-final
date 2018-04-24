# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 18:20:02 2018

@author: Rudy
"""

# To begin using librosa we need to import it, and other tools such as matplotlib and numpy
import os
import copy as cp
from pylab import *
import pretty_midi
import librosa             # The librosa library
import librosa.display     # librosa's display module (for plotting features)
import IPython.display     # IPython's display module (for in-line audio)
import matplotlib.pyplot as plt # matplotlib plotting functions
import matplotlib.style as ms   # plotting style
import numpy as np              # numpy numerical functions
ms.use('seaborn-muted')         # fancy plot designs


def matrix2notes(m):
    # first sort the matrix to make sure starting time is in order
    m = array(m)
    m = m[argsort(m[:,0]),:]
    # transfer the databack to note list
    notes=[pretty_midi.Note(start=m[i,0], end=m[i,1], pitch=int(m[i,2]), velocity= int(m[i,3]) ) 
                            for i in range(size(m,0))]
    return notes

class Measure:
    def __init__(self, notes=[], beats=[], velocity=100, is_drum=False):
        self.length = len(notes)
        if type(notes[0]) != int:
            self.notes = [pretty_midi.note_name_to_number(note) for note in notes]
        else: 
            self.notes = notes    # ex. [60, 63, 67, 69, 63, 60]
        self.beats = beats    # ex. [1, 1, 1./2, 1./2, 1]
        self.velocity = velocity
    
    
    def extend_measure(self, other, velocity=-1):
        self.length += other.get_length()
        self.notes += other.notes
        self.bats += other.beats
        if velocity != -1:     # default: do not change velocity
            self.velocity = velocity
    
    def set_velocity(self, velocity):
        self.velocity = velocity
    
    def get_notes(self):
        return [pretty_midi.note_number_to_name(note) for note in self.notes]
    
    def get_beats(self):
        return self.beats
    
    def get_length(self):
        return self.length
    
    def get_velocity(self):
        return self.velocity
    
    
    def __str__(self):
        return str(self.get_notes())+'\n'+str(self.get_beats())
    
    def to_midi_notes(self, bpm=120, velocity=-1):        #returns note list appendable for midi instruments
        if velocity == -1: velocity = self.velocity
        rate = 60./bpm
        starts = []
        ends = [beat*rate for beat in self.beats]
        starts = [0] + ends[:-1]
        notes = [pretty_midi.Note(start=starts[i], end=ends[i], pitch=self.notes[i], velocity=velocity) for i in range(self.length)]
        return notes
  