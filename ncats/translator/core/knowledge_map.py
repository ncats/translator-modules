#!/usr/bin/env python

import importlib
from copy import deepcopy
from pprint import pprint


"""
This script iterates through the inventory of NCATS Translator Modules
to extract and compile an external catalog of associated BioLink Model metadata.

The initial catalog captures a ReasonerAPI 'predicate' inventory, i.e. something like:

{
  "chemical_substance": {
    "gene": [
      "directly_interacts_with",
      "decreases_activity_of"
    ]
  }
}

Where the input BioLink Model concept 'category' is a top level node,
the output Biolink Model concept 'category' is at the  2nd level node,
and  the leaves of the  tree are the associated BioLink Model predicates.

"""

import fire

DEBUG = False


class KnowledgeMap:

    _the_knowledge_map = None

    @classmethod
    def get_the_knowledge_map(cls):
        if not cls._the_knowledge_map:
            cls._the_knowledge_map = KnowledgeMap()
        return cls._the_knowledge_map

    def __init__(self):
        self.kmap = {}
        self.known_categories: set = set()
        self.known_predicates: set = set()
        self.load()

    def load(self):
        ntm = importlib.import_module('ncats.translator.modules')
        for input_category in ntm._input_categories:

            if DEBUG:
                print("Input Category:\t", input_category)

            if input_category not in self.kmap:
                self.kmap[input_category] = {}

            input_package_name = input_category.replace(' ','_')

            # the Reasoner API uses snake_case category names...so record the categories thus
            self.known_categories.add(input_package_name)

            input_package = \
                importlib.import_module(
                    '.'+input_package_name,
                    'ncats.translator.modules'
                )

            for output_category in input_package._output_categories:

                if DEBUG:
                    print("\tOutput Category:\t", output_category)

                if output_category not in self.kmap[input_category]:
                    self.kmap[input_category][output_category] = []

                output_package_name = output_category.replace(' ', '_')

                # the Reasoner API uses snake_case category names...so record the categories thus
                self.known_categories.add(output_package_name)

                output_package = \
                    importlib.import_module(
                        '.'+output_package_name,
                        input_package.__name__
                    )
                for module_name in output_package._modules:

                    if DEBUG:
                        print("\t\tModule:\t", module_name)

                    module = \
                        importlib.import_module(
                            '.' + module_name,
                            output_package.__name__
                        )
                    metadata = module.metadata()

                    if DEBUG:
                        print("\t\t\tMetadata:\n")
                        pprint(metadata)

                    if metadata.relationship not in self.kmap[input_category][output_category]:
                        self.kmap[input_category][output_category].append(metadata.relationship)
                        self.known_predicates.add(metadata.relationship)

    def predicates(self):
        return deepcopy(self.kmap)

    def dump(self):
        pprint(self.kmap)

    def known_category(self, category) -> bool:
        if category in self.known_categories:
            return True
        else:
            return False

    def known_predicate(self, predicate) -> bool:
        if predicate in self.known_predicates:
            return True
        else:
            return False


def main():
    fire.Fire(KnowledgeMap)


if __name__ == '__main__':
    main()
