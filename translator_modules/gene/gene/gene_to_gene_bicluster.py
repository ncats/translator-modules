#!/usr/bin/env python3

# Workflow 9, Gene-to-Gene Bicluster
import asyncio
import concurrent.futures
import urllib.request
from collections import defaultdict
from datetime import datetime

import fire
import pandas as pd
import requests

from translator_modules.core.module_payload import Payload, fix_curies

bicluster_gene_url = 'https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_v3_gene/'
bicluster_bicluster_url = 'https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_v3_bicluster/'
related_biclusters_and_genes_for_each_input_gene = defaultdict(dict)


class BiclusterByGeneToGene():
    def __init__(self):
        self.meta = {
            'source': 'RNAseqDB Biclustering',
            'association': 'gene to gene association',
            'input_type': {
                'complexity': 'set',
                'id_type': 'ENSEMBL',
                'data_type': 'gene',
            },
            'relationship': 'related_to',
            'output_type': {
                'complexity': 'set',
                'id_type': 'ENSEMBL',
                'data_type': 'gene',
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

    ### !!! this is the non-async version of the code... it works but it is slow. kept for reference. !!!
    @DeprecationWarning
    def find_related_biclusters(self, curated_ID_list):
        # this function is an artifact... a way to understand 'find_related_biclusters_async', below
        for gene in curated_ID_list:
            request_1_url = bicluster_gene_url + gene + '/'
            response = requests.get(request_1_url)
            response_json = response.json()
            cooccurrence_dict_each_gene = defaultdict(dict)
            cooccurrence_dict_each_gene['related_biclusters'] = defaultdict(dict)
            cooccurrence_dict_each_gene['number_of_related_biclusters'] = len(response_json)
            for x in response_json:
                bicluster_dict = defaultdict(dict)
                cooccurrence_dict_each_gene['related_biclusters'][x['bicluster']] = []
                for related_bicluster in cooccurrence_dict_each_gene['related_biclusters']:
                    request_2_url = bicluster_bicluster_url + related_bicluster + '/'
                    response_2 = requests.get(request_2_url)
                    response_2_json = response_2.json()
                    gene_in_each_bicluster_list = [bicluster['gene'] for bicluster in response_2_json]
                    cooccurrence_dict_each_gene['related_biclusters'][related_bicluster] = gene_in_each_bicluster_list
            related_biclusters_and_genes_for_each_input_gene[gene] = dict(cooccurrence_dict_each_gene)
        return related_biclusters_and_genes_for_each_input_gene

    async def gene_to_gene_biclusters_async(self, curated_ID_list):
        start_time = datetime.now()

        bicluster_url_list = [bicluster_gene_url + gene + '/' + '?include_similar=true' for gene in curated_ID_list]
        length_bicluster_url_list = len(bicluster_url_list)

        with concurrent.futures.ThreadPoolExecutor(
                max_workers=2) as executor_1:  # changing the # of workers does not change performance...
            loop_1 = asyncio.get_event_loop()
            futures_1 = [loop_1.run_in_executor(executor_1, requests.get, request_1_url) for request_1_url in
                         bicluster_url_list]
            for response in await asyncio.gather(*futures_1):
                cooccurrence_dict_each_gene = defaultdict(dict)
                cooccurrence_dict_each_gene['related_biclusters'] = defaultdict(dict)
                response_json = response.json()
                length_response_json = len(response_json)
                cooccurrence_dict_each_gene['number_of_related_biclusters'] = length_response_json

                if length_response_json > 0:
                    gene = response_json[0]['gene']
                    for x in response_json:
                        bicluster = x['bicluster']
                        cooccurrence_dict_each_gene['related_biclusters'][x['bicluster']] = []
                    related_biclusters = [x for x in cooccurrence_dict_each_gene['related_biclusters']]
                    bicluster_bicluster_url_list = [bicluster_bicluster_url + related_bicluster + '/' for
                                                    related_bicluster in related_biclusters]
                    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor_2:
                        loop_2 = asyncio.get_event_loop()
                        futures_2 = [loop_2.run_in_executor(executor_2, requests.get, request_2_url) for request_2_url
                                     in bicluster_bicluster_url_list]
                        for response_2 in await asyncio.gather(*futures_2):
                            response_2_json = response_2.json()
                            genes_in_each_bicluster = [bicluster['gene'] for bicluster in response_2_json]
                            biclusterindex = [x['bicluster'] for x in response_2_json]
                            cooccurrence_dict_each_gene['related_biclusters'][
                                biclusterindex[0]] = genes_in_each_bicluster
                        related_biclusters_and_genes_for_each_input_gene[gene] = dict(cooccurrence_dict_each_gene)

        end_time = datetime.now()
        return related_biclusters_and_genes_for_each_input_gene

    # the function below returns a dictionary listing all biclusters which occur in the input with a count of how many times each bicluster occurs
    def bicluster_occurrences_dict(self, related_biclusters_and_genes_for_each_input_gene):
        bicluster_occurrences_dict = defaultdict(dict)
        for key, value in related_biclusters_and_genes_for_each_input_gene.items():
            for key, value in value.items():
                if key == 'related_biclusters':
                    for key, value in value.items():
                        if bicluster_occurrences_dict[key]:
                            bicluster_occurrences_dict[key] += 1
                        else:
                            bicluster_occurrences_dict[key] = 1
        return bicluster_occurrences_dict

    def unique_biclusters(self, bicluster_occurrences_dict):
        list_of_unique_biclusters = []
        for key, value in bicluster_occurrences_dict.items():
            if value == 1:
                list_of_unique_biclusters.append(key)
        return list_of_unique_biclusters

    # the method below lends itself to async ... reprogram it
    def genes_in_unique_biclusters(self, list_of_unique_biclusters, related_biclusters_and_genes_for_each_input_gene):
        dict_of_genes_in_unique_biclusters = defaultdict(dict)
        for key, value in related_biclusters_and_genes_for_each_input_gene.items():
            for key, value in value.items():
                if key == 'related_biclusters':
                    for key, value in value.items():
                        dict_of_genes_in_unique_biclusters[key] = []
                        if key in list_of_unique_biclusters:
                            dict_of_genes_in_unique_biclusters[key].append(value)
        return dict_of_genes_in_unique_biclusters

    def genes_in_unique_biclusters_not_in_input_gene_list(self, curated_ID_list, dict_of_genes_in_unique_biclusters):
        dict_of_genes_in_unique_biclusters_not_in_inputs = defaultdict(dict)
        for key, value in dict_of_genes_in_unique_biclusters.items():
            if value:
                for gene in value[0]:
                    if gene in curated_ID_list:
                        continue
                    if not dict_of_genes_in_unique_biclusters_not_in_inputs[gene]:
                        dict_of_genes_in_unique_biclusters_not_in_inputs[gene] = 1
                    else:
                        dict_of_genes_in_unique_biclusters_not_in_inputs[gene] += 1
        return dict_of_genes_in_unique_biclusters_not_in_inputs

    @staticmethod
    def sorted_list_of_output_genes(dict_of_genes_in_unique_biclusters_not_in_inputs):
        sorted_list_of_output_genes = sorted(
            (value, key) for (key, value) in dict_of_genes_in_unique_biclusters_not_in_inputs.items())
        sorted_list_of_output_genes.reverse()
        return sorted_list_of_output_genes

    @staticmethod
    def ids_in_unique_biclusters(list_of_unique_biclusters, related_biclusters_and_ids_for_each_input_id):
        dict_of_ids_in_unique_biclusters = defaultdict(dict)
        for key, value in related_biclusters_and_ids_for_each_input_id.items():
            for key, value in value.items():
                if key == 'related_biclusters':
                    for key, value in value.items():
                        dict_of_ids_in_unique_biclusters[key] = []
                        if key in list_of_unique_biclusters:
                            dict_of_ids_in_unique_biclusters[key].append(value)
        return dict_of_ids_in_unique_biclusters

    @staticmethod
    def ids_in_unique_biclusters_not_in_input_ID_list(curated_ID_list, dict_of_ids_in_unique_biclusters):
        dict_of_ids_in_unique_biclusters_not_in_inputs = defaultdict(dict)
        for key, value in dict_of_ids_in_unique_biclusters.items():
            if value:
                for ID in value[0]:
                    # try inserting a split fcn here and basically making a dictionary where every gene gets split and counted, etc, idk...
                    if ID in curated_ID_list:
                        continue
                    if not dict_of_ids_in_unique_biclusters_not_in_inputs[ID]:
                        dict_of_ids_in_unique_biclusters_not_in_inputs[ID] = 1
                    else:
                        dict_of_ids_in_unique_biclusters_not_in_inputs[ID] += 1
        return dict_of_ids_in_unique_biclusters_not_in_inputs


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
            if isinstance(input_obj, str):
                # Assume a comma delimited list of input identifiers?
                input_gene_ids = input_obj.split(',')
            else:
                # Assume that an iterable Tuple or equivalent is given here
                input_gene_ids = input_obj

        related_biclusters_and_genes_for_each_input_gene = \
            asyncio.run(self.mod.gene_to_gene_biclusters_async(input_gene_ids))

        #print("related biclusters", related_biclusters_and_genes_for_each_input_gene)

        bicluster_occurrences_dict = \
            self.mod.bicluster_occurrences_dict(related_biclusters_and_genes_for_each_input_gene)
        unique_biclusters = self.mod.unique_biclusters(bicluster_occurrences_dict)
        genes_in_unique_biclusters = \
            self.mod.genes_in_unique_biclusters(unique_biclusters, related_biclusters_and_genes_for_each_input_gene)
        genes_in_unique_biclusters_not_in_input_gene_list = \
            self.mod.genes_in_unique_biclusters_not_in_input_gene_list(input_genes, genes_in_unique_biclusters)

        # need to convert the raw Ensembl ID's to CURIES
        genes_in_unique_biclusters_not_in_input_gene_list = \
            fix_curies(genes_in_unique_biclusters_not_in_input_gene_list, prefix='ENSEMBL')

        sorted_list_of_output_genes = \
            self.mod.sorted_list_of_output_genes(genes_in_unique_biclusters_not_in_input_gene_list)

        self.results = pd.DataFrame.from_records(sorted_list_of_output_genes, columns=["score", "hit_id"])


if __name__ == '__main__':
    fire.Fire(GeneToGeneBiclusters)