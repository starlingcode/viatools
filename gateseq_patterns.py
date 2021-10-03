import json
import struct

class GateseqPatterns:

    def __init__(self):
 
        self.patterns = {}
        self.pattern_set = []
        self.pattern_dir = './gateseq/'
        self.output_dir = './binaries/'

    def load_pattern_set(self, slug='original'):

        with open(self.pattern_dir + 'local_manifest.json') as jsonfile:
            local_manifest = json.load(jsonfile)

        with open(self.pattern_dir + 'remote_manifest.json') as jsonfile:
            remote_manifest = json.load(jsonfile)
        
        manifest = {**remote_manifest, **local_manifest}

        self.pattern_set = manifest[slug]

        for number, tag in enumerate(self.pattern_set):
            self.load_pattern(tag, number, self.pattern_dir + 'patterns/')

    def load_pattern(self, tag, index, pattern_path):
         
        if self.pattern_set[index] in self.patterns:
            self.patterns.pop(self.pattern_set[index])
        self.pattern_set[index] = tag

        with open(pattern_path + tag + '.json') as jsonfile:    
            pattern = json.load(jsonfile)
            self.patterns[tag] = {}
            self.patterns[tag]['sequences'] = []
            for recipe in pattern:
                self.add_sequence(tag, recipe)
            self.patterns[tag]['index'] = index    

    def add_sequence(self, tag, recipe):
        if len(self.patterns[tag]['sequences']) < 16:
            sequence = {}
            sequence['recipe'] = recipe
            sequence['rendered'] = self.decode_recipe(recipe) 
            sequence['density'] = self.get_density(recipe)
            sequence['length'] = len(sequence['rendered'])
            self.patterns[tag]['sequences'].append(sequence)
            self.patterns[tag]['sequences'].sort(key=lambda x: x['density'])
            return True
        else:
            return False

    def remove_sequence(self, tag, index):
        self.patterns[tag]['sequences'].pop(index)

    def get_density(self, recipe):
        pattern = self.decode_recipe(recipe)
        ons = 0
        steps = 0
        for event in pattern:
            if int(event) == 1:
                ons += 1
            steps += 1
        return ons/steps

    def decode_recipe(self, recipe):
        if str(recipe[0]).isdigit():
            sequence = self.bjorklund(recipe[0], recipe[1])
        elif '_' in recipe[0] or '^' in recipe[0]:
            sequence = recipe[0].replace('_', '0')
            sequence = sequence.replace('^', '1')
        int_sequence = []
        for step in sequence:
            int_sequence.append(int(step))
        return int_sequence
            
    def pack_binary(self):
        
        structs = []
        for tag in self.pattern_set:
            structs.append(self.patterns[tag])

        packer = struct.Struct('<16I16I')
        compiled_structs = []
        binary_offset = 32 * 8
        for pattern in structs:
            pack = []
            for sequence in pattern['sequences']:
                binary_offset += int(sequence['length'])
                pack.append(binary_offset)
            for sequence in pattern['sequences']:
                pack.append(sequence['length'])
            compiled_structs.append(packer.pack(*pack))
        for pattern in structs:
            for sequence in pattern['sequences']:
                packer = struct.Struct('<%dI' % sequence['length'])
                compiled_structs.append(packer.pack(*sequence['rendered']))
        
        with open(self.output_dir + 'gateseqpatterns.bin', 'wb') as outfile:
            for chunk in compiled_structs:
                outfile.write(chunk)
    

# muah ha ha ha catfish will not be free from this garden of horror and papa is the evil genius in contol muah ha ha ha 
        
    # from https://github.com/brianhouse/bjorklund
    def bjorklund(self, pulses, steps):
        steps = int(steps)
        pulses = int(pulses)
        if pulses > steps:
            raise ValueError
        if pulses == 0:
            zero_pad = []
            for i in range(0, steps):
                zero_pad.append(0)
            return zero_pad
        pattern = []
        counts = []
        remainders = []
        divisor = steps - pulses
        remainders.append(pulses)
        level = 0
        while True:
            counts.append(divisor / remainders[level])
            remainders.append(divisor % remainders[level])
            divisor = remainders[level]
            level = level + 1
            if remainders[level] <= 1:
                break
        counts.append(divisor)

        def build(level):
            if level == -1:
                pattern.append(0)
            elif level == -2:
                pattern.append(1)
            else:
                for i in range(0, int(counts[level])):
                    build(level - 1)
                if remainders[level] != 0:
                    build(level - 2)

        build(level)
        i = pattern.index(1)
        pattern = pattern[i:] + pattern[0:i]
        return pattern

