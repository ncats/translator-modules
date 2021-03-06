#!/usr/bin/env python3

# Workflow 2, Module 1E: Gene Interaction

import fire
import pandas as pd

from biolink_api.biolink_api_client import BioLinkApiWrapper
from biolink.model import GeneToGeneAssociation, Gene

from ncats.translator.core.identifiers_resolver import gene_symbol

from ncats.translator.core import Config
from ncats.translator.core.module_payload import Payload
from ncats.translator.core.data_transfer_model import ModuleMetaData, ConceptSpace


class GeneInteractions:

    def __init__(self):
        self.blw = BioLinkApiWrapper(Config().get_biolink_api_endpoint())

    @staticmethod
    # RMB: July 5, 2019 - gene_records is a Pandas DataFrame
    def load_gene_set(gene_records):
        annotated_gene_set = []
        for gene in gene_records.to_dict(orient='records'):

            gene['hit_symbol'] = gene_symbol(gene['hit_id'], gene['hit_symbol'])

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

                interaction['input_symbol'] = \
                    gene_symbol(
                        interaction['input_id'],
                        interaction['input_symbol']
                    )

                interaction['hit_symbol'] = \
                    gene_symbol(
                        interaction['hit_id'],
                        interaction['hit_symbol']
                    )

                results.append({
                    'input_id': interaction['input_id'],
                    'input_symbol': interaction['input_symbol'],
                    'hit_id': interaction['hit_id'],
                    'hit_symbol': interaction['hit_symbol'],
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

    # RMB: we set the threshold to default to "return all"
    def __init__(self, input_genes=None, threshold=0):

        super(GeneInteractionSet, self).__init__(module=GeneInteractions())

        if not input_genes:
            raise RuntimeError("GeneInteractionSet ERROR: missing mandatory input_genes parameter")

        input_gene_data_frame = self.get_input_data_frame(input_genes)

        self.results = self.module.get_interactions(input_gene_data_frame, threshold)


GeneInteractionSet.set_metadata(
    ModuleMetaData(
        name="Module 1E - Gene Interaction",
        source='Monarch Biolink',
        association=GeneToGeneAssociation,
        domain=ConceptSpace(Gene, ['HGNC']),
        relationship='interacts_with',
        range=ConceptSpace(Gene, ['HGNC']),
    )
)


def metadata():
    """
    Retrieve Module Metadata
    """
    return GeneInteractionSet.get_metadata()


def main():
    fire.Fire(GeneInteractionSet)


if __name__ == '__main__':
    main()
