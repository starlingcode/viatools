import struct
from viatools.via_resource import ViaResource, ViaResourceSet
import json

class Wavetable(ViaResource):

    def __init__(self, table_file, slug, slope_file):
        self.slug = slug
        self.load(table_file)
        self.slope_file = slope_file

    def load(self, json_path): 
        with open(json_path) as json_file:
            self.data = json.load(json_file)[self.slug]

    def save(self, save_path):
        with open(save_path, 'r') as save_file:
            save_data = json.load(save_file)
        save_data[self.slug] = self.data
        with open(save_path, 'w') as save_file:
            save_data = json.load(save_file)
        json.dump(save_data, save_file)

    # recipe is [attack_table_slug, release_table_slug]
    def update_data(self, recipe):
        self.data = recipe
        self.sort()

class WavetableSet(ViaResourceSet):

    def __init__(self, resource_dir, slug, table_file, slope_file):
        self.table_file = table_file
        self.slope_file = slope_file
        super().__init__(Wavetable, slug, resource_dir, None)
        self.output_dir = resource_dir + 'binaries/'            

    def load_resource(self, slug):
        return Wavetable(self.table_file, slug, self.slope_file)

    def pack_binary(self, write_dir=None): 
        if not write_dir:
            write_dir = self.output_dir

        with open(self.slope_file) as jsonfile:
            slope_dict = json.load(jsonfile)

        slope_sets_used = set()
        for table in self.resources:
            slope_sets_used.add(table.data[0]) 
            slope_sets_used.add(table.data[1]) 

        # 'compile' slopes and store offsets in units of 16 bit half words
        offset = 0
        packer = struct.Struct('<257h')
        compiled_slopes = []
        slope_data = {}
        for slope_set in slope_sets_used:
            slope_data[slope_set] = {}
            slope_data[slope_set]['offset'] = offset
            slope_data[slope_set]['size'] = len(slope_dict[slope_set])
            for slope in slope_dict[slope_set]:
                offset += 257
                compiled_slopes.append(packer.pack(*slope))

        # 'compile' table def structs using above slope offsets
        compiled_structs = []
        for table in self.resources:
            packer = struct.Struct('<IIII')
            pack = []
            slope = table.data[0]
            pack.append(slope_data[slope]['offset'])
            slope = table.data[1]
            pack.append(slope_data[slope]['offset'])
            pack.append(257)
            pack.append(slope_data[slope]['size'])
            compiled_structs.append(packer.pack(*pack))
        
        resource_path = write_dir + self.slug + '.' + self.output_dir.split('/')[-2] + 'tables'

        with open(resource_path, 'wb') as outfile:
            for chunk in compiled_structs + compiled_slopes:
                outfile.write(chunk)

        return resource_path   
