#!/usr/bin/env python3

import asyncio
import pandas as pd
import fire

from translator_modules.wf9.util.bicluster_tissue_to_gene import BiclusterByTissueToGene
from translator_modules.core.module_payload import Payload


class TissueToGeneBicluster(Payload):

    def __init__(self, input_tissues):
        self.mod = BiclusterByTissueToGene()
        input_obj, extension = self.handle_input_or_input_location(input_tissues)

        input_tissue_ids: list
        # NB: push this out to the handle_input_or_input_location function?
        if extension == "csv":
            import csv
            with open(input_tissues) as genes:
                input_reader = csv.DictReader(genes)
                input_tissue_ids = list(set([row['input_id'] for row in input_reader]))
        elif extension == "json":
            import json
            with open(input_tissues) as genes:
                input_json = json.loads(genes)
                # assume records format
                input_tissue_ids = [record["hit_id"] for record in input_json]
        elif extension is None:
            input_tissue_ids = input_obj

        most_common_tissues = asyncio.run(self.mod.tissue_to_gene_biclusters_async(input_tissue_ids))
        self.results = pd.DataFrame.from_records(most_common_tissues, columns=["hit_id", "score"])

        if self.results is not None:
            print(self.results.to_json())

if __name__ == '__main__':
    fire.Fire(TissueToGeneBicluster)
