#!/usr/bin/env python3

import asyncio
import concurrent.futures
import urllib.request
from collections import defaultdict, Counter

import fire
import pandas as pd
import requests

from BioLink.model import GeneToExpressionSiteAssociation, AnatomicalEntity, Gene
from typing import Dict, List, Set

from translator_modules.core.module_payload import Payload, fix_curies, get_simple_input_gene_list

bicluster_gene_url = 'https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_v3_gene/'


class BiclusterByGeneToTissue():
    def __init__(self):
        self.meta = {
            'source': 'RNAseqDB Biclustering',
            'association': GeneToExpressionSiteAssociation,
            'input_type': {
                'complexity': 'set',
                'id_prefixes': 'ENSEMBL',
                'category': Gene,
            },
            'relationship': 'related_to',
            'output_type': {
                'complexity': 'set',
                'id_prefixes': ['MONDO', 'DOID', 'UBERON'],
                'category': AnatomicalEntity,
            },
        }

    async def gene_to_tissue_biclusters_async(self, input_ID_list):
        bicluster_url_list = [bicluster_gene_url + gene + '/' + '?include_similar=true' for gene in input_ID_list]
        with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor_1:
            all_tissues = []
            tissue_map = defaultdict(Dict[str, Set[str]])
            loop_1 = asyncio.get_event_loop()
            futures_1 = [loop_1.run_in_executor(executor_1, requests.get, request_1_url) for request_1_url in
                         bicluster_url_list]
            for response in await asyncio.gather(*futures_1):
                response_json = response.json()
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
        super(GeneToTissueBiclusters, self).__init__(BiclusterByGeneToTissue())

        input_obj, extension = self.handle_input_or_input_location(input_genes)

        input_gene_set = get_simple_input_gene_list(input_obj, extension)

        most_common_tissues = asyncio.run(self.mod.gene_to_tissue_biclusters_async(input_gene_set))

        self.results = pd.DataFrame.from_records(most_common_tissues)


if __name__ == '__main__':
    fire.Fire(GeneToTissueBiclusters)
