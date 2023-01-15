import json
import os

class ViaResource:
    
    def __init__(self, json_path=None):
        if json_path:
            self.load(json_path)

    def validate(self, json_path):
        try: 
            with open(json_path) as json_file:
                data = json.load(json_file)
                if 'title' not in data:
                    print("Can't find a title field!")
                    return False
        except:
            print("Error loading " + str(json_path))
            return False

        return True 

    def load(self, json_path):
        try: 
            with open(json_path) as json_file:
                data = json.load(json_file)
        except:
            print("Error loading " + str(json_path))
            return False

        self.data = data 

        return True 

    def save(self, save_path):
        with open(save_path, 'w') as save_file:
            json.dump(self.data, save_file)
    
class ViaResourceSet(ViaResource):

    def __init__(self, resource_type, slug, resource_set_dir, resource_dir):
        super().__init__(resource_set_dir + slug + '.json')
        self.resource_type = resource_type
        self.resource_dir = resource_dir
        self.resource_set_dir = resource_set_dir
        self.init_resources()
        self.slug = slug
   
    def save_set(self, slug, description):
        self.data['title'] = slug
        self.data['description'] = description
        self.save(self.resource_set_dir + slug + '.json')
        self.slug = slug 

    def load_set(self, slug):
        self.load(self.resource_set_dir + slug + '.json')
        self.slug = slug
        self.init_resources()

    def init_resources(self):
        self.resources = []
        for slug in self.data['slug_list']:
            self.add_resource(self.load_resource(slug))
    
    def add_resource(self, resource):
        self.resources.append(resource)

    def load_resource(self, slug):
        return self.resource_type(self.resource_dir + slug + '.json')

    def replace_resource(self, slug, index):
        self.resources[index] = self.load_resource(slug)
        self.data['slug_list'][index] = slug

    def save_resource(self, slug, index, description):
        self.resources[index].data['title'] = slug
        self.resources[index].data['description'] = description
        self.resources[index].save(self.resource_dir + slug + '.json')
        self.data['slug_list'][index] = slug

    def make_title_maps(self, slugs, slug_path):
        slug_to_title = {}
        title_to_slug = {}
        for slug in slugs:
            with open(slug_path + slug + '.json') as thefile:
                title = json.load(thefile)['title']
                slug_to_title[slug] = title
                title_to_slug[title] = slug
        return slug_to_title, title_to_slug

    def get_available_resources(self, search_dir=None):
        if not search_dir:
            search_dir = self.resource_dir
        resources = []
        for root, dirs, files in os.walk(search_dir):
            for file in [x for x in files if ".json" in x]:
                if self.validate(os.path.join(root, file)):
                    resources.append(file.replace('.json', ''))
                else:
                    print("Bad file at " + os.path.join(root, file))
            break
        return self.make_title_maps(resources, search_dir)


    def get_available_resource_sets(self):
        return self.get_available_resources(self.resource_set_dir)

    

