#!/usr/bin/env python

import importlib

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

    def __init__(self):
        self.kmap = {}

    def load(self):
        ntm = importlib.import_module('ncats.translator.modules')
        for input_category in ntm._input_categories:
            print("Input Category:\t", input_category)
            input_package_name = input_category.replace(' ','_')
            input_package = \
                importlib.import_module(
                    '.'+input_package_name,
                    'ncats.translator.modules'
                )
            for output_category in input_package._output_categories:
                print("\tOutput Category:\t", output_category)
                output_package_name = output_category.replace(' ', '_')
                output_package = \
                    importlib.import_module(
                        '.'+output_package_name,
                        input_package.__name__
                    )
                for module_name in output_package._modules:
                    print("\t\tModule:\t", module_name)

def main():
    fire.Fire(KnowledgeMap)


if __name__ == '__main__':
    main()
