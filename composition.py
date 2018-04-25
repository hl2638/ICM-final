# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 19:46:34 2018

@author: Rudy
"""

import measure
import markov
import pickle
import pretty_midi
import random
from markov_learn_and_create import *

def random_beats(n):
#    print("random_beats " + str(n))
    random.seed()
    beat_choices = [1., 1./2, 1./4, 1./8]
    prob = [1, 1.25, 1.5, 1.5]
    population = []
    weights = []
    for i in range(4):
        if beat_choices[i]-n <= 0.0001:
            population.append(beat_choices[i])
            weights.append(prob[i])
    beat = random.choices(population, weights=weights)

    if n-beat[0] <= 0: return beat
    return beat+random_beats(n-beat[0])

def predefined_measure_generator(markov):
    if markov == None: markov = load_markov("default_markov")   #TODO: still need to develop a default markov chain
    if type(markov) == str: markov = load_markov(markov)
    #otherwise markov is a markov Class
    created_measure = markov.create_notes(length=15)
    beats = random_beats(4.0)
    durations = [int(beat*measure.Measure.blocks/4) for beat in beats]
#    beats = [beat*rate for beat in beats]
#    print(beats)
    notes = [note.pitch for note in created_measure[:len(beats)]]
    generated_measure = measure.Measure(notes, durations=durations)
    return generated_measure
    
def save_measure(measure, filename):
    fileObject = open(filename, 'wb')
    pickle.dump(measure, fileObject)

def load_measure(filename):
    fileObject = open(filename, 'rb')
    measure = pickle.load(fileObject)
    return measure


def composition_rule1(measure):

# This composition rule takes a piece of input which is exactly a measure.
# What it does is: randomly choose 1/4 of the notes and replace them by other notes generated by Markov
    pass
    


if __name__ == "__main__":
    
    markov = markov.Markov_chain()
    markov_learn(markov, "FlowerDance.mid")
    testmidi = pretty_midi.PrettyMIDI()
    testmidi.instruments.append(pretty_midi.Instrument(0))
#    print(type(predefined_measure_generator(markov)))
    generated_measure = predefined_measure_generator(markov).to_midi_notes()
    generated_measure = load_measure("generated_measure02.mes")
    testmidi.instruments[0].notes = generated_measure
    testmidi.write("generated_measure.mid")