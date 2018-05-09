
import measure
import markov
import pickle
import pretty_midi
import random
from markov_learn_and_create import *
import composition

class Channel:

    def __init__(self, unit_total=20, unit_lengh=3, instrument=1, appear_how=[], markov=None):
        """
        Attributes:
            appear_list: list [0,1,1,0,1,...]  0 or 1: whether there is a unit being played in the time slot
            instrument: Instrument
            notes: list
            
        """
        if appear_how == []:
            self.appear_list = [1] * unit_total #whether there is something in the accourding unit [1,0,0,1,1,1,1,...]
        else:
            self.appear_list = [0] * unit_total
            for i in range(int(len(appear_how)/2)):
                try:
                    start = appear_how[i*2]
                    end = appear_how[i*2+1]
                    for j in range(start,end):
                        self.appear_list[j] = 1
                except ValueError:
                    print ("appear_how value")

            print(self.appear_list)
        self.instrument = instrument
        self.notes = []
        
        if markov == None: 
            markov_load = load_markov("calm_piano_main.markov")
        else:   
            markov_load = markov
        generated_unit = composition.predefined_unit_generator(markov_load, 4, unit_lengh)
        for i in range(unit_total):
            if self.appear_list[i] == 1:
                self.notes += generated_unit.to_midi_notes(start_time = i*unit_lengh)

#one minute audio in total
#four channels

whole_length = 60 #in second
unit_lengh = 3 #in second
unit_total = int(whole_length / unit_lengh)

channel_number = 4
channel_list = [1] * channel_number

instrument_list = [4, 25, 66, 106]
appear_how_list = [[0,12],[4,14],[6,18],[8,20]]
for i in range(channel_number):
    channel_list[i] = Channel(unit_total = unit_total, unit_lengh = unit_lengh, instrument=instrument_list[i], appear_how=appear_how_list[i])

oneMinuteMidi = pretty_midi.PrettyMIDI ()

for i in range(channel_number):
    oneMinuteMidi.instruments.append(pretty_midi.Instrument(channel_list[i].instrument))
    oneMinuteMidi.instruments[i].notes = channel_list[i].notes

oneMinuteMidi.write("tt.mid")
