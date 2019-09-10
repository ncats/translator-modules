#!/usr/bin/env python3

# Workflow 2, Module 1E: Gene Interaction

from pprint import pprint

import fire
import pandas as pd
# Workflow 2, Module 1E: Gene interactions
from BioLink.biolink_client import BioLinkWrapper

from BioLink.model import GeneToGeneAssociation, Gene

from translator_modules.core import Config
from translator_modules.core.module_payload import Payload, get_input_gene_data_frame


class GeneInteractions:

    def __init__(self):
        self.blw = BioLinkWrapper(Config().get_biolink_api_endpoint())
        self.meta = {
            'source': 'Monarch Biolink',
            'association': GeneToGeneAssociation.class_name,
            'input_type': {
                'complexity': 'set',
                'category': Gene.class_name,
                'mappings': 'HGNC',
            },
            'relationship': 'interacts_with',
            'output_type': {
                'complexity': 'set',
                'category': Gene.class_name,
                'mappings': 'HGNC',
            },
        }

    def metadata(self):
        print("""Mod1E Interaction Network metadata:""")
        pprint(self.meta)

    @staticmethod
    # RMB: July 5, 2019 - gene_records is a Pandas DataFrame
    def load_gene_set(gene_records):
        annotated_gene_set = []
        for gene in gene_records.to_dict(orient='records'):
            annotated_gene_set.append({
                'input_id': gene['hit_id'],
                'sim_input_curie': gene['hit_id'],
                'input_symbol': gene['hit_symbol']
            })
        return annotated_gene_set

    def get_interactions(self, input_gene_set, threshold):

        annotated_input_gene_set = self.load_gene_set(input_gene_set)
        lower_bound = int(threshold)

        results = []
        for gene in annotated_input_gene_set:
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
                    'score': 1,  # CX: changed score from 0 to 1
                })

        # Process the results
        results = pd.DataFrame().from_records(results)
        counts = results['hit_symbol'].value_counts().rename_axis('unique_values').to_frame('counts').reset_index()
        high_counts = counts[counts['counts'] > lower_bound]['unique_values'].tolist()
        results = pd.DataFrame(results[results['hit_symbol'].isin(high_counts)])

        # CX: remove results where input gene = output gene. Output gene can still be disease associated genes. 
        results = results[~(results['hit_symbol'] == results['input_symbol'])]

        return results


class GeneInteractionSet(Payload):
    def __init__(self, input_genes, threshold=12):

        super(GeneInteractionSet, self).__init__(GeneInteractions())

        input_obj, extension = self.handle_input_or_input_location(input_genes)

        input_gene_data_frame = get_input_gene_data_frame(input_obj, extension)

        # TODO: add schema check

        self.results = self.mod.get_interactions(input_gene_data_frame, threshold)


if __name__ == '__main__':
    fire.Fire(GeneInteractionSet)
