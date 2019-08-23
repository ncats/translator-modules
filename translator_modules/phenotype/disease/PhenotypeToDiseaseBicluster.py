#!/usr/bin/env python3

import asyncio

import fire
import pandas as pd

from translator_modules.core.module_payload import Payload
from translator_modules.phenotype.disease.bicluster_phenotype_to_disease import BiclusterByPhenotypeToDisease


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
            input_phenotype_ids = input_obj

        most_common_diseases = asyncio.run(self.mod.phenotype_to_disease_biclusters_async(input_phenotype_ids))
        self.results = pd.DataFrame.from_records(most_common_diseases, columns=["hit_id", "score"])

        if self.results is not None:
            print(self.results.to_json())

if __name__ == '__main__':
    fire.Fire(PhenotypeToDiseaseBiclusters)
