#!/usr/bin/python3
import fire

# Workflow 2, Module 0: Lookups
from BioLink.biolink_client import BioLinkWrapper
from biothings_client import get_client
import pandas as pd
from pprint import pprint
from sys import stdout
from json import dump

from ..core import Config

class LookUp(object):

    def __init__(self):
        self.blw = BioLinkWrapper(Config().getBiolinkApiEndpoint())
        self.mg = get_client('gene')
        self.input_object = ''
        self.meta = {
            'data_type': 'disease',
            'input_type': {
                'complexity': 'single',
                'id_type': ['MONDO', 'DO', 'OMIM'],
            },
            'output_type': {
                'complexity': 'set',
                'id_type': 'HGNC'
            },
            'taxon': 'human',
            'limit': None,
            'source': 'Monarch Biolink',
            'predicate': 'blm:gene associated with condition'
        }

    def metadata(self):
        print("""Mod O DiseaseGeneLookup metadata:""")
        pprint(self.meta)

    #
    # def load_input_object(self, input_object):
    #     input_object = self.blw.get_obj(obj_id=input_object['input'])
    #     self.input_object = {
    #         'id': input_object['id'],
    #         'label': input_object['label'],
    #         'description': input_object['description'],
    #     }
    #
    # def get_input_object_id(self):
    #     return self.input_object['id']

    def echo_input_object(self, output=None):
        if output:
            dump(self.input_object, output, indent=4, separators=(',', ': '))
        else:
            dump(self.input_object, stdout, indent=4, separators=(',', ': '))

    def disease_geneset_lookup(self, name, id):
        input_disease_label = name
        input_disease_id = id
        input_gene_set = self.blw.disease2genes(input_disease_id)
        input_gene_set = [self.blw.parse_association(input_disease_id, input_disease_label, x) for x in
                          input_gene_set['associations']]
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

from translator_modules.core import Payload

class DiseaseAssociatedGeneSet(Payload):

    def __init__(self, input_disease_name, input_disease_mondo):
        super(DiseaseAssociatedGeneSet, self).__init__(LookUp())

        self.input_disease_name = input_disease_name
        self.input_disease_mondo = input_disease_mondo

        # get genes associated with disease from Biolink
        self.results = self.mod.disease_geneset_lookup(self.input_disease_name, self.input_disease_mondo)
        self.disease_associated_genes = self.results[['hit_id', 'hit_symbol']].to_dict(orient='records')

    def get_input_disease_name(self):
        return self.input_disease_name


if __name__ == '__main__':
    fire.Fire(DiseaseAssociatedGeneSet)
