#!/usr/bin/env python3

# Workflow 2, Module 1A: Functional similarity

import fire

from biothings_client import get_client

from biolink.model import FunctionalAssociation, Gene

from translator_modules.core.data_transfer_model import ModuleMetaData, ConceptSpace
from translator_modules.core.generic_similarity import GenericSimilarity
from translator_modules.core.module_payload import Payload


class FunctionalSimilarity(GenericSimilarity):

    def __init__(self, taxon):
        GenericSimilarity.__init__(self)
        self.mg = get_client('gene')
        self.input_object = ''
        self.taxon = taxon
        self.ont = 'go'

        # Load the functional catalog of
        # GO ontology and annotation associations
        self.load_associations(taxon)

    # RMB: July 5, 2019 - gene_records is a Pandas DataFrame
    def load_gene_set(self, input_gene_set):
        annotated_gene_set = []
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
                if result['input_symbol']: # not None or empty input_symbol?
                    if gene['sim_input_curie'] != result['input_id']:
                        result['input_id'] = self.symbol2hgnc(result['input_symbol'])

        results = GenericSimilarity.sort_results(results)

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

        super(FunctionallySimilarGenes, self).__init__(
            module=FunctionalSimilarity('human'),
            metadata=ModuleMetaData(
                name="Mod1A Functional Similarity",
                source='Monarch Biolink',
                association=FunctionalAssociation,
                domain=ConceptSpace(Gene, ['HGNC']),
                relationship='related_to',
                range=ConceptSpace(Gene, ['HGNC']),
            )
        )

        input_gene_data_frame = self.get_input_data_frame(input_genes)

        self.results = self.module.compute_similarity(input_gene_data_frame, threshold)


if __name__ == '__main__':
    fire.Fire(FunctionallySimilarGenes)
