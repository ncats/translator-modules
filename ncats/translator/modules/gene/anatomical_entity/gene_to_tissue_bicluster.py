#!/usr/bin/env python3

import asyncio
import concurrent.futures
from collections import defaultdict, Counter
from json import JSONDecodeError

import fire
import pandas as pd
import requests

from typing import Dict, Set

from biolink.model import GeneToExpressionSiteAssociation, AnatomicalEntity, Gene

from ncats.translator.identifiers import fix_curies

from ncats.translator.core.module_payload import Payload
from ncats.translator.core.data_transfer_model import ModuleMetaData, ConceptSpace

bicluster_gene_url = 'https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_v3_gene/'


class BiclusterByGeneToTissue:

    def __init__(self):
        pass

    async def gene_to_tissue_biclusters_async(self, input_ID_list):
        bicluster_url_list = [bicluster_gene_url + gene + '/' + '?include_similar=true' for gene in input_ID_list]
        with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor_1:
            all_tissues = []
            tissue_map = defaultdict(Dict[str, Set[str]])
            loop_1 = asyncio.get_event_loop()
            futures_1 = [loop_1.run_in_executor(executor_1, requests.get, request_1_url) for request_1_url in
                         bicluster_url_list]

            for response in await asyncio.gather(*futures_1):

                try:
                    response_json = response.json()
                except JSONDecodeError:
                    continue

                for x in response_json:
                    gene = x['gene']
                    tissues = x['all_col_labels'].split('__')
                    for y in tissues:
                        if y not in tissue_map:
                            tissue_map[y]: Set[str] = set()
                        tissue_map[y].add(gene)
                        all_tissues.append(y)
            tissues_counted = Counter(all_tissues)
        results = [
            {
                'input_id': ','.join(fix_curies(tissue_map[tissue], prefix='ENSEMBL')),
                'hit_id': tissue_count[0],
                'score': tissue_count[1]
            }
            for tissue in tissue_map.keys()
            for tissue_count in tissues_counted.most_common()
            if tissue == tissue_count[0]
        ]
        return results


class GeneToTissueBiclusters(Payload):

    def __init__(self, input_genes):

        super(GeneToTissueBiclusters, self).__init__(
            module=BiclusterByGeneToTissue(),
            metadata=ModuleMetaData(
                name="Mod9A - Gene-to-Tissue Bicluster",
                source='RNAseqDB Biclustering',
                association=GeneToExpressionSiteAssociation,
                domain=ConceptSpace(Gene, ['ENSEMBL']),
                relationship='related_to',
                range=ConceptSpace(AnatomicalEntity, ['MONDO', 'DOID', 'UBERON']),
            )
        )

        input_gene_set = self.get_simple_input_identifier_list(input_genes)

        most_common_tissues = asyncio.run(self.module.gene_to_tissue_biclusters_async(input_gene_set))

        self.results = pd.DataFrame.from_records(most_common_tissues)


def main():
    fire.Fire(GeneToTissueBiclusters)


if __name__ == '__main__':
    main()