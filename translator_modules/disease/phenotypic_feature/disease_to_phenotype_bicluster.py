#!/usr/bin/env python3

import asyncio
import concurrent.futures
import urllib.request
from collections import defaultdict, Counter

import fire
import pandas as pd
import requests

from BioLink.model import DiseaseToPhenotypicFeatureAssociation, Disease, PhenotypicFeature

from translator_modules.core.module_payload import Payload

base_disease_url = 'https://smartbag-hpotomondo.ncats.io/HPO_to_MONDO_mondo_list/'


class BiclusterByDiseaseToPhenotype():
    def __init__(self):
        self.meta = {
            'source': 'RNAseqDB Biclustering',
            'association': DiseaseToPhenotypicFeatureAssociation.class_name,
            'input_type': {
                'complexity': 'single',
                'category': Disease.class_name,
                'mappings': 'MONDO',
            },
            'relationship': 'has_phenotype',
            'output_type': {
                'complexity': 'set',
                'category': PhenotypicFeature.class_name,
                'mappings': 'HP',
            },
        }

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

    async def disease_to_phenotype_biclusters_async(self, input_ID_list):
        bicluster_url_list = [base_disease_url + disease + '/' + '?include_similar=true' for disease in input_ID_list]
        all_biclusters_dict = defaultdict(dict)
        with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor_1:
            all_phenotypes = []

            loop_1 = asyncio.get_event_loop()
            futures_1 = [loop_1.run_in_executor(executor_1, requests.get, request_1_url) for request_1_url in
                         bicluster_url_list]
            for response in await asyncio.gather(*futures_1):
                response_json = response.json()
                for x in response_json:
                    phenotype = x['hpo']
                    all_phenotypes.append(phenotype)

            phenotypes_counted = Counter(all_phenotypes)
        return phenotypes_counted.most_common()


class DiseaseToPhenotypeBiclusters(Payload):

    def __init__(self, input_diseases):

        super(DiseaseToPhenotypeBiclusters, self).__init__(BiclusterByDiseaseToPhenotype())

        input_obj, extension = self.handle_input_or_input_location(input_diseases)

        input_disease_ids: list
        # NB: push this out to the handle_input_or_input_location function?
        if extension == "csv":
            import csv
            with open(input_diseases) as genes:
                input_reader = csv.DictReader(genes)
                input_disease_ids = list([row['input_id'] for row in input_reader])
        elif extension == "json":
            import json
            with open(input_diseases) as genes:
                input_json = json.loads(genes)
                # assume records format
                input_disease_ids = [record["hit_id"] for record in input_json]
        elif extension is None:
            input_disease_ids = input_obj

        most_common_phenotype = asyncio.run(self.mod.disease_to_phenotype_biclusters_async(input_disease_ids))
        self.results = pd.DataFrame.from_records(most_common_phenotype, columns=["hit_id", "score"])


if __name__ == '__main__':
    fire.Fire(DiseaseToPhenotypeBiclusters)
