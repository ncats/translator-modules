#!/usr/bin/env python3

# Workflow 2, Module 1A: Functional similarity

from pprint import pprint

import fire

from biothings_client import get_client

from translator_modules.core.module_payload import Payload, get_input_gene_data_frame

from translator_modules.core.generic_similarity import GenericSimilarity

from BioLink.model import FunctionalAssociation, Gene


class FunctionalSimilarity(GenericSimilarity):

    def __init__(self, taxon):
        GenericSimilarity.__init__(self)
        self.mg = get_client('gene')
        self.input_object = ''
        self.taxon = taxon
        self.ont = 'go'
        self.meta = {
            'source': 'Monarch Biolink',
            'association': FunctionalAssociation.class_name,
            'input_type': {
                'complexity': 'set',
                'category': Gene.class_name,
                'mappings': 'HGNC',
            },
            'relationship': 'related_to',
            'output_type': {
                'complexity': 'set',
                'category': Gene.class_name,
                'mappings': 'HGNC',
            },
        }

        # Load the functional catalog of
        # GO ontology and annotation associations
        self.load_associations(taxon)

    def metadata(self):
        print("""Mod1A Functional Similarity metadata:""")
        pprint(self.meta)

    # RMB: July 5, 2019 - gene_records is a Pandas DataFrame
    def load_gene_set(self, input_gene_set):
        annotated_gene_set = []
        record_inputs = []  ## CX: to avoid duplicates in next steps
        for gene in input_gene_set.to_dict(orient='records'):
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
            
            if gene_curie not in record_inputs: ## CX: to avoid duplicates in next steps
                record_inputs.append(gene_curie)
                annotated_gene_set.append({
                    'input_id': gene_curie,
                    'sim_input_curie': sim_input_curie,
                    'input_symbol': gene['hit_symbol']
                })

        return annotated_gene_set

    # RMB: July 5, 2019 - annotated_gene_set is a Pandas DataFrame
    def compute_similarity(self, input_gene_set, threshold):

        annotated_input_gene_set = self.load_gene_set(input_gene_set)
#        print(annotated_input_gene_set)
        
        lower_bound = float(threshold)

        results = self.compute_jaccard(annotated_input_gene_set, lower_bound)

        for result in results:
            if self.taxon == 'human':
                result['hit_id'] = self.symbol2hgnc(result['hit_symbol'])
            for gene in annotated_input_gene_set:
                if result['input_symbol']: # not None or empty input_symbol?
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

        input_obj, extension = self.handle_input_or_input_location(input_genes)

        input_gene_data_frame = get_input_gene_data_frame(input_obj, extension)

        self.results = self.mod.compute_similarity(input_gene_data_frame, threshold)


if __name__ == '__main__':
    fire.Fire(FunctionallySimilarGenes)
