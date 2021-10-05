import struct
from viatools.via_resource import ViaResource, ViaResourceSet

class GateseqPattern(ViaResource):

    def load(self, json_path):
        super().load(json_path)
        self.sort()

    def add_data(self, recipe):
        self.data.append(recipe)
        self.sort()

    def remove_data(self, index):
        self.data.pop(index)

    def bake_data(self, index):
        self.baked = []
        for recipe in self.data:
            self.baked.append(self.expand_sequence(recipe))

    def sort(self):
        self.data.sort(key=self.get_density)

    def get_density(self, recipe):
        pattern = self.expand_sequence(recipe)
        return pattern.count(1)/len(pattern)

    def expand_sequence(self, recipe):
        if str(recipe[0]).isdigit():
            sequence = self.expand_euclidean(recipe[0], recipe[1])
        elif '_' in recipe[0] or '^' in recipe[0]: 
            sequence = self.expand_text(recipe[0], recipe[1])
        int_sequence = []
        for step in sequence:
            int_sequence.append(int(step))
        return int_sequence

    # from https://github.com/brianhouse/bjorklund
    def expand_euclidean(self, pulses, steps):
        steps = int(steps)
        pulses = int(pulses)
        if pulses > steps:
            raise ValueError
        if pulses == 0:
            zero_pad = []
            for i in range(0, steps):
                zero_pad.append(0)
            return zero_pad
        sequence = []
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
                sequence.append(0)
            elif level == -2:
                sequence.append(1)
            else:
                for i in range(0, int(counts[level])):
                    build(level - 1)
                if remainders[level] != 0:
                    build(level - 2)

        build(level)
        i = sequence.index(1)
        sequence = sequence[i:] + sequence[0:i]
        return sequence

    def expand_text(self, recipe):
        sequence = recipe[0].replace('_', '0')
        sequence = sequence.replace('^', '1')
        return sequence

class GateseqPatternSet(ViaResourceSet):

    def __init__(self, resource_dir, output_dir, slug):
        super().__init__(GateseqPattern, slug, resource_dir, resource_dir + 'patterns/')
        self.output_dir = output_dir            

    def pack_binary(self):
        
        packer = struct.Struct('<16I16I')
        compiled_structs = []
        binary_offset = 32 * 8
        for pattern in self.resources:
            pack = []
            for sequence in pattern.baked:
                binary_offset += len(sequence)
                pack.append(binary_offset)
            for sequence in pattern.baked:
                pack.append(len(sequence))
            compiled_structs.append(packer.pack(*pack))
        for pattern in self.resources:
            for sequence in pattern.baked:
                packer = struct.Struct('<%dI' % len(sequence))
                compiled_structs.append(packer.pack(*sequence))
        
        with open(self.output_dir + 'gateseqpatterns.bin', 'wb') as outfile:
            for chunk in compiled_structs:
                outfile.write(chunk)
