#!/usr/bin/env python3

# Workflow 2, Module 1B: Chemical Gene Interaction
import fire
import pandas as pd
# Workflow 2, Module 1D: Chemical-gene interactions
from CTD.CTD_wrapper import CTDWrapper

from translator_modules.core.module_payload import Payload


# TODO: Refactor towards methods being functional
class ChemicalGeneInteractions(object):
    def __init__(self):
        self.ctd = CTDWrapper()
        self.gene_set = ''
        self.chemicals = []
        self.gene_hits = []
        self.meta = {
            'source': 'RENCI ChemoInformatics',
            'association': 'chemical to gene association',
            'input_type': {
                'complexity': 'set',
                'id_type': 'ChemicalID',
                'data_type': 'chemical',
            },
            'relationship': 'interacts_with',
            'output_type': {
                'complexity': 'set',
                'id_type': 'HGNC',
                'data_type': 'gene',
            },
        }

    def load_gene_set(self, gene_set):
        self.gene_set = gene_set

    def get_chemicals(self, action):
        gene_chemicals = list()
        for index, row in self.gene_set.iterrows():
            gene_chemicals = gene_chemicals + self.ctd.gene2chem(row[3].split(':')[-1])
            gene_chemicals = [x for x in gene_chemicals if action in x['InteractionActions'] and '9606' in x['OrganismID']]
        self.chemicals = self.chemicals + gene_chemicals

    def get_genes(self, chemical_id, action):
        ctd_hits = self.ctd.chem2gene(chem_curie=chemical_id)
        chemical_genes = [x for x in ctd_hits if action in x['InteractionActions'] and '9606' in x['OrganismID']]
        return chemical_genes

    def load_gene_hits(self, action, rows):
        chem_df = pd.DataFrame(self.chemicals).groupby(['GeneSymbol', 'GeneID'])['ChemicalID'].apply(', '.join).reset_index().to_dict(orient='records')
        for chem in chem_df:
            for index, cid in enumerate(chem['ChemicalID'].split(',')):
                if index < rows:
                    cid = cid.lstrip().rstrip()
                    cid_hit = self.get_genes(chemical_id=cid, action=action)
                    self.gene_hits = self.gene_hits + cid_hit


# TODO: Test the module separately to observe baseline behavior
class ChemicalGeneInteractionSet(Payload):

    def __init__(self, input_genes, action, rows=50):
        super(ChemicalGeneInteractionSet, self).__init__(ChemicalGeneInteractionSet())
        input_genes, extension = self.handle_input_or_input_location(input_genes)

        if "json" in extension:
            # assuming it's JSON and it's a record list
            input_gene_set_df = pd.read_json(input_genes, orient='records')
        # TODO: add schema check

        self.mod.load_gene_set(input_gene_set_df.to_dict(orient='records'))
        self.mod.get_chemicals(action)
        self.mod.load_gene_hits(action, rows)
        self.results = self.mod.gene_hits


if __name__ == '__main__':
    fire.Fire(ChemicalGeneInteractionSet)
