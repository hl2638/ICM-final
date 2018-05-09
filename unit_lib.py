# -*- coding: utf-8 -*-
"""
Created on Wed May  9 19:55:53 2018

@author: Rudy
"""

import measure
import markov
import pickle
import pretty_midi
import random
from markov_learn_and_create import *
import composition


class Unit_lib:
    FAST = 0
    SLOW = 1
    def __init__(self, instrument=0):
        self.instrument = instrument
        self.num_of_types = 0
        self.types = []
        self.units = dict()     #units: {tag1: [(unit1_1,unit_name1_1), (unit 1_2,unit_name1_2) ...], tag2:...}
        
    def add(self, unit, tag, name=""):   #tag: what type this unit belongs to e.g. fast, slow, ...
        if name == "":
            for note in unit.notes[:4]:
                name += str(note)
        if self.units.get(tag) == None:
            self.units[tag] = [(unit, name)]
            self.num_of_types += 1
            self.types.append(tag)
        else:
            if unit not in self.units[tag]:
                self.units[tag].append((unit, name))
#        print("Now the list looks like:", self.units[tag])
    def add_units(self, unit_list):
        for unit, tag, name in unit_list:
            self.add(unit, tag, name)
    
    def delete_unit(self, unit_name, tag=None):   #specify tag to delete faster
        if unit_name == "": return
        if tag == None:
            tags = self.types
        else:
            tags = [tag]
            
        for tag in tags:
            for i in range(len(self.units[tag])):
                if self.units[tag][i][1] == unit_name:
                    self.units[tag].pop(i)
                    return
                
    def __str__(self):
        str_ret = dict()
        for key, val in self.units.items():
            str_ret[key] = [tup[1] for tup in val]
        return str(str_ret)
               
    

def load_unit(filename):
    fileObject = open(filename, 'rb')
    measure = pickle.load(fileObject)
    return measure

def save_lib(lib, filename):
    fileObject = open(filename, 'wb')
    pickle.dump(lib, fileObject)

def load_lib(filename):
    fileObject = open(filename, 'rb')
    lib = pickle.load(fileObject)
    return lib

if __name__ == "__main__":
    lib_dict = dict()           #key: instrument no.  value: corresponding unit library
    drums_lib = Unit_lib(15)
    lib_dict[15] = drums_lib
    #what we want to add to the lib this time
    # unit, tag, unit_name
    unit_list = [(load_unit("drum_fast%d.mes" % i), Unit_lib.FAST, "drum_fast%d.mes" % i) for i in range(1,5)]              
    drums_lib.add_units(unit_list)
    print(drums_lib)
    
    