#!/usr/bin/env python3

import asyncio
import concurrent.futures
import urllib.request
from collections import defaultdict, Counter

import fire
import pandas as pd
import requests

from translator_modules.core.module_payload import Payload

bicluster_disease_url = 'https://smartbag-hpotomondo.ncats.io/HPO_to_MONDO_bicluster/'
base_phenotype_url = 'https://smartbag-hpotomondo.ncats.io/HPO_to_MONDO_hpo/'


# HP is phenotype ... example URL: https://smartbag-hpotomondo.ncats.io/HPO_to_MONDO_hpo/HP%3A0002193/?include_similar=false
# MONDO is disease ... example URL: https://smartbag-hpotomondo.ncats.io/HPO_to_MONDO_mondo_list/MONDO.0007030/?include_similar=true

# source for diabetes phenotypic features: https://bionames.renci.org/lookup/diabetes/phenotypic%20feature/?include_similar=true
# diabetes phenotypic features: ['HP:0000819', 'HP:0000873', 'HP:0005978', 'HP:0100651']

class BiclusterByPhenotypeToDisease():
    def __init__(self):
        self.meta = {
            'source': 'RNAseqDB Biclustering',
            'association': 'disease to phenotypic feature association',
            'input_type': {
                'complexity': 'set',
                'data_type': 'phenotypic feature',
                'id_type': 'HP'
            },
            'relationship': 'has_phenotype',
            'output_type': {
                'complexity': 'single',
                'data_type': 'disease',
                'id_type': ['MONDO', 'DO', 'OMIM'],
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

    async def phenotype_to_disease_biclusters_async(self, input_ID_list):
        bicluster_url_list = [base_phenotype_url + phenotype + '/' + '?include_similar=true' for phenotype in
                              input_ID_list]
        length_bicluster_url_list = len(bicluster_url_list)
        all_biclusters_dict = defaultdict(dict)
        with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor_1:
            all_diseases = []
            loop_1 = asyncio.get_event_loop()
            futures_1 = [loop_1.run_in_executor(executor_1, requests.get, request_1_url) for request_1_url in
                         bicluster_url_list]
            for response in await asyncio.gather(*futures_1):
                response_json = response.json()
                for x in response_json:
                    disease = x['mondo_list'].split('__')
                    for y in disease:
                        all_diseases.append(y)
            disease_counted = Counter(all_diseases)
        return disease_counted.most_common()


class PhenotypeToDiseaseBiclusters(Payload):

    def __init__(self, input_phenotypes):
        self.mod = BiclusterByPhenotypeToDisease()
        input_obj, extension = self.handle_input_or_input_location(input_phenotypes)

        input_phenotype_ids: list
        # NB: push this out to the handle_input_or_input_location function?
        if extension == "csv":
            import csv
            with open(input_phenotypes) as genes:
                input_reader = csv.DictReader(genes)
                input_phenotype_ids = list(set([row['input_id'] for row in input_reader]))
        # TODO: handle JSON
        elif extension == "json":
            import json
            with open(input_phenotypes) as genes:
                input_json = json.loads(genes)
                # assume records format
                input_phenotype_ids = [record["hit_id"] for record in input_json]
        elif extension is None:
            if isinstance(input_obj, str):
                # Assume a comma delimited list of input identifiers?
                input_phenotype_ids = input_obj.split(',')
            else:
                # Assume that an iterable Tuple or equivalent is given here
                input_phenotype_ids = input_obj

        most_common_diseases = asyncio.run(self.mod.phenotype_to_disease_biclusters_async(input_phenotype_ids))
        self.results = pd.DataFrame.from_records(most_common_diseases, columns=["hit_id", "score"])


if __name__ == '__main__':
    fire.Fire(PhenotypeToDiseaseBiclusters)
