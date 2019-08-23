#!/usr/bin/env python3

import asyncio
import pandas as pd
import fire

from translator_modules.wf9.util.bicluster_disease_to_phenotype import BiclusterByDiseaseToPhenotype
from translator_modules.core.module_payload import Payload


class DiseaseToPhenotypeBiclusters(Payload):

    def __init__(self, input_diseases):
        self.mod = BiclusterByDiseaseToPhenotype()

        input_str, extension = self.handle_input_or_input_location(input_diseases)

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
            pass

        most_common_phenotype = asyncio.run(self.mod.disease_to_phenotype_biclusters_async(input_disease_ids))
        self.results = pd.DataFrame.from_records(most_common_phenotype, columns=["hit_id", "score"])

        if self.results is not None:
            print(self.results.to_json())

if __name__ == '__main__':
    fire.Fire(DiseaseToPhenotypeBiclusters)
