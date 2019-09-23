#!/usr/bin/env python3

# Workflow 2, Module 0: Lookups
from pprint import pprint

import fire
import pandas as pd

from biolink_api.biolink_api_client import BioLinkApiWrapper
from biothings_client import get_client

from biolink.model import GeneToDiseaseAssociation, Gene, Disease

from core import Config
from core.module_payload import Payload
from core.data_transfer_model import ModuleMetaData, ConceptSpace


class LookUp(object):

    def __init__(self):
        self.blw = BioLinkApiWrapper(Config().get_biolink_api_endpoint())
        self.mg = get_client('gene')
        self.meta = {
            'taxon': 'human',
            'limit': None,
        }

    def metadata(self):
        print("""Mod O DiseaseGeneLookup metadata:""")
        pprint(self.meta)

    def disease_geneset_lookup(self, disease_id, disease_label, query_biolink=True):

        disease_gene_association_results = self.blw.disease2genes(disease_id)
        input_gene_set = [self.blw.parse_association(disease_id, disease_label, association) for association in
                          disease_gene_association_results['associations']]

        for input_gene in input_gene_set:
            if query_biolink:
                igene_mg = self.mg.query(input_gene['hit_id'].replace('HGNC', 'hgnc'), species='human', entrezonly=True,
                                         fields='entrez,HGNC,symbol')
                if igene_mg['hits']:
                    input_gene.update({'input_ncbi': 'NCBIGene:{}'.format(igene_mg['hits'][0]['_id'])})
        input_genes_df = pd.DataFrame(data=input_gene_set)
        if not input_genes_df.empty:
            # group duplicate identifier and gather sources
            input_genes_df['sources'] = input_genes_df['sources'].str.join(', ')
            input_genes_df = input_genes_df.groupby(
                ['input_id', 'input_symbol', 'hit_id', 'hit_symbol', 'relation'])['sources'].apply(
                ', '.join).reset_index()
        return input_genes_df


class DiseaseAssociatedGeneSet(Payload):

    def __init__(self, disease_identifier, disease_label='', query_biolink=True):

        super(DiseaseAssociatedGeneSet, self).__init__(
            module=LookUp(),
            metadata=ModuleMetaData(
                name="Mod2.0 - Disease Associated Genes",
                source='Monarch Biolink',
                association=GeneToDiseaseAssociation,
                domain=ConceptSpace(Disease, ['MONDO']),
                relationship='gene_associated_with_condition',
                range=ConceptSpace(Gene, ['HGNC']),
            )
        )

        self.input_disease_identifier = disease_identifier
        if disease_label:
            self.input_disease_label = disease_label
        else:
            self.input_disease_label = disease_identifier

        # get genes associated with disease from Biolink
        self.results = self.module.disease_geneset_lookup(disease_identifier, disease_label, query_biolink)

        if not self.results.empty:
            self.disease_associated_genes = self.results[['hit_id', 'hit_symbol']].to_dict(orient='records')
        else:
            self.disease_associated_genes = []


def main():
    fire.Fire(DiseaseAssociatedGeneSet)


if __name__ == '__main__':
    main()