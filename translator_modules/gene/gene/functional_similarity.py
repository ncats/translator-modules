#!/usr/bin/env python3

# Workflow 2, Module 1A: Functional similarity

from pprint import pprint

import fire
import pandas as pd
from biothings_client import get_client

from translator_modules.core.generic_similarity import GenericSimilarity
from translator_modules.core.module_payload import Payload


class FunctionalSimilarity(GenericSimilarity):

    def __init__(self, taxon):
        GenericSimilarity.__init__(self)
        self.mg = get_client('gene')
        self.input_object = ''
        self.taxon = taxon
        self.ont = 'go'
        self.meta = {
            'source': 'Monarch Biolink',
            'association': 'functional association',
            'input_type': {
                'complexity': 'set',
                'id_type': 'HGNC',
                'data_type': 'gene',
            },
            'relationship': 'related_to',
            'output_type': {
                'complexity': 'set',
                'id_type': 'HGNC',
                'data_type': 'gene',
            },
        }

        # Load the functional catalog of
        # GO ontology and annotation associations
        self.load_associations(taxon)

    def metadata(self):
        print("""Mod1A Functional Similarity metadata:""")
        pprint(self.meta)

    # RMB: July 5, 2019 - gene_records is a Pandas DataFrame
    def load_gene_set(self, gene_records):
        annotated_gene_set = []
        for gene in gene_records.to_dict(orient='records'):
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

    # RMB: July 5, 2019 - annotated_gene_set is a Pandas DataFrame
    def compute_similarity(self, input_gene_set, threshold):

        annotated_input_gene_set = self.load_gene_set(input_gene_set)
        lower_bound = float(threshold)

        results = self.compute_jaccard(annotated_input_gene_set, lower_bound)

        for result in results:
            if self.taxon == 'human':
                result['hit_id'] = self.symbol2hgnc(result['hit_symbol'])
            for gene in annotated_input_gene_set:
                if gene['sim_input_curie'] != result['input_id']:
                    result['input_id'] = self.symbol2hgnc(result['input_symbol'])

        results = GenericSimilarity.sort_results(input_gene_set, results)

        return results

    def symbol2hgnc(self, symbol):
        try:
            mg_hit = self.mg.query('symbol:{}'.format(symbol),
                                   fields='HGNC,symbol,taxon',
                                   species='human',
                                   entrezonly=True)
            if mg_hit['total'] == 1:
                return 'HGNC:{}'.format(mg_hit['hits'][0]['HGNC'])
        except:
            return 'symbol:{}'.format(symbol)


class FunctionallySimilarGenes(Payload):

    def __init__(self, input_genes, threshold):

        super(FunctionallySimilarGenes, self).__init__(FunctionalSimilarity('human'))

        input_genes, extension = self.handle_input_or_input_location(input_genes)

        if extension == "csv":
            input_gene_set = pd.read_csv(input_genes, orient='records')
        elif extension == "json":
            # assuming it's JSON and it's a record list
            input_gene_set = pd.read_json(input_genes, orient='records')
        elif extension is None:
            # TODO: this was written for the sharpener. maybe more generic if we get Biolink Model adherence
            # TODO: rewrite into schema check
            gene_ids = [gene.gene_id for gene in input_genes]
            symbols = [attribute.value for gene in input_genes for attribute in gene.attributes if
                       attribute.name == 'gene_symbol']
            genes = {"hit_id": gene_ids, "hit_symbol": symbols}
            input_gene_set = pd.DataFrame(data=genes)

        self.results = self.mod.compute_similarity(input_gene_set, threshold)


if __name__ == '__main__':
    fire.Fire(FunctionallySimilarGenes)
