#!/usr/bin/env python3

# Workflow 2, Module 1B: Chemical Gene Interaction
from json import JSONDecodeError
from sys import stderr
import fire
import pandas as pd

from biothings_client import get_client

from CTD.CTD_wrapper import CTDWrapper

from BioLink.model import ChemicalToGeneAssociation, ChemicalSubstance, Gene
from typing import List

from translator_modules.core.module_payload import Payload, get_input_gene_set


# TODO: Refactor towards methods being functional
class ChemicalGeneInteractions(object):
    def __init__(self):
        self.mg = get_client('gene')
        self.ctd = CTDWrapper()
        self.meta = {
            'source': 'RENCI ChemoInformatics',
            'association': ChemicalToGeneAssociation.class_name,
            'input_type': {
                'complexity': 'set',
                'category': Gene.class_name,
                'mappings': 'HGNC',
            },
            'relationship': 'interacts_with',
            'output_type': {
                'complexity': 'set',
                'category': ChemicalSubstance.class_name,
                'mappings': 'ChemicalID',
            },
        }

    def load_gene_set(self, input_gene_set) -> List[str]:
        annotated_gene_set = []
        for gene in input_gene_set.to_dict(orient='records'):
            if 'HGNC' in gene['hit_id']:
                gene_curie = gene['hit_id'].replace('HGNC', 'hgnc')
                scope = 'HGNC'
                mg_hit = \
                    self.mg.query(
                        gene_curie,
                        scopes=scope,
                        species='human',
                        fields='symbol',
                        entrezonly=True
                    )
                try:
                    symbol = mg_hit['hits'][0]['symbol']
                except Exception as e:
                    # problem with symbol discovery?
                    print(gene, e)
                    continue

            annotated_gene_set.append(symbol)

        return annotated_gene_set

    def get_chemicals(self, input_gene_set, action) -> List[dict]:

        target_gene_set = self.load_gene_set(input_gene_set)

        chemicals = list()
        for gene_id in target_gene_set:
            # The 'gene_id' is assumed to be a curie to be parsed here for
            # its object identifier which is a valid gene query to the CTD wrapper
            target_id = gene_id.split(':')[-1]
            try:
                all_gene_chemicals = self.ctd.gene2chem(target_id)
            except JSONDecodeError as e:
                print("Error: gene2chem target_id '"+target_id+"':"+e.msg, file=stderr)
                continue

            gene_chemicals = [
                x for x in all_gene_chemicals
                if action in x['InteractionActions'] and '9606' in x['OrganismID']
            ]
            chemicals = chemicals + gene_chemicals

        return chemicals

    def get_genes(self, chemical_id, action) -> List[dict]:
        ctd_hits = self.ctd.chem2gene(chem_curie=chemical_id)
        chemical_genes = [
            x for x in ctd_hits
            if action in x['InteractionActions'] and '9606' in x['OrganismID']]
        return chemical_genes

    def load_gene_hits(self, chemicals, action, rows) -> pd.DataFrame:

        # Empty dataset?
        if len(chemicals) == 0:
            return pd.DataFrame()

        chem_df = pd.DataFrame(chemicals).\
            groupby(['GeneSymbol', 'GeneID'])['ChemicalID'].\
            apply(', '.join).reset_index().to_dict(orient='records')

        gene_hits = List[dict]
        for chem in chem_df:
            for index, cid in enumerate(chem['ChemicalID'].split(',')):
                if index < rows:
                    cid = cid.lstrip().rstrip()
                    cid_hit = self.get_genes(chemical_id=cid, action=action)

                    # Not sure if the gene hits from CTD are in
                    # the expected data format for the results(?)
                    # We may need to do some more work here, i.e.
                    #
                    # gene_hits.append({
                    #     'input_id': ...,
                    #     'input_symbol': ...,
                    #     'hit_symbol': ...,
                    #     'hit_id': ...,
                    #     'score': ...,
                    # })
                    gene_hits = gene_hits + cid_hit

        gene_hits_df = pd.DataFrame({'hit_id': gene_hits})
        return gene_hits_df

    def get_gene_chemical_interactions(self, input_gene_set, action, rows) -> pd.DataFrame:
        chemicals = self.get_chemicals(input_gene_set, action)
        gene_hits_df = self.load_gene_hits(chemicals, action, rows)
        return gene_hits_df


# TODO: Test the module separately to observe baseline behavior
class ChemicalGeneInteractionSet(Payload):

    def __init__(self, input_genes, action='InteractionActions', rows=50):

        super(ChemicalGeneInteractionSet, self).__init__(ChemicalGeneInteractions())

        input_genes, extension = self.handle_input_or_input_location(input_genes)

        input_gene_set = get_input_gene_set(input_genes, extension)

        self.results = self.mod.get_gene_chemical_interactions(input_gene_set, action, rows)


if __name__ == '__main__':
    fire.Fire(ChemicalGeneInteractionSet)
