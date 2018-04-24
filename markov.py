# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 15:32:25 2018

@author: Rudy
"""

# To begin using librosa we need to import it, and other tools such as matplotlib and numpy
from pylab import *
import pretty_midi
import librosa             # The librosa library
import librosa.display     # librosa's display module (for plotting features)
import IPython.display     # IPython's display module (for in-line audio)
import matplotlib.pyplot as plt # matplotlib plotting functions
import matplotlib.style as ms   # plotting style
import numpy as np              # numpy numerical functions


"""
# The next line makes all plots appear in the notebook, instead of a separate pop-up window
# visualize score
def show_score(S, fs = 100):
    imshow(S, aspect='auto', origin='bottom', interpolation='nearest', cmap=cm.gray_r)
    xlabel('Time')
    ylabel('Pitch')
    pc=array(['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B'])
    idx = tile([0,4,7],13)[:128]
    yticks(arange(0,128,4),pc[idx], fontsize=5)
    xticks(arange(0,S.shape[1],fs),arange(0,S.shape[1],fs)/fs, )
"""
     
def matrix2notes(m):
    # first sort the matrix to make sure starting time is in order
    m = array(m)
    m = m[argsort(m[:,0]),:]
    # transfer the databack to note list
    notes=[pretty_midi.Note(start=m[i,0], end=m[i,1], pitch=int(m[i,2]), velocity= int(m[i,3]) ) 
                            for i in range(size(m,0))]
    return notes



class Markov_chain:
    
    def __init__(self):
        self.note_next = dict()     #numbers of a combination
        self.next_notes = dict()    #notes that follow a certain note
        self.note_next_total = dict() #total combinations of a note
        self.dur_next = dict()
        self.next_durs = dict()
        self.dur_next_total = dict()
        self.notes = set()
        self.durations = set()
        

    def learn(self, channel):
        
        i = 0
        while i+1 < len(channel.notes):
            if channel.notes[i+1].start - channel.notes[i].start < 0.0001:
#                print(channel.notes[i+1],end=" removed\n")
                channel.notes.pop(i+1)
            i += 1
        
        self.notes = self.notes.union([note.pitch for note in channel.notes])    #all the notes
        self.durations = self.durations.union([round(note.end-note.start, 4) for note in channel.notes])    #all the durations
#        print(self.notes, self.durations)
        
        for note in self.notes:     # if this note found for the first time
            if self.next_notes.get(note) == None: 
                self.next_notes[note] = []
                self.note_next_total[note] = 0
        for duration in self.durations:     # if this duration found for the first time
            if self.next_durs.get(duration) == None:
                self.next_durs[duration] = []
                self.dur_next_total[duration] = 0

        for i in range(len(channel.notes)-1):    # all the notes in channel
            this_note = channel.notes[i].pitch
            next_note = channel.notes[i+1].pitch
            if self.note_next.get((this_note, next_note)) == None:    # this combination found for the first time
                self.next_notes[this_note].append(next_note)
                self.note_next[(this_note, next_note)] = 1
            #         print(this_note, next_note)
                self.note_next_total[this_note] += 1
            else: 
                self.note_next[(this_note, next_note)] += 1
            

            this_dur = round(channel.notes[i].end-channel.notes[i].start, 4)
            next_dur = round(channel.notes[i+1].end-channel.notes[i+1].start, 4)
            if self.dur_next.get((this_dur, next_dur)) == None:
                self.next_durs[this_dur].append(next_dur)
                self.dur_next[(this_dur, next_dur)] = 1
                self.dur_next_total[this_dur] += 1
            else:
                self.dur_next[(this_dur, next_dur)] += 1

        for pair in self.note_next.keys():
            self.note_next[pair] /= float(self.note_next_total[pair[0]])

        for pair in self.dur_next.keys():
            self.dur_next[pair] /= float(self.dur_next_total[pair[0]])
    
    
        
    def create_notes(self, length=100, start_note=-1, start_dur=-1, dur_limit=-1, velocity=101):
        #    returns a pretty_midi.PrettyMIDI()
        import random
        random.seed()
        if start_note == -1: 
            start_note = random.choice(list(self.notes))
            while(self.note_next_total[start_note] == 0):
                start_note = random.choice(list(self.notes))
                
        if start_dur == -1: 
            start_dur = random.choice(list(self.durations))
            while(self.dur_next_total[start_dur] == 0):
                start_dur = random.choice(list(self.durations))
        note_matrix = matrix(zeros((length, 4)))
        note_matrix[0,:] = matrix([0, start_dur, start_note, velocity])
        for i in range(1, length):
            prev_note = int(note_matrix[i-1, 2])
            population = self.next_notes[prev_note]
            weights = [self.note_next[(prev_note, note)] for note in population]
#            print(population)
#            print(weights)
            note = random.choices(population, weights)[0]

            prev_dur = round(note_matrix[i-1, 1]-note_matrix[i-1, 0], 4)
            population = self.next_durs[prev_dur]
            weights = [self.dur_next[(prev_dur, dur)] for dur in population]
            dur = random.choices(population, weights)[0]
            
            last_end = note_matrix[i-1,1]
            note_matrix[i,:] = matrix([last_end, last_end+dur, note, velocity])
                
        notes = matrix2notes(note_matrix)
        return notes

if __name__ == "__main__":
    markov = Markov_chain()
    midi = pretty_midi.PrettyMIDI("FlowerDance.mid")
    channel = midi.instruments[0]
    #print(channel.notes)
    markov.learn(channel)