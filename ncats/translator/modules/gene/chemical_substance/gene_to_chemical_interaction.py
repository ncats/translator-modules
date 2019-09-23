#!/usr/bin/env python3

# Workflow 2, Module 1B: Gene to Chemical Interaction

from json import JSONDecodeError
from sys import stderr
import fire
import pandas as pd

from CTD.CTD_wrapper import CTDWrapper

from biolink.model import ChemicalToGeneAssociation, ChemicalSubstance, Gene
from typing import List

from ncats.translator.core.module_payload import Payload
from ncats.translator.core.data_transfer_model import ModuleMetaData, ConceptSpace


class GeneToChemicalInteractions(object):
    def __init__(self, action, taxon):
        self.action=action
        self.taxon=taxon
        self.ctd = CTDWrapper()

    def get_chemicals_interacting_with_genes(self, input_gene_set, rows) -> pd.DataFrame:

        chemical_hits: List[dict] = list()

        for input_id in input_gene_set:
            # The 'gene_id' is assumed to be a raw NCBIGene object identifier
            # which is a valid gene query to the CTD wrapper
            try:
                all_gene_chemicals = self.ctd.gene2chem(input_id)
            except JSONDecodeError as e:
                print("Error: gene2chem target_id 'NCBIGene:"+input_id+"':"+e.msg, file=stderr)
                continue

            gene_chemicals = [
                x for x in all_gene_chemicals
                if (not self.action or self.action in x['InteractionActions']) and self.taxon in x['OrganismID']
            ]

            # Load results into standard formatted Pandas DataFrame for export
            # Each chemical record also contains its 'input_id' as GeneID from the input_gene_set
            for chem in gene_chemicals:
                chemical_hits.append({
                    'input_id': 'NCBIGene:' + chem['GeneID'],
                    'input_symbol': chem['GeneSymbol'],
                    'hit_id': chem['ChemicalID'],
                    'hit_symbol': chem['ChemicalName'],
                    'score': 1,  # score here is simply a 'hit' of one
                })

        return pd.DataFrame(chemical_hits)


class GeneToChemicalInteractionPayload(Payload):

    # I set default for action filter to 'None' for now; could be action='InteractionActions'
    def __init__(self, input_genes, action=None, taxon='9606', rows=50):

        super(GeneToChemicalInteractionPayload, self).__init__(
            module=GeneToChemicalInteractions(action, taxon),
            metadata=ModuleMetaData(
                name="Module 1B: Gene to Chemical Interactions",
                source='Chemical Toxicology Database (CTD)',
                association=ChemicalToGeneAssociation,
                domain=ConceptSpace(Gene, ['NCBIGene']),
                relationship='interacts_with',
                range=ConceptSpace(ChemicalSubstance, ['ChemicalID'])
            )
        )

        input_gene_set = self.get_simple_input_identifier_list(input_genes, object_id_only=True)

        self.results = self.module.get_chemicals_interacting_with_genes(input_gene_set, rows)


def main():
    fire.Fire(GeneToChemicalInteractionPayload)


if __name__ == '__main__':
    main()