import struct
import math
import numpy as np
from viatools.via_resource import ViaResource, ViaResourceSet


class Osc3Scale(ViaResource):

    def load(self, json_path):
        super().load(json_path)

    def add_chord(self, chord):
        self.data['chords'].append(chord)

    def remove_chord(self, index):
        self.data['chords'].pop(index)

    def add_note(self, note):
        if note not in self.data['notes']:
            self.data['notes'].append(note)

    def remove_note(self, note):
        if note in self.data['notes']:
            self.data['notes'].remove(note)

    def bake(self):
        self.baked = self.expand_scale(self.data)

    def expand_scale(self, data):
        baked = {}

        exp_offsets = [] 
        for note in data['notes']:
            exp_offsets.append(note_exp_offset = 2.0**(note/2.0))
        degrees = []
        for pitch_class in range(0, 12):
            exp_offset = 2.0**(pitch_class/2.0)
            min_diff_index = 0
            min_diff = 0
            for idx, offset in enumerate(exp_offsets):
                diff = abs(offset - exp_offset)
                if diff < min_diff:
                    diff = min_diff
                    min_diff_index = idx
            degrees.append(min_diff_index) 
        baked['degrees'] = degrees

        scale_out = []
        for index in range(0, 127):
            index_note = (index - 4) % 12
            index_octave = int(((index - 4) / 12)) * 12
            if index - 4 < 0:
                index_note = 0
            scale_out.append(index_octave + data['notes'][index_note])
        baked['scale'] = scale_out
        
        intervals = []
        for i in range(0, 12 - len(data['notes']):
            intervals.append(0)
        for note in notes:
            intervals.append(-12 + note)
        for note in notes:
            intervals.append(note)
        for note in notes:
            intervals.append(12 + note)
        intervals.append(24 + notes[0])
        for i in (len(intervals, 36)
            intervals.append(0)
        baked['intervals'] = intervals

        chords = []
        for chord in data['chords']:
            chords.append[chord[0]]
            chords.append[chord[1]]
        # Double the last chord
        chords.append[chord[0]]
        chords.append[chord[1]]
        baked['chords'] = chords

class Osc3ScaleSet(ViaResourceSet):

    def __init__(self, resource_dir, slug):
        super().__init__(Osc3Scale, slug, resource_dir, resource_dir + 'scales/')
        self.output_dir = resource_dir + 'binaries/'            
        self.slug = slug

    def bake(self):
        for resource in self.resources:
            resource.bake()

    def pack_binary(self, write_dir=None):
        if not write_dir:
            write_dir = self.output_dir
        packer = struct.Struct('<%dI%dI%dI%dI' % (128, 36, 12, 34))
        compiled_structs = []
        for resource in self.resources:
            resource.bake()
            scale = resource.baked
            pack = []
            for number in scale['scale']:
                pack.append(number)
            for number in scale['intervals']:
                pack.append(number)
            for number in scale['degrees']:
                pack.append(number) 
            for number in scale['chords']:
                pack.append(number)
            pack.append(0)
            compiled_structs.append(packer.pack(*pack))

        resource_path = write_dir + self.slug + '.osc3'

        with open(resource_path, 'wb') as outfile:
            for chunk in compiled_structs:
                outfile.write(chunk)

        return resource_path
