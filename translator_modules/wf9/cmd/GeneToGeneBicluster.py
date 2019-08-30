#!/usr/bin/env python3

import asyncio
import pandas as pd
import fire

from translator_modules.wf9.util.bicluster_gene_to_gene import BiclusterByGeneToGene
from translator_modules.core.module_payload import Payload


class GeneToGeneBiclusters(Payload):

    def __init__(self, input_genes):

        self.mod = BiclusterByGeneToGene()

        input_obj, extension = self.handle_input_or_input_location(input_genes)

        input_gene_ids: list
        # NB: push this out to the handle_input_or_input_location function?
        if extension == "csv":
            import csv
            with open(input_genes) as genes:
                input_reader = csv.DictReader(genes)
                input_gene_ids = [row['input_id'] for row in input_reader]
        elif extension == "json":
            import json
            with open(input_genes) as genes:
                input_json = json.loads(genes)
                # assume records format
                input_gene_ids = [record["hit_id"] for record in input_json]
        elif extension is None:
            input_gene_ids = input_obj

        related_biclusters_and_genes_for_each_input_gene = asyncio.run(self.mod.gene_to_gene_biclusters_async(input_gene_ids))

        #print("related biclusters", related_biclusters_and_genes_for_each_input_gene)

        bicluster_occurrences_dict = self.mod.bicluster_occurrences_dict(related_biclusters_and_genes_for_each_input_gene)
        unique_biclusters = self.mod.unique_biclusters(bicluster_occurrences_dict)
        genes_in_unique_biclusters = self.mod.genes_in_unique_biclusters(unique_biclusters, related_biclusters_and_genes_for_each_input_gene)
        genes_in_unique_biclusters_not_in_input_gene_list = self.mod.genes_in_unique_biclusters_not_in_input_gene_list(input_genes, genes_in_unique_biclusters)
        sorted_list_of_output_genes = self.mod.sorted_list_of_output_genes(genes_in_unique_biclusters_not_in_input_gene_list)
        self.results = pd.DataFrame.from_records(sorted_list_of_output_genes, columns=["score", "hit_id"])

        if self.results is not None:
            print(self.results.to_json())


if __name__ == '__main__':
    fire.Fire(GeneToGeneBiclusters)