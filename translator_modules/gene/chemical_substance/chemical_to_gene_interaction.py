#!/usr/bin/env python3

# Workflow 2, Module 1B: Chemical Gene Interaction
from json import JSONDecodeError
from sys import stderr
import fire
import pandas as pd

from biothings_client import get_client

from CTD.CTD_wrapper import CTDWrapper

from biolink.model import ChemicalToGeneAssociation, ChemicalSubstance, Gene
from typing import List

from translator_modules.core.module_payload import Payload
from translator_modules.core.data_transfer_model import ModuleMetaData, ConceptSpace


# TODO: Refactor towards methods being functional
class ChemicalGeneInteractions(object):
    def __init__(self, action, taxon):
        self.action=action
        self.taxon=taxon
        self.mg = get_client('gene')
        self.ctd = CTDWrapper()

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

    def get_chemicals_interacting_with_genes(self, input_gene_set) -> List[dict]:

        chemicals: List[dict] = list()
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
            # Each chemical record also contains its 'input_id' as GeneID from the input_gene_set
            chemicals += gene_chemicals

        return chemicals

    def get_genes_by_chemical_id(self, chemical_id) -> List[dict]:
        ctd_hits = self.ctd.chem2gene(chem_curie=chemical_id)
        chemical_genes = [
            x for x in ctd_hits
            if (not self.action or self.action in x['InteractionActions']) and self.taxon in x['OrganismID']]
        return chemical_genes

    def get_genes_interacting_with_chemicals(self, chemicals, rows) -> pd.DataFrame:

        # Empty dataset?
        if len(chemicals) == 0:
            return pd.DataFrame()

        chem_df = pd.DataFrame(chemicals).\
            groupby(['GeneSymbol', 'GeneID'])['ChemicalID'].\
            apply(', '.join).reset_index().to_dict(orient='records')

        gene_hits: List[dict] = list()
        for chem in chem_df:
            for index, cid in enumerate(chem['ChemicalID'].split(',')):
                if index < rows:
                    cid = cid.lstrip().rstrip()
                    cid_hits = self.get_genes_by_chemical_id(chemical_id=cid)

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
                    for cid_hit in cid_hits:
                        gene_hits.append({
                            'input_id': 'NCBIGene:'+chem['GeneID'],
                            'input_symbol': chem['GeneSymbol'],
                            'hit_symbol': '',  # subject_label,
                            'hit_id': '',  # subject_curie,
                            'score': '',  # score,
                        })

        gene_hits_df = pd.DataFrame({'hit_id': gene_hits})
        return gene_hits_df

    def get_gene_chemical_interactions(self, input_gene_set, rows) -> pd.DataFrame:
        chemicals = self.get_chemicals_interacting_with_genes(input_gene_set)
        gene_hits_df = self.get_genes_interacting_with_chemicals(chemicals, rows)
        return gene_hits_df


# TODO: Test the module separately to observe baseline behavior
class ChemicalGeneInteractionSet(Payload):

    # I set default for action filter to 'None' for now; could be action='InteractionActions'
    def __init__(self, input_genes, action=None, taxon='9606', rows=50):

        super(ChemicalGeneInteractionSet, self).__init__(
            module=ChemicalGeneInteractions(action, taxon),
            metadata=ModuleMetaData(
                name="Module 1B: Chemical Gene Interaction",
                source='Chemical Toxicology Database (CTD)',
                association=ChemicalToGeneAssociation,
                domain=ConceptSpace(Gene, ['NCBIGene']),
                relationship='interacts_with',
                range=ConceptSpace(ChemicalSubstance, ['ChemicalID'])
            )
        )

        input_gene_set = self.get_simple_input_identifier_list(input_genes, object_id_only=True)

        self.results = self.module.get_gene_to_chemical_interactions(input_gene_set, rows)


def main():
    fire.Fire(ChemicalGeneInteractionSet)


if __name__ == '__main__':
    main()