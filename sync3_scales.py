import sys
from shutil import copyfile
import requests
import os
import struct
import json
import numpy as np

class Sync3Scales:

    def __init__(self):

        self.fill_modes = {
                        'octave': self.fill_octave,
                        '2octave': self.fill_2octave,
                        'tritave': self.fill_tritave,
                        'expand': self.fill_expand
                    }    

        self.text_out = ''
        self.scale_dir = './sync3/'
        self.output_dir = './binaries/'
        self.scales = {}        
        self.scales_backup = {}
        self.scale_set = []
        self.scale_set_backup = []

    def load_scale_set(self, slug='original'):

        self.scales = {}

        with open(self.scale_dir + 'local_manifest.json') as jsonfile:
            local_manifest = json.load(jsonfile)

        with open(self.scale_dir + 'remote_manifest.json') as jsonfile:
            remote_manifest = json.load(jsonfile)
        
        manifest = {**remote_manifest, **local_manifest}

        self.scale_set = manifest[slug]
        self.scale_set_backup = manifest[slug]

        for number, tag in enumerate(manifest[slug]):
            self.load_scale(tag, number, self.scale_dir + 'scales/') 
            self.load_scale_backup(tag, number, self.scale_dir + 'scales/') 

    def load_scale(self, tag, index, scale_path):
        if self.scale_set[index] in self.scales:
            self.scales.pop(self.scale_set[index])
        self.scale_set[index] = tag
        
        with open(scale_path + tag + '.json') as jsonfile:    
            scale = json.load(jsonfile)
            self.scales[tag] = {}
            self.scales[tag]['seed_ratios'] = []
            for ratio in scale['seed_ratios']:
                self.add_seed_ratio(tag, ratio[0], ratio[1])
            self.scales[tag]['fill_method'] = scale['fill_method']
            self.scales[tag]['index'] = index

    def load_scale_backup(self, tag, index, scale_path):
        self.scale_set[index] = tag 
        with open(scale_path + tag + '.json') as jsonfile:    
            scale = json.load(jsonfile)
            self.scales_backup[tag] = {}
            self.scales_backup[tag]['seed_ratios'] = scale['seed_ratios']
            self.scales_backup[tag]['fill_method'] = scale['fill_method']
            self.scales_backup[tag]['index'] = index

    def save_scale(self, scale):

        with open(self.dir + scale + '.json', 'w') as jsonfile:
            scale_output = scale
            scale_output.pop('index')
            scale_output.pop('numerators')
            scale_output.pop('denominators')
            scale_output.pop('precalcs')
            scale_output.pop('keys')
            json.dump(scale_output, jsonfile)

    def save_scale_set(self, scale_set_slug):
        
        scale_sets = {}

        with open(self.dir + self.manifest, 'r') as manifest_file: 
            scale_sets = json.load(manifest_file)
 
        scale_sets[scale_set_slug] = self.scale_set

        with open(self.dir + self.manifest, 'w') as manifest_file: 
            json.dump(manifest_file, scale_sets)

        #TODO make scales object a list and add slug/filepath to dict
    def add_seed_ratio(self, scale_id, numerator, denominator):
        gcd = np.gcd(numerator, denominator)
        ratio = [int(numerator/gcd), int(denominator/gcd)]
        if ratio not in self.scales[scale_id]['seed_ratios']:
            self.scales[scale_id]['seed_ratios'].append(ratio)
            self.scales[scale_id]['seed_ratios'].sort(key=lambda x: x[0]/x[1])
            return True
        else:
            return False

