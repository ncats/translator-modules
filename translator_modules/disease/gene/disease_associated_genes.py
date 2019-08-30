#!/usr/bin/env python3

from pprint import pprint

import fire
import pandas as pd
# Workflow 2, Module 0: Lookups
from BioLink.biolink_client import BioLinkWrapper
from biothings_client import get_client

from translator_modules.core import Config
from translator_modules.core.module_payload import Payload


class LookUp(object):

    def __init__(self):
        self.blw = BioLinkWrapper(Config().get_biolink_api_endpoint())
        self.mg = get_client('gene')
        self.input_object = ''
        self.meta = {
            'input_type': {
                'complexity': 'single',
                'data_type': 'disease',
                'id_type': ['MONDO', 'DO', 'OMIM'],
            },
            'output_type': {
                'complexity': 'set',
                'data_type': 'gene',
                'id_type': 'HGNC'
            },
            'taxon': 'human',
            'limit': None,
            'source': 'Monarch Biolink',
            'association': '',
            'predicate': 'gene_associated_with_condition'
        }

    def metadata(self):
        print("""Mod O DiseaseGeneLookup metadata:""")
        pprint(self.meta)

    def disease_geneset_lookup(self, disease_id):
        # TODO: does this get faster if we specify the API type
        disease_label = self.blw.get_obj(disease_id)["label"]
        disease_gene_association_results = self.blw.disease2genes(disease_id)
        input_gene_set = [self.blw.parse_association(disease_id, disease_label, association) for association in
                          disease_gene_association_results['associations']]

        for input_gene in input_gene_set:
            igene_mg = self.mg.query(input_gene['hit_id'].replace('HGNC', 'hgnc'), species='human', entrezonly=True,
                                     fields='entrez,HGNC,symbol')
            input_gene.update({'input_ncbi': 'NCBIGene:{}'.format(igene_mg['hits'][0]['_id'])})
        input_genes_df = pd.DataFrame(data=input_gene_set)
        # # group duplicate ids and gather sources
        input_genes_df['sources'] = input_genes_df['sources'].str.join(', ')
        input_genes_df = input_genes_df.groupby(
            ['input_id', 'input_symbol', 'hit_id', 'hit_symbol', 'relation'])['sources'].apply(', '.join).reset_index()
        return input_genes_df


class DiseaseAssociatedGeneSet(Payload):

    def __init__(self, disease_id):
        super(DiseaseAssociatedGeneSet, self).__init__(LookUp())

        # get genes associated with disease from Biolink
        self.results = self.mod.disease_geneset_lookup(disease_id)
        self.disease_associated_genes = self.results[['hit_id', 'hit_symbol']].to_dict(orient='records')


if __name__ == '__main__':
    fire.Fire(DiseaseAssociatedGeneSet)
