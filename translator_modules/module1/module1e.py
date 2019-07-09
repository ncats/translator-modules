#!/usr/bin/env python3

import fire

# Workflow 2, Module 1E: Gene interactions
from BioLink.biolink_client import BioLinkWrapper
from pprint import pprint

import pandas as pd

from translator_modules.core import Config
from translator_modules.core import Payload


class GeneInteractions(object):

    def __init__(self):
        self.blw = BioLinkWrapper(Config().get_biolink_api_endpoint())
        self.meta = {
            'input_type': {
                'complexity': 'set',
                'id_type': 'HGNC',
                'data_type': 'gene',
            },
            'output_type': {
                'complexity': 'set',
                'id_type': 'HGNC',
                'data_type': 'gene',
            },

            'source': 'Monarch Biolink',
            'predicate': ['blm:interacts with']
        }

    def metadata(self):
        print("""Mod1E Interaction Network metadata:""")
        pprint(self.meta)

    @staticmethod
    # RMB: July 5, 2019 - gene_records is a Pandas DataFrame
    def load_gene_set(gene_records):
        annotated_gene_set = []
        for gene in gene_records:
            annotated_gene_set.append({
                'input_id': gene['hit_id'],
                'sim_input_curie': gene['hit_id'],
                'input_symbol': gene['hit_symbol']
            })
        return annotated_gene_set

    def get_interactions(self, annotated_gene_set):
        results = []
        for gene in annotated_gene_set:
            interactions = self.blw.gene_interactions(gene_curie=gene['sim_input_curie'])
            for assoc in interactions['associations']:
                interaction = \
                    self.blw.parse_association(
                        input_id=gene['sim_input_curie'],
                        input_label=gene['input_symbol'],
                        association=assoc
                    )
                results.append({
                    'input_id': interaction['input_id'],
                    'input_symbol': interaction['input_symbol'],
                    'hit_symbol': interaction['hit_symbol'],
                    'hit_id': interaction['hit_id'],
                    'score': 0,
                })
        return results


class GeneInteractionSet(Payload):

    # TODO
    def __init__(self, input_gene_set_file=None):
        super(GeneInteractionSet, self).__init__(GeneInteractions())

        input_gene_set_df = None
        if input_gene_set_file:
            with open(input_gene_set_file) as stream:
                # assuming it's JSON and it's a record list
                input_gene_set_df = pd.read_json(stream, orient='records')

        # in this case "load gene set" is more like a reformatting function
        self.results = pd.DataFrame().from_records(self.mod.get_interactions(self.mod.load_gene_set(input_gene_set_df.to_dict(orient='records'))))


if __name__ == '__main__':
    fire.Fire(GeneInteractionSet)
