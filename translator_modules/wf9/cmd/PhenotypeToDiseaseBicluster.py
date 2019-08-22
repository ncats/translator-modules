#!/usr/bin/env python3

import asyncio
import pandas as pd
import fire

from translator_modules.wf9.util.bicluster_phenotype_to_disease import phenotype_to_disease
from translator_modules.core.module_payload import Payload


class PhenotypeToDiseaseBiclusters(Payload):

    def __init__(self, input_phenotype):
        self.mod = phenotype_to_disease()
        input_str, extension = self.handle_input_or_input_location(input_phenotype)

        input_phenotype_ids: list
        # NB: push this out to the handle_input_or_input_location function?
        if extension == "csv":
            import csv
            with open(input_phenotype) as genes:
                input_reader = csv.DictReader(genes)
                input_phenotype_ids = list(set([row['input_id'] for row in input_reader]))
        # TODO: handle JSON
        elif extension == "json":
            import json
            with open(input_phenotype) as genes:
                input_json = json.loads(genes)
                # assume records format
                input_phenotype_ids = [record["hit_id"] for record in input_json]
        elif extension is None:
            pass

        most_common_diseases = asyncio.run(self.mod.phenotype_to_disease_biclusters_async(input_phenotype_ids))
        self.results = pd.DataFrame.from_records(most_common_diseases, columns=["hit_id", "score"])

        if self.results is not None:
            print(self.results.to_json())

if __name__ == '__main__':
    fire.Fire(PhenotypeToDiseaseBiclusters)
