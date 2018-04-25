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
    
    blocks = 48
    
    def __init__(self, notes=[], starts=[], durations=[], velocities=[], time=3, autofill=False):
        self.time = time
        self.length = len(notes)
        self.velocities = velocities
        if len(self.velocities) == 0: self.velocities = [101 for i in range(self.length)] 
        
        if type(notes[0]) != int:
            self.notes = [pretty_midi.note_name_to_number(note) for note in notes]
        else: 
            self.notes = notes    # ex. [60, 63, 67, 69, 63, 60]
            
        self.starts = starts      #ex. [5, 8, 12, 20]
        
        if not autofill:
            self.durations = durations    # ex. [1, 1, 1./2, 1./2, 1]
        else:
            self.durations = [self.starts[i+1]-self.starts[i] for i in range(len(self.starts)-1)]+[Measure.blocks-self.starts[-1]]
        
        if len(self.starts) == 0:
            self.starts = [0]
            for i in range(self.length-1):
                self.starts.append(self.starts[i]+self.durations[i])
        
    def set_starts(self, starts):
        self.starts = starts        
    def set_durations(self, durations):
        self.durations = durations    
    def set_velocities(self, velocities):
        self.velocities = velocities
    def get_starts(self):
        return self.starts
    def get_notes(self):
        return [pretty_midi.note_number_to_name(note) for note in self.notes]
    def get_durations(self):
        return self.durations
    def get_length(self):
        return self.length
    def get_time(self):
        return self.time
    def get_velocities(self):
        return self.velocities
    
    def __str__(self):
        return str(self.get_notes())+'\n'+str(self.get_starts())+'\n'+str(self.get_durations())+'\n'+str(self.get_velocities())
    
    def to_midi_notes(self):        #returns note list appendable for midi instruments
        print(self.length)
        print(self)
        spb = self.time/float(Measure.blocks)    # seconds per block
        starts = [start*spb for start in self.starts]
        ends = [(self.starts[i]+self.durations[i])*spb for i in range(self.length)]
        notes = [pretty_midi.Note(start=starts[i], end=ends[i], pitch=self.notes[i], velocity=self.velocities[i]) for i in range(self.length)]
        return notes
  
    