# 

    def fill_octave(self, ratios):

        numerators = []
        denominators = []

        for ratio in ratios:
            if (ratio[0] % 4 == 0):
                numerators.append(int(ratio[0] / 4))
                denominators.append(int(ratio[1]))
            elif (ratio[0] % 2 == 0):
                numerators.append(int(ratio[0] / 2))
                denominators.append(int(ratio[1] * 2))
            else:
                numerators.append(int(ratio[0]))
                denominators.append(int(ratio[1] * 4))

        for ratio in ratios:
            if (ratio[0] % 2 == 0):
                numerators.append(int(ratio[0] / 2))
                denominators.append(int(ratio[1]))
            else:
                numerators.append(int(ratio[0]))
                denominators.append(int(ratio[1] * 2))

        for ratio in ratios:
            numerators.append(int(ratio[0]))
            denominators.append(int(ratio[1]))

        for ratio in ratios:
            if (ratio[1] % 2 == 0):
                numerators.append(int(ratio[0]))
                denominators.append(int(ratio[1] / 2))
            else:
                numerators.append(int(ratio[0] * 2))
                denominators.append(int(ratio[1]))

        return numerators, denominators

    def fill_tritave(self, ratios):

        numerators = []
        denominators = []

        for ratio in ratios:
            if (ratio[0] % 9 == 0):
                numerators.append(int(ratio[0] / 9))
                denominators.append(int(ratio[1]))
            elif (ratio[0] % 3 == 0):
                numerators.append(int(ratio[0] / 3))
                denominators.append(int(ratio[1] * 3))
            else:
                numerators.append(int(ratio[0]))
                denominators.append(int(ratio[1] * 9))

        for ratio in ratios:
            if (ratio[0] % 3 == 0):
                numerators.append(int(ratio[0] / 3))
                denominators.append(int(ratio[1]))
            else:
                numerators.append(int(ratio[0]))
                denominators.append(int(ratio[1] * 3))

        for ratio in ratios:
            numerators.append(int(ratio[0]))
            denominators.append(int(ratio[1]))

        for ratio in ratios:
            if (ratio[1] % 3 == 0):
                numerators.append(int(ratio[0]))
                denominators.append(int(ratio[1] / 3))
            else:
                numerators.append(int(ratio[0] * 3))
                denominators.append(int(ratio[1]))

        return numerators, denominators

    def fill_2octave(self, ratios):

        numerators = []
        denominators = []

        for ratio in ratios:

            if (ratio[0] % 16 == 0):
                numerators.append(int(ratio[0] / 16))
                denominators.append(int(ratio[1]))
            elif (ratio[0] % 8 == 0):
                numerators.append(int(ratio[0] / 8))
                denominators.append(int(ratio[1] * 2))
            elif (ratio[0] % 4 == 0):
                numerators.append(int(ratio[0] / 4))
                denominators.append(int(ratio[1] * 4))
            elif (ratio[0] % 2 == 0):
                numerators.append(int(ratio[0] / 2))
                denominators.append(int(ratio[1] * 8))
            else:
                numerators.append(int(ratio[0]))
                denominators.append(int(ratio[1] * 16))

        for ratio in ratios:

            if (ratio[0] % 4 == 0):
                numerators.append(int(ratio[0] / 4))
                denominators.append(int(ratio[1]))
            elif (ratio[0] % 2 == 0):
                numerators.append(int(ratio[0] / 2))
                denominators.append(int(ratio[1] * 2))
            else:
                numerators.append(int(ratio[0]))
                denominators.append(int(ratio[1] * 4))

        for ratio in ratios:
            numerators.append(int(ratio[0]))
            denominators.append(int(ratio[1]))

        for ratio in ratios:

            if (ratio[1] % 4 == 0):
                numerators.append(int(ratio[0]))
                denominators.append(int(ratio[1] / 4))
            elif (ratio[1] % 2 == 0):
                numerators.append(int(ratio[0] * 2))
                denominators.append(int(ratio[1] / 2))
            else:
                numerators.append(int(ratio[0] * 4))
                denominators.append(int(ratio[1]))

        return numerators, denominators

    def fill_expand(self, ratios):

        numerators = []
        denominators = []

        if len(ratios) == 16:
            for ratio in ratios:
                numerators.append(int(ratio[0]))
                denominators.append(int(ratio[1]))
                numerators.append(int(ratio[0]))
                denominators.append(int(ratio[1]))
            print(numerators)
        else:
                
            for ratio in ratios:
                numerators.append(int(ratio[0]))
                denominators.append(int(ratio[1]))
            #TODO: Dirty hack for ints set which has a doubled 1/1 in the middle
            # That got bashed by the "unique seed ratios only"
            # Maybe time for a custom mapping fill method
            while len(numerators) < 32:
                numerators.append(int(ratios[-1][0]))
                denominators.append(int(ratios[-1][1]))

        return numerators, denominators

    def fill_default(self, ratios):

        numerators = []
        denominators = []

        for ratio in ratios:
            numerators.append(int(ratio[0]))
            denominators.append(int(ratio[1]))

        return numerators, denominators

# Scale updating functions
# TODO: render function per scale
    def render(self):

        for scale in self.scales:

            ratios = self.scales[scale]['seed_ratios']

            mode = self.scales[scale]['fill_method']

            numerators, denominators = self.fill_modes[mode](ratios)

            precalcs = []

            for index, denominator in enumerate(denominators):
                precalc = int((2 ** 32) / denominator) % 4294967296
                precalcs.append(precalc)

            ratios_used = set()

            keys = []

            key = 0

            for index, numerator in enumerate(numerators):

                ratio = (numerator, denominators[index])

                if ratio not in ratios_used:

                    ratios_used.add(ratio)
                    key += 1

                keys.append(key)

            self.scales[scale]['numerators'] = numerators
            self.scales[scale]['denominators'] = denominators
            self.scales[scale]['precalcs'] = precalcs
            self.scales[scale]['keys'] = keys

# Export functions

    def pack_binary(self):
        
        structs = []
        for tag in self.scale_set:
            structs.append(self.scales[tag])

        packer = struct.Struct('<32I32I32I32II')
        compiled_structs = []
        for scale in structs:
            print(len(scale['numerators']))
            pack = []
            for number in scale['numerators']:
                pack.append(number)
            for number in scale['denominators']:
                pack.append(number)
            for number in scale['precalcs']:
                pack.append(number) 
            for number in scale['keys']:
                pack.append(number)
            pack.append(0)
            compiled_structs.append(packer.pack(*pack))
        with open(self.output_dir + 'sync3scales.bin', 'wb') as outfile:
            for chunk in compiled_structs:
                outfile.write(chunk)

