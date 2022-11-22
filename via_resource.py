import json
import os

class ViaResource:
    
    def __init__(self, json_path=None):
        if json_path:
            self.load(json_path)

    def load(self, json_path): 
        with open(json_path) as json_file:
            data = json.load(json_file)
            if 'title' in data and 'data' in data:
                self.data = data['data']
            else:
                self.data = data 

    def save(self, save_path):
        with open(save_path, 'w') as save_file:
            json.dump(self.data, save_file)
    
class ViaResourceSet(ViaResource):
    
    # self.data is a list of slugs
    # self.resources is a list of resources loaded from those slugs

    def __init__(self, resource_type, slug, resource_set_dir, resource_dir):
        super().__init__(resource_set_dir + slug + '.json')
        self.resource_type = resource_type
        self.resource_dir = resource_dir
        self.resource_set_dir = resource_set_dir
        self.init_resources()
        self.slug = slug
   
    def save_set(self, slug):
        self.save(self.resource_set_dir + slug + '.json')
        self.slug = slug 

    def load_set(self, slug):
        self.load(self.resource_set_dir + slug + '.json')
        self.slug = slug
        self.init_resources()

    def init_resources(self):
        self.resources = []
        for slug in self.data:
            self.add_resource(self.load_resource(slug))
    
    def add_resource(self, resource):
        self.resources.append(resource)

    def load_resource(self, slug):
        return self.resource_type(self.resource_dir + slug + '.json')

    def replace_resource(self, slug, index):
        self.resources[index] = self.load_resource(slug)
        self.data[index] = slug

    def save_resource(self, slug, index):
        self.resources[index].save(self.resource_dir + slug + '.json')
        self.data[index] = slug

    def make_title_maps(self, slugs, slug_path):
        slug_to_title = {}
        title_to_slug = {}
        for slug in slugs:
            with open(slug_path + slug + '.json') as thefile:
                title = json.load(thefile)['title']
                slug_to_title[slug] = title
                title_to_slug[title] = slug
        return slug_to_title, title_to_slug

    def get_available_resource_sets(self):
        sets = []
        for root, dirs, files in os.walk(self.resource_set_dir):
            for file in files:
                sets.append(file.replace('.json', ''))
            break
        return self.make_title_maps(sets, self.resource_set_dir)

    def get_available_resources(self):
        resources = []
        for root, dirs, files in os.walk(self.resource_dir):
            for file in files:
                resources.append(file.replace('.json', ''))
            break
        return self.make_title_maps(resources, self.resource_dir)

    

