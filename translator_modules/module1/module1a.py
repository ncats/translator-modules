#!/usr/bin/python3
import fire

# Workflow 2, Module 1A: Functional similarity

from translator_modules.core.generic_similarity import GenericSimilarity
from pprint import pprint
from biothings_client import get_client
import pandas as pd


class FunctionalSimilarity(GenericSimilarity):

    def __init__(self, taxon):
        GenericSimilarity.__init__(self)
        self.mg = get_client('gene')
        self.input_object = ''
        self.taxon = taxon
        self.ont = 'go'
        self.meta = {
            'input_type': {
                'complexity': 'set',
                'id_type': 'HGNC',
                'data_type': 'gene',
            },
            'output_type': {
                'complexity': 'set',
                'id_type': 'HGNC',
                'data_type': 'gene',
            },

            'source': 'Monarch Biolink',
            'predicate': ['blm:macromolecular machine to biological process association',
                          'macromolecular machine to molecular activity association']
        }

        # Load the functional catalog of
        # GO ontology and annotation associations
        self.load_associations(taxon)

    def metadata(self):
        print("""Mod1A Functional Similarity metadata:""")
        pprint(self.meta)

    def load_gene_set(self, input_genes):
        annotated_gene_set = []
        gene_records = input_genes.to_dict(orient='records')
        for gene in gene_records:
            mg = self.mg
            gene_curie = ''
            sim_input_curie = ''
            symbol = ''
            if 'MGI' in gene['hit_id']:
                gene_curie = gene['hit_id']
                sim_input_curie = gene['hit_id'].replace('MGI', 'MGI:MGI')
                symbol = None
            if 'HGNC' in gene['hit_id']:
                gene_curie = gene['hit_id'].replace('HGNC', 'hgnc')
                scope = 'HGNC'
                mg_hit = mg.query(gene_curie,
                                  scopes=scope,
                                  species=self.taxon,
                                  fields='uniprot, symbol, HGNC',
                                  entrezonly=True)
                try:
                    gene_curie = gene['hit_id']
                    sim_input_curie = 'UniProtKB:{}'.format(mg_hit['hits'][0]['uniprot']['Swiss-Prot'])
                except Exception as e:
                    print(gene, e)

            annotated_gene_set.append({
                'input_id': gene_curie,
                'sim_input_curie': sim_input_curie,
                'input_symbol': gene['hit_symbol']
            })

        return annotated_gene_set

    def compute_similarity(self, annotated_gene_set, threshold):
        lower_bound = float(threshold)
        results = self.compute_jaccard(annotated_gene_set, lower_bound)
        for result in results:
            if self.taxon == 'human':
                result['hit_id'] = self.symbol2hgnc(result['hit_symbol'])
            for gene in annotated_gene_set:
                if gene['sim_input_curie'] != result['input_id']:
                    result['input_id'] = self.symbol2hgnc(result['input_symbol'])
        return results

    def symbol2hgnc(self, symbol):
        mg_hit = self.mg.query('symbol:{}'.format(symbol),
                          fields='HGNC,symbol,taxon',
                          species='human',
                          entrezonly=True)
        if mg_hit['total'] == 1:
            return 'HGNC:{}'.format(mg_hit['hits'][0]['HGNC'])


import json
from translator_modules.core import Payload


class FunctionallySimilarGenes(Payload):

    def __init__(self, threshold=0.75, input_payload_file=None):

        input_gene_set_df = None
        if input_payload_file:
            with open(input_payload_file) as stream:
                # TODO assuming it's JSON and it's a record list
                input_gene_set_df = pd.read_json(stream, orient='records')

        self.input_object = {
            'input': input_gene_set_df,
            'parameters': {
                'taxon': 'human',
                'threshold': threshold,
            },
        }

        # TODO: similarity should be refactored out of the payload and into the FunctionalSimilarity class
        # it should be made a behavior for functional similarity that can give us a result we can use
        # if we're just doing file conversions it's our responsibility in this class to do that properly
        self.fs = FunctionalSimilarity('human')
        self.functionally_similar_gene_results = self._similarity(input_gene_set_df, threshold)

    def _similarity(self, input_gene_set, threshold):

        # TODO: Break this out into an EXPANDER workflow step?
        annotated_input_gene_set = self.fs.load_gene_set(input_gene_set)

        # Perform the comparison on specified gene set
        results = self.fs.compute_similarity(annotated_input_gene_set, threshold)

        # Process the results
        results_table = pd.DataFrame(results)
        results_table = \
            results_table[~results_table['hit_id'].
                isin(input_gene_set['hit_id'].
                     tolist())].sort_values('score', ascending=False)

        return results_table

    def echo_input_object(self, output=None):
        return self.fs.echo_input_object(output)
    #
    # def get_input_object_id(self):
    #     return self.fs.get_input_object_id()

    def get_data_frame(self):
        return self.functionally_similar_gene_results

    def get_hits(self):
        hits = self.get_data_frame()[['hit_id', 'hit_symbol']]
        return hits

    def get_hits_dict(self):
        hits_dict = self.get_hits().to_dict(orient='records')
        return hits_dict


if __name__ == '__main__':
    from os import sys, path
    sys.path.extend(path.dirname(path.dirname(path.abspath(__file__))))
    fire.Fire(FunctionallySimilarGenes)
