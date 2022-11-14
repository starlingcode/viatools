import struct
import math
import numpy as np
from viatools.via_resource import ViaResource, ViaResourceSet


class Osc3Quantization(ViaResource):

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

    def pad_to_length(self):

        if self.data['chords'] == []:
            self.data['chords'] = [[0,0]]

        if len(self.data['chords']) < 16:
            out_size = 16
            #TODO copied from sync3_scales.py 
            relative_indices = []
            for idx in range(0, len(self.data['chords'])):
                rel = idx * (out_size/len(self.data['chords']))
                rel += (out_size - 1) - (len(self.data['chords']) - 1) * (out_size/len(self.data['chords']))
                relative_indices.append(rel)
            new_data = []
            to_add = 0
            for notch in range(0, int(out_size)):
                print(new_data)
                new_data.append(self.data['chords'][to_add])
                if notch >= relative_indices[to_add]:
                    to_add += 1
            self.data['chords'] = new_data

    def expand_scale(self, data):
        baked = {}

        data['notes'].sort()

        exp_offsets = [] 
        for note in data['notes']:
            exp_offsets.append(2.0**(note/12.0))
        print(exp_offsets)
        degrees = []
        for pitch_class in range(0, 12):
            exp_offset = 2.0**(pitch_class/12.0)
            print(exp_offset)
            min_diff_index = 0
            min_diff = 100
            for idx, offset in enumerate(exp_offsets):
                diff = abs(offset - exp_offset)
                print(diff)
                if diff < min_diff:
                    min_diff = diff
                    min_diff_index = idx
            degrees.append(min_diff_index) 
        baked['degrees'] = degrees
        print(degrees)
        print('Degrees length: %d' % len(degrees))

        scale_out = []
        scale12 = []
        for degree in degrees:
            scale12.append(data['notes'][degree])
        for index in range(0, 128):
            index_note = (index - 4) % 12
            index_octave = int(((index - 4) / 12)) * 12
            if index - 4 < 0:
                index_note = 0
            scale_out.append(index_octave + scale12[index_note])
        baked['scale'] = scale_out
        print(scale_out)
        print('Degrees length: %d' % len(scale_out))
        
        intervals = []
        notes = data['notes']
        for i in range(0, 12 - len(notes)):
            intervals.append(0)
        for note in notes:
            intervals.append(-12 + note)
        for note in notes:
            intervals.append(note)
        for note in notes:
            intervals.append(12 + note)
        intervals.append(24 + notes[0])
        for i in range(0, 37 - len(intervals)):
            intervals.append(0)
        baked['intervals'] = intervals
        print(intervals)
        print('Degrees length: %d' % len(intervals))

        chords = []
        for chord in data['chords']:
            chords.append(chord[0])
            chords.append(chord[1])
        # Double the last chord
        chords.append(chord[0])
        chords.append(chord[1])
        baked['chords'] = chords
        print(chords)
        print('Degrees length: %d' % len(chords))
        
        return baked

class Osc3QuantizationSet(ViaResourceSet):

    def __init__(self, resource_dir, slug):
        super().__init__(Osc3Quantization, slug, resource_dir, resource_dir + 'quantizations/')
        self.output_dir = resource_dir + 'binaries/'            
        self.slug = slug

    def bake(self):
        for resource in self.resources:
            resource.bake()

    def pack_binary(self, write_dir=None):
        if not write_dir:
            write_dir = self.output_dir
        packer = struct.Struct('<%dI%dI%dI%dI' % (128, 37, 12, 34))
        compiled_structs = []
        for resource in self.resources:
            resource.bake()
            scale = resource.baked
            pack = []
            for number in scale['scale']:
                pack.append(number & 0xFFFFFFFF)
            for number in scale['intervals']:
                pack.append(number & 0xFFFFFFFF)
            for number in scale['degrees']:
                pack.append(number & 0xFFFFFFFF) 
            for number in scale['chords']:
                pack.append(number & 0xFFFFFFFF)
            compiled_structs.append(packer.pack(*pack))

        resource_path = write_dir + self.slug + '.osc3'

        with open(resource_path, 'wb') as outfile:
            for chunk in compiled_structs:
                outfile.write(chunk)

        return resource_path
