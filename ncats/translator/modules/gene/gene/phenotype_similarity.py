#!/usr/bin/env python3

# Workflow 2, Module 1B: Phenotype similarity

import fire

from biothings_client import get_client

from biolink.model import GeneToPhenotypicFeatureAssociation, Gene

from ncats.translator.core.module_payload import Payload
from ncats.translator.core.data_transfer_model import ModuleMetaData, ConceptSpace
from ncats.translator.core.generic_similarity import GenericSimilarity


class PhenotypeSimilarity(GenericSimilarity):

    def __init__(self, taxon):
        GenericSimilarity.__init__(self)
        self.mg = get_client('gene')
        self.taxon = taxon
        if self.taxon == 'mouse':
            self.ont = 'mp'
        if self.taxon == 'human':
            self.ont = 'hp'

        # Load the associated Biolink (Monarch)
        # phenotype ontology and annotation associations
        # self.load_associations(taxon)  # associations now remotely initialized (in ontology service)

    # RMB: July 5, 2019 - gene_records is a Pandas DataFrame
    def load_gene_set(self, input_gene_set):
        annotated_gene_set = []
        for gene in input_gene_set.to_dict(orient='records'):
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

        results = GenericSimilarity.sort_results(results)

        return results


class PhenotypicallySimilarGenes(Payload):

    def __init__(self, input_genes, threshold):

        super(PhenotypicallySimilarGenes, self).__init__(
            module=PhenotypeSimilarity('human'),
            metadata=ModuleMetaData(
                name="Mod1B1 Phenotype Similarity",
                source='Monarch Biolink',
                association=GeneToPhenotypicFeatureAssociation,
                domain=ConceptSpace(Gene, ['HGNC']),
                relationship='has_phenotype',
                range=ConceptSpace(Gene, ['HGNC']),
            )
        )

        input_gene_data_frame = self.get_input_data_frame(input_genes)

        self.results = self.module.compute_similarity(input_gene_data_frame, threshold)


def main():
    fire.Fire(PhenotypicallySimilarGenes)


if __name__ == '__main__':
    main()