import struct
from viatools.via_resource import ViaResource, ViaResourceSet
import json

class Wavetable(ViaResource):

    def __init__(self, table_file, slug, slope_file, max_table_size):
        self.slug = slug
        self.load(table_file)
        self.slope_file = slope_file
        self.max_table_size = max_table_size

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
    
    def expand(self):

        with open(self.slope_file) as slopejson:
            slopes = json.load(slopejson)
            attack_table = slopes[self.data[0]]
            release_table = slopes[self.data[1]]

        tables = []

        if len(attack_table) > self.max_table_size:
            read_table = attack_table[0:self.max_table_size]
        else:
            read_table = attack_table

        for index, table in enumerate(attack_table):

            full_table = []

            for sample in table[:256]:
                full_table.append(int(sample))

            release = release_table[index][1:]

            release.reverse()

            for sample in release:
                full_table.append(int(sample))

            tables.append(full_table)
        
        return tables

class WavetableSet(ViaResourceSet):

    def __init__(self, resource_dir, slug, table_file, slope_file, size_limit_data=None):
        if size_limit_data:
            self.max_table_size = size_limit_data['table_size']
        else:
            self.max_table_size = 9            
        self.table_file = table_file
        self.slope_file = slope_file
        super().__init__(Wavetable, slug, resource_dir, None)
        self.output_dir = resource_dir + 'binaries/'            

    def load_resource(self, slug):
        return Wavetable(self.table_file, slug, self.slope_file, self.max_table_size)

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
        packer = struct.Struct('<257H')
        compiled_slopes = []
        slope_data = {}
        for slope_set in slope_sets_used:
            slope_data[slope_set] = {}
            slope_data[slope_set]['offset'] = offset
            slope_read = slope_dict[slope_set] 
            if len(slope_read) > self.max_table_size:
                slope_read = slope_read[0:self.max_table_size]
            slope_data[slope_set]['size'] = len(slope_read)
            for slope in slope_read:
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
            pack.append(256)
            pack.append(slope_data[slope]['size'])
            compiled_structs.append(packer.pack(*pack))
        
        resource_path = write_dir + self.slug + '.' + self.output_dir.split('/')[-2] + 'tables'

        with open(resource_path, 'wb') as outfile:
            for chunk in compiled_structs + compiled_slopes:
                outfile.write(chunk)

        return resource_path   
