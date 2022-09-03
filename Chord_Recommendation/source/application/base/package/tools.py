class Record():
    '''Generate lists simultaneously to record instances.
    '''
    def __init__(self, *objects__):
        self.objects__ = objects__
        self.records = {object__: [] for object__ in objects__}
    
    def reset(self):
        self.records = dict.fromkeys(self.objects__, [])

    def write(self, object__, instance):
        self.records[object__].append(instance)
    
    def read(self, object__):
        return self.records[object__]

class InvertableMapping():
    def __init__(self, domain, codomain):
        self.__domain = domain
        self.__codomain = codomain
        self.from_domain_to_codomain = {key: value for key, value in zip(self.__domain, self.__codomain)}
        self.from_codomain_to_domain = {key: value for key, value in zip(self.__codomain, self.__domain)}

    def map(self, element):
        if element in self.__domain:
            return self.from_domain_to_codomain[element]
        if element in self.__codomain:
            return self.from_codomain_to_domain[element]