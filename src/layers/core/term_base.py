from typing import Callable


class TermBase:
    def __init__(self, name:str, attributes:list[str]=list(), function:Callable=lambda x:x):
        self._name = name
        self._attributes = attributes
        self._function = function
        pass
    
    @property
    def name(self):
        return self._name
    
    @property
    def attributes(self):
        return self._attributes
    
    def __str__(self):
        return self._name
    
    def __len__(self):
        return len(self._attributes)

    def get_multiplier(self, *args):
        if len(args) == len(self._attributes):
            return self._function(*args)

class SequentialTerms:
    def __init__(self, terms:list[TermBase]=list()):
        self._terms = terms
    
    def __str__(self):
        return f'SequentialTerms({[str(x) for x in self._terms]})'
    
    # TODO: resource packer
    def iterate_terms(self, ref_obj):
        results= list()
        for term in self._terms:
            arguments = list()
            for attribute in term.attributes:
                arguments.append(ref_obj.attribute)
            results.append(term.get_multiplier(*arguments))
        return results

    def attach(self, new_term:TermBase):
        self._terms.append(new_term)
        
