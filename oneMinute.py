
import measure
import markov
import pickle
import pretty_midi
import random
import unit_lib
from markov_learn_and_create import *
import composition

class Channel:

    def __init__(self, unit_total=20, unit_lengh=3, instrument=1, appear_how=[], unit_lib=None):
        """
        Attributes:
            appear_list: list [0,1,1,0,1,...]  0 or 1: whether there is a unit being played in the time slot
            instrument: Instrument
            notes: list
            
        """
        self.unit_total = unit_total
        self.unit_length = unit_lengh
        self.instrument = instrument
        self.unit_lib = unit_lib
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
        
#        if markov == None: 
#            markov_load = load_markov("calm_piano_main.markov")
#        else:   
#            markov_load = markov
#        generated_unit = composition.predefined_unit_generator(markov_load, 4, unit_lengh)
#        for i in range(unit_total):
#            if self.appear_list[i] == 1:
#                self.notes += generated_unit.to_midi_notes(start_time = i*unit_lengh)
    
    def create(self, tags=None):
        random.seed()
        if tags == None: tags = self.unit_lib.types
#        num_units = 0
        for i in range(self.unit_total):
            if self.appear_list[i] == 1:
                generated_unit = self.unit_lib.get_unit(random.choice(tags))
                self.notes += generated_unit.to_midi_notes(start_time = i*self.unit_length)
#                num_units += 1
#                print("start_time: %d now %d units\n" % (i*self.unit_length, num_units))

#one minute audio in total
#four channels

whole_length = 60 #in second
unit_lengh = 3 #in second
unit_total = int(whole_length / unit_lengh)

#channel_number = 4
#channel_list = [1] * channel_number

instrument_list = [4, 25, 66, 106]
appear_how_list = [[0,12],[4,14],[6,18],[8,20]]
#for i in range(channel_number):
#    channel_list[i] = Channel(unit_total = unit_total, unit_lengh = unit_lengh, instrument=instrument_list[i], appear_how=appear_how_list[i])

drums_lib = unit_lib.load_lib("drums_lib.lib")

drum_channel = Channel(unit_total, unit_lengh, 15, appear_how_list[0], drums_lib)
drum_channel.create()

oneMinuteMidi = pretty_midi.PrettyMIDI ()

#for i in range(channel_number):
#    oneMinuteMidi.instruments.append(pretty_midi.Instrument(channel_list[i].instrument))
#    oneMinuteMidi.instruments[i].notes = channel_list[i].notes
oneMinuteMidi.instruments.append(pretty_midi.Instrument(15, is_drum=True))
#unit = drums_lib.get_unit()
#oneMinuteMidi.instruments[0].notes = unit.to_midi_notes()
oneMinuteMidi.instruments[0].notes = drum_channel.notes
oneMinuteMidi.write("test_drum_channel.mid")
