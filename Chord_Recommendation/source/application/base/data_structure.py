from collections import deque, namedtuple
from dataclasses import dataclass
from itertools import accumulate
import re

from .configuration import NUMBER_OF_FLATS
from .package.display import Display
from .package.tools import Record, InvertableMapping



class AdjacentNotes():

    @dataclass(frozen = True)
    class Domain():
        next_note = ('C', 'D', 'E', 'F', 'G', 'A', 'B')
        previous_note = ('D', 'E', 'F', 'G', 'A', 'B', 'C')
    @dataclass(frozen = True)
    class Codimain():
        next_note = ('D', 'E', 'F', 'G', 'A', 'B', 'C')
        previous_note = ('C', 'D', 'E', 'F', 'G', 'A', 'B')
    
    next_note_mapping = {note: next_note for note, next_note in zip(Domain.next_note,
                                                                    Codimain.next_note)}
    previous_note_mapping = {note: previous_note for note, previous_note in zip(Domain.previous_note,
                                                                                Codimain.previous_note)}

    half_step = {('E', 'F'), ('B', 'C')}
    whole_step = {('C', 'D'), ('D', 'E'), ('F', 'G'), ('G', 'A'), ('A', 'B')}

    def get_next_adjacent_note(cls, note):
        return cls.next_note_mapping[note]

    def get_previous_adjacent_note(cls, note):
        return cls.previous_note_mapping[note]

    def get_adjacent_interval(cls, *adjacent_notes):
        if adjacent_notes in cls.half_step:
            return 1
        if adjacent_notes in cls.whole_step:
            return 2

class BasicMusicTheory(AdjacentNotes):

    heptatonic_scale = ('C', 'D', 'E', 'F', 'G', 'A', 'B')

    def get_interval(self, first_note, second_note):
        interval = 0
        while True:
            interval += self.get_adjacent_interval(first_note,
                                                   next_note := self.get_next_adjacent_note(first_note))
            first_note = next_note
            if next_note == second_note:
                break
        return interval
    
    def get_composition(self, root):
        
        degree_sequence = range(1, len(self.heptatonic_scale)+1, 1)
        scale_sequence = {scale: degree for scale, degree in zip(self.heptatonic_scale, degree_sequence)}
        triad_mask = slice(0, (3-1)*2+1, 2)
        
        scale_degree_mappping = InvertableMapping(scale_sequence, degree_sequence)

        offset = scale_degree_mappping.map(root) - scale_degree_mappping.map('C')

        heptatonic_scale = deque(self.heptatonic_scale)
        heptatonic_scale.rotate(-offset)
        
        compositions = tuple(heptatonic_scale)[triad_mask]
        
        return compositions



class String(BasicMusicTheory):
    node = namedtuple('Node', 'flat, note')
    
    def __init__(self, root):
        self.root = root
    @property
    def nodes(self):
        guitar_record = Record('notes', 'intervals')
        # 1. For same notes.
        guitar_record.write('notes', self.root)
        guitar_record.write('intervals', 0)
        # 2. For different notes.
        note = self.root
        while True:

            next_note = self.get_next_adjacent_note(note)
            
            guitar_record.write('notes', next_note)
            guitar_record.write('intervals', self.get_adjacent_interval(note, next_note))

            if next_note == self.root:
                break

            note = next_note
        
        notes, intervals = guitar_record.read('notes'), guitar_record.read('intervals')
        flats = tuple(accumulate(intervals))
        return tuple(self.node(flat, note) for flat, note in zip(flats,
                                                                 notes))

class Guitar(String):

    string_index = ('1', '2', '3', '4', '5', '6')
    normal_roots = ('E', 'B', 'G', 'D', 'A', 'E')
    default_slice = slice(0, 5+1, 1)
    bass_slice = slice(4, 5+1, 1)
    modes = {'default': string_index[default_slice],
             'bass': string_index[bass_slice]}

    def __init__(self, roots = normal_roots):
        root_index_mapping = InvertableMapping(roots, self.string_index)
        self.roots = roots
        self.__strings = {index: String(root_index_mapping.map(index)) for index in self.string_index}

    @property
    def strings(self):
        return self.__strings

    def show_fingerboard(self, chord, mode = 'default'):
        compositions = self.get_composition(chord)
        Display.for_fingerboard(self.strings, compositions, self.modes[mode])