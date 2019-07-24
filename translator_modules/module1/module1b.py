#!/usr/bin/env python3

import fire

# Workflow 2, Module 1B: Phenotype similarity
from pprint import pprint
from biothings_client import get_client
from translator_modules.core.generic_similarity import GenericSimilarity
import pandas as pd

from translator_modules.core import Payload


class PhenotypeSimilarity(GenericSimilarity):

    def __init__(self, taxon):
        GenericSimilarity.__init__(self)
        self.mg = get_client('gene')
        self.taxon = taxon
        if self.taxon == 'mouse':
            self.ont = 'mp'
        if self.taxon == 'human':
            self.ont = 'hp'
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
            'predicate': ['blm:has phenotype']
        }

        # Load the associated Biolink (Monarch)
        # phenotype ontology and annotation associations
        self.load_associations(taxon)

    def metadata(self):
        print("""Mod1B1 Phenotype Similarity metadata:""")
        pprint(self.meta)

    # RMB: July 5, 2019 - gene_records is a Pandas DataFrame
    def load_gene_set(self, gene_records):
        annotated_gene_set = []
        for gene in gene_records.to_dict(orient='records'):
            gene_curie = ''
            sim_input_curie = ''
            symbol = ''
            if 'MGI' in gene['hit_id']:
                gene_curie = gene['hit_id']
                sim_input_curie = gene['hit_id']
                # if self.ont == 'go':
                #     sim_input_curie = gene.replace('MGI', 'MGI:MGI')
                # else:
                #
                symbol = None
            if 'HGNC' in gene['hit_id']:
                mgi_gene_curie = gene['hit_id'].replace('HGNC', 'hgnc')
                scope = 'HGNC'
                mg_hit = self.mg.query(mgi_gene_curie,
                                  scopes=scope,
                                  species=self.taxon,
                                  fields='uniprot, symbol, HGNC',
                                  entrezonly=True)
                try:
                    gene_curie = gene['hit_id']
                    sim_input_curie = gene['hit_id']
                    symbol = mg_hit['hits'][0]['symbol']

                except Exception as e:
                    print(__name__+".load_gene_set() Exception: ", gene, e)

            annotated_gene_set.append({
                'input_id': gene_curie,
                'sim_input_curie': sim_input_curie,
                'input_symbol': gene['hit_symbol']
            })

        return annotated_gene_set

    # RMB: July 5, 2019 - annotated_gene_set is a Pandas DataFrame
    def compute_similarity(self, input_gene_set, threshold):

        annotated_input_gene_set = self.load_gene_set(input_gene_set)
        lower_bound = float(threshold)

        results = self.compute_jaccard(annotated_input_gene_set, lower_bound)

        for result in results:
            for gene in annotated_input_gene_set:
                if gene['sim_input_curie'] == result['input_id']:
                    result['input_symbol'] = gene['input_symbol']

        results = GenericSimilarity.sort_results(input_gene_set, results)

        return results


class PhenotypicallySimilarGenes(Payload):

    def __init__(self, threshold=0.35, input_genes=None, file=True):

        super(PhenotypicallySimilarGenes, self).__init__(PhenotypeSimilarity('human'))

        if file:
            with open(input_genes) as stream:
                # assuming it's JSON and it's a record list
                input_gene_set = pd.read_json(stream, orient='records')
        else:
            gene_ids = [gene.gene_id for gene in input_genes]
            symbols = [attribute.value for gene in input_genes for attribute in gene.attributes if attribute.name == 'symbol']
            genes = {"hit_id": gene_ids, "hit_symbol": symbols}
            input_gene_set = pd.DataFrame(data=genes)

        self.results = self.mod.compute_similarity(input_gene_set, threshold)



if __name__ == '__main__':
    fire.Fire(PhenotypicallySimilarGenes)
