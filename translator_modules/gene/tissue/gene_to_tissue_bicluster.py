#!/usr/bin/env python3

import asyncio

import fire
import pandas as pd

from translator_modules.core.module_payload import Payload

import concurrent.futures
import urllib.request
from collections import defaultdict, Counter

import requests

bicluster_gene_url = 'https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_v3_gene/'


class BiclusterByGeneToTissue():
    def __init__(self):
        pass

    def get_ID_list(self, ID_list_url):
        with urllib.request.urlopen(ID_list_url) as url:
            ID_list = url.read().decode().split('\n')
        return ID_list

    def curated_ID_list(self, ID_list):
        curated_ID_list = []
        for ID in ID_list:
            if not ID:
                continue
            else:
                ID = ID.split(None, 1)[0]
                ID = ID.lower()
                curated_ID_list.append(ID)
        return curated_ID_list

    def run_getinput(self, ID_list_url):
        ID_list = self.get_ID_list(ID_list_url)
        curated_ID_list = self.curated_ID_list(ID_list)
        return curated_ID_list

    async def gene_to_tissue_biclusters_async(self, input_ID_list):
        bicluster_url_list = [bicluster_gene_url + gene + '/' + '?include_similar=true' for gene in input_ID_list]
        length_bicluster_url_list = len(bicluster_url_list)
        all_biclusters_dict = defaultdict(dict)
        with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor_1:
            all_tissues = []
            loop_1 = asyncio.get_event_loop()
            futures_1 = [loop_1.run_in_executor(executor_1, requests.get, request_1_url) for request_1_url in
                         bicluster_url_list]
            for response in await asyncio.gather(*futures_1):
                response_json = response.json()
                for x in response_json:
                    tissues = x['all_col_labels'].split('__')
                    for y in tissues:
                        all_tissues.append(y)
            tissues_counted = Counter(all_tissues)
        return tissues_counted.most_common()


class GeneToTissueBiclusters(Payload):

    def __init__(self, input_genes):
        self.mod = BiclusterByGeneToTissue()
        input_obj, extension = self.handle_input_or_input_location(input_genes)

        input_gene_ids: list
        # NB: push this out to the handle_input_or_input_location function?
        if extension == "csv":
            import csv
            with open(input_genes) as genes:
                input_reader = csv.DictReader(genes)
                input_gene_ids = list([row['input_id'] for row in input_reader])
        elif extension == "json":
            import json
            with open(input_genes) as genes:
                input_json = json.loads(genes)
                # assume records format
                input_gene_ids = [record["hit_id"] for record in input_json]
        elif extension is None:
            input_gene_ids = input_obj

        most_common_tissues = asyncio.run(self.mod.gene_to_tissue_biclusters_async(input_gene_ids))

        self.results = pd.DataFrame.from_records(most_common_tissues, columns=["hit_id", "score"])

        if self.results is not None:
            print(self.results.to_json())

if __name__ == '__main__':
    fire.Fire(GeneToTissueBiclusters)
