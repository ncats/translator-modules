#!/usr/bin/env python3

# Workflow 2, Module 1B: Chemical Gene Interaction
import fire
import pandas as pd

from biothings_client import get_client

from CTD.CTD_wrapper import CTDWrapper

from biolink.model import ChemicalToGeneAssociation, ChemicalSubstance, Gene
from typing import List

from ncats.translator.core.module_payload import Payload
from ncats.translator.core.data_transfer_model import ModuleMetaData, ConceptSpace


class ChemicalToGeneInteractions(object):
    def __init__(self, action, taxon):
        self.action=action
        self.taxon=taxon
        self.mg = get_client('gene')
        self.ctd = CTDWrapper()

    def get_genes_by_chemical_id(self, chemical_id) -> List[dict]:
        ctd_hits = self.ctd.chem2gene(chem_curie=chemical_id)
        chemical_genes = [
            x for x in ctd_hits
            if (not self.action or self.action in x['InteractionActions']) and self.taxon in x['OrganismID']]
        return chemical_genes

    def get_genes_interacting_with_chemicals(self, chemicals, rows) -> pd.DataFrame:

        gene_list: List[dict] = list()
        for chem_id in chemicals:
            chemical_gene_interactions = self.get_genes_by_chemical_id(chemical_id=chem_id)
            for chemical_gene_hit in chemical_gene_interactions:
                gene_list.append({
                    'input_id': "CTD:"+chemical_gene_hit['ChemicalID'],
                    'input_symbol': chemical_gene_hit['ChemicalName'],
                    'hit_id': 'NCBIGene:'+chemical_gene_hit['GeneID'],
                    'hit_symbol': chemical_gene_hit['GeneSymbol'],
                    'score': 1,  # score here is simply a 'hit' of one
                })

        return pd.DataFrame(gene_list)


class ChemicalToGeneInteractionPayload(Payload):

    # I set default for action filter to 'None' for now; could be action='InteractionActions'
    def __init__(self, input_chemicals=None, action=None, taxon='9606', rows=50):

        super(ChemicalToGeneInteractionPayload, self).__init__(
            module=ChemicalToGeneInteractions(action, taxon),
            metadata=ModuleMetaData(
                name="Module 1B: Chemical Gene Interaction",
                source='Chemical Toxicology Database (CTD)',
                association=ChemicalToGeneAssociation,
                domain=ConceptSpace(ChemicalSubstance, ['CTD']),
                relationship='interacts_with',
                range=ConceptSpace(Gene, ['NCBIGene'])
            )
        )

        if not input_chemicals:
            raise RuntimeError("ChemicalToGeneInteractionPayload ERROR: missing mandatory input_chemicals parameter")

        input_chemical_set = self.get_simple_input_identifier_list(input_chemicals, object_id_only=True)

        self.results = self.module.get_genes_interacting_with_chemicals(input_chemical_set, rows)


def main():
    fire.Fire(ChemicalToGeneInteractionPayload)


if __name__ == '__main__':
    main()