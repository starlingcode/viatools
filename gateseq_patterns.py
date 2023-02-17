import struct
from viatools.via_resource import ViaResource, ViaResourceSet

class GateseqPattern(ViaResource):

    def load(self, json_path):
        self.pattern_size = 16
        if not super().load(json_path):
            return False
        self.sorted = True
        if 'sorted' in self.data:
            if self.data['sorted'] is False:
                self.sorted = False
        self.sort()
        return True

    def save(self, json_path):
        self.pad_to_length()
        super().save(json_path)

    def add_data(self, recipe, idx=None):
        if idx:
            self.data['data'].insert(idx, recipe)
        else:
            self.data['data'].append(recipe)
            self.sort()
            insert_idx = len(self.data['data']) - 1
            return insert_idx

    def clear_data(self):
        old_data = self.data['data']
        self.data['data'] = [[1,1]]
        return old_data

    def reorder_data(self, idx_to_move, destination):
        self.data['data'].insert(destination, self.data['data'].pop(idx_to_move))

    def reload_data(self, data_copy):
        self.data['data'] = []
        for ratio in data_copy:
            self.data['data'].append(ratio)

    def remove_data(self, index):
        self.data['data'].pop(index)

    def get_length(self, seq_idx):
        self.bake()
        return len(self.baked)

    def get_data(self):
        data = []
        for recipe in self.data['data']:
            data.append(recipe)
        return data

    def get_recipe(self, seq_idx):
        return self.data['data'][seq_idx]

    def update_length(self, seq_idx, length):
        if self.is_euclidean_recipe(self.data['data'][seq_idx]):
            self.data['data'][seq_idx] = self.euclidean_to_bool(self.data['data'][seq_idx])
        current_length = len(self.data['data'][seq_idx])
        if current_length >= length:
            self.data['data'][seq_idx] = self.data['data'][seq_idx][0:length]
        else:
            for i in range(current_length, length):
                self.data['data'][seq_idx].append(False)
        save_me = self.data['data'][seq_idx]
        #TODO sorted/unsorted
        self.sort()
        return self.data['data'].index(save_me)

    def update_step(self, seq_idx, step_idx, state):
        if self.is_euclidean_recipe(self.data['data'][seq_idx]):
            self.data['data'][seq_idx] = self.euclidean_to_bool(self.data['data'][seq_idx])
        self.data['data'][seq_idx][step_idx] = state
        save_me = self.data['data'][seq_idx]
        #TODO sorted/unsorted
        self.sort()
        return self.data['data'].index(save_me)

    def reload_recipe(self, seq_idx, recipe):
        self.data['data'][seq_idx] = recipe
        self.sort()

    def bake(self):
        self.pad_to_length()
        self.baked = []
        for recipe in self.data['data']:
            self.baked.append(self.expand_sequence(recipe))

    def update_sorted(self, is_sorted):
        self.data['sorted'] = is_sorted
        self.sorted = is_sorted
        old_order = []
        for pattern in self.data['data']:
            old_order.append(pattern)
        self.sort()
        return old_order

    def sort(self):
        if self.sorted:
            self.data['data'].sort(key=self.get_density)

    def get_density(self, recipe):
        pattern = self.expand_sequence(recipe)
        return pattern.count(1)/len(pattern)

    def pad_to_length(self):

        self.data['expanded_data'] = []

        if self.data['data'] == []:
            self.data['data'] = [[0,1],[1,1]]

        if len(self.data['data']) < self.pattern_size:
            out_size = self.pattern_size
            #TODO copied from sync3_scales.py 
            relative_indices = []
            for idx in range(0, len(self.data['data'])):
                rel = idx * (out_size/len(self.data['data']))
                rel += (out_size - 1) - (len(self.data['data']) - 1) * (out_size/len(self.data['data']))
                relative_indices.append(rel)
            to_add = 0
            for notch in range(0, int(out_size)):
                self.data['expanded_data'].append(self.data['data'][to_add])
                if notch >= relative_indices[to_add]:
                    to_add += 1
        else:
            for pattern in self.data['data']:
                self.data['expanded_data'].append(pattern)

    def get_name(self, idx):
        sequence = self.data['data'][idx]
        if self.is_euclidean_recipe(sequence):
            return '%s/%s' % (sequence[0], sequence[1])
        else:
            return '!%s/%s!' % (str(sequence.count(True)), str(len(sequence)))

    def is_euclidean_recipe(self, recipe):
        if str(recipe[0]).isdigit():
            return True
        else:
            return False

    def expand_sequence(self, recipe):
        if self.is_euclidean_recipe(recipe):
            sequence = self.expand_euclidean(recipe[0], recipe[1])
        else: 
            sequence = self.expand_bool(recipe)
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

    def euclidean_to_bool(self, recipe):
        expanded = self.expand_euclidean(recipe[0], recipe[1])
        new_seq = []
        for step in expanded:
            if step == 1:
                new_seq.append(True)
            else:
                new_seq.append(False)
        return new_seq


    def expand_bool(self, recipe):
        sequence = []
        for step in recipe:
            if step is True:
                sequence.append(1)
            else:
                sequence.append(0)
        return sequence


class GateseqPatternSet(ViaResourceSet):

    def __init__(self, resource_dir, slug):
        super().__init__(GateseqPattern, slug, resource_dir, resource_dir + 'patterns/')
        self.output_dir = resource_dir + 'binaries/'            
        self.pattern_size = 16

    def pack_binary(self, write_dir=None, title=None):
        if not title:
            title=self.slug 
        if not write_dir:
            write_dir = self.output_dir
        packer = struct.Struct('<%dI%dI' % (self.pattern_size, self.pattern_size))
        compiled_structs = []
        binary_offset = self.pattern_size * 2 * 8
        for pattern in self.resources:
            pattern.bake()
            pack = []
            for sequence in pattern.baked:
                pack.append(binary_offset)
                binary_offset += len(sequence)
            for sequence in pattern.baked:
                pack.append(len(sequence))
            compiled_structs.append(packer.pack(*pack))
        for pattern in self.resources:
            for sequence in pattern.baked:
                packer = struct.Struct('<%dI' % len(sequence))
                compiled_structs.append(packer.pack(*sequence))
        
        resource_path = write_dir + title + '.gateseq'

        with open(resource_path, 'wb') as outfile:
            for chunk in compiled_structs:
                outfile.write(chunk)

        return resource_path   
