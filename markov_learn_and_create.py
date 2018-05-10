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
    fileObject = open(filename,'rb')  
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
    

def trim_long(channel, limit=0.7):
    i = 0
    while i < len(channel.notes):
        if channel.notes[i].end-channel.notes[i].start > limit:
            channel.notes.pop(i)
        i += 1
    return channel

def trim_short(channel, limit=0.1):
    i = 0
    while i < len(channel.notes):
        if channel.notes[i].end-channel.notes[i].start < limit:
            channel.notes.pop(i)
        i += 1
    return channel

if __name__ == "__main__":
    markov = markov.Markov_chain()
#    midilist = ["Sunburst_piano.mid","Life_piano.mid","FlowerDance_main.mid","LuvLetter_main.mid"]
#    midilist = ["Ralph Cowell EDM Essential Melodies MIDI Vol. 1 - " +str(i)+ ".mid" for i in range(1,11)]
    midilist = ["akame_accompany.mid", "jiyuu_accompany.mid", "shinzou_accompany.mid", "unravel_accompany.mid"]
    for filename in midilist:
        midi = pretty_midi.PrettyMIDI(filename)
        channel = midi.instruments[0]
        channel = trim_short(channel)
        channel = trim_long(channel)
        markov.learn(channel)
    creation = pretty_midi.PrettyMIDI()
    creation.instruments.append(pretty_midi.Instrument(102-102))
    creation.instruments[0].notes = markov.create_notes(length=50)
    creation.write("test_hype_accompany.mid")
    save_markov(markov, "hype_piano_accompany.markov")