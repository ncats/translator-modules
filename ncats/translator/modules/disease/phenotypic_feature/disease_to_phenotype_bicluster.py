#!/usr/bin/env python3

import asyncio
import concurrent.futures
import urllib.request
from collections import defaultdict, Counter

import fire
import pandas as pd
import requests

from biolink.model import DiseaseToPhenotypicFeatureAssociation, Disease, PhenotypicFeature

from ncats.translator.core.module_payload import Payload
from ncats.translator.core.data_transfer_model import ModuleMetaData, ConceptSpace

base_disease_url = 'https://smartbag-hpotomondo.ncats.io/HPO_to_MONDO_mondo_list/'


class BiclusterByDiseaseToPhenotype():
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

    async def disease_to_phenotype_biclusters_async(self, input_id_list):
        bicluster_url_list = [base_disease_url + disease + '/' + '?include_similar=true' for disease in input_id_list]
        all_biclusters_dict = defaultdict(dict)
        with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor_1:
            all_phenotypes = []

            loop_1 = asyncio.get_event_loop()
            futures_1 = [loop_1.run_in_executor(executor_1, requests.get, request_1_url) for request_1_url in
                         bicluster_url_list]
            for response in await asyncio.gather(*futures_1):

                try:
                    response_json = response.json()
                except JSONDecodeError:
                    continue

                for x in response_json:
                    phenotype = x['hpo']
                    all_phenotypes.append(phenotype)

            phenotypes_counted = Counter(all_phenotypes)

        return phenotypes_counted.most_common()


class DiseaseToPhenotypeBiclusters(Payload):

    def __init__(self, input_diseases=None):

        super(DiseaseToPhenotypeBiclusters, self).__init__(
            module=BiclusterByDiseaseToPhenotype(),
            metadata=ModuleMetaData(
                name="Mod2.0 - Disease Associated Genes",
                source='RNAseqDB Biclustering',
                association=DiseaseToPhenotypicFeatureAssociation,
                domain=ConceptSpace(Disease, ['MONDO']),
                relationship='has_phenotype',
                range=ConceptSpace(PhenotypicFeature, ['HP']),
            )
        )

        if not input_diseases:
            raise RuntimeError("DiseaseToPhenotypeBiclusters ERROR: missing mandatory input_diseases parameter")

        input_disease_ids = self.get_simple_input_identifier_list(input_diseases)

        most_common_phenotype = asyncio.run(self.module.disease_to_phenotype_biclusters_async(input_disease_ids))

        self.results = pd.DataFrame.from_records(most_common_phenotype, columns=["hit_id", "score"])


def main():
    fire.Fire(DiseaseToPhenotypeBiclusters)


if __name__ == '__main__':
    main()