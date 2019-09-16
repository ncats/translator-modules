#!/usr/bin/env python3

# Workflow 9, Gene-to-Gene Bicluster
import asyncio
import concurrent.futures
import urllib.request
from collections import defaultdict

import fire
import pandas as pd
import requests
from typing import Dict, List

from biolink.model import GeneToGeneAssociation, Gene

from translator_modules.core import fix_curies
from translator_modules.core.module_payload import Payload
from translator_modules.core.data_transfer_model import ModuleMetaData, ConceptSpace

bicluster_gene_url = 'https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_v3_gene/'
bicluster_bicluster_url = 'https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_v3_bicluster/'


class BiclusterByGeneToGene():

    def __init__(self):
        self.related_biclusters_and_genes_for_each_input_gene = defaultdict(dict)

    @staticmethod
    def get_id_list(id_list_url):
        with urllib.request.urlopen(id_list_url) as url:
            id_list = url.read().decode().split('\n')
        return id_list

    @staticmethod
    def curated_id_list(id_list):
        curated_id_list = []
        for identifier in id_list:
            if not identifier:
                continue
            else:
                identifier = identifier.split(None, 1)[0]
                identifier = identifier.lower()
                curated_id_list.append(identifier)
        return curated_id_list

    def run_get_input(self, id_list_url):
        id_list = self.get_id_list(id_list_url)
        curated_id_list = self.curated_id_list(id_list)
        return curated_id_list

    ### !!! this is the non-async version of the code... it works but it is slow. kept for reference. !!!
    @DeprecationWarning
    def find_related_biclusters(self, curated_id_list):
        # this function is an artifact... a way to understand 'find_related_biclusters_async', below
        for gene in curated_id_list:
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
            self.related_biclusters_and_genes_for_each_input_gene[gene] = dict(cooccurrence_dict_each_gene)

    async def gene_to_gene_biclusters_async(self, curated_id_list):

        bicluster_url_list = [bicluster_gene_url + gene + '/' + '?include_similar=true' for gene in curated_id_list]
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
                        cooccurrence_dict_each_gene['related_biclusters'][x['bicluster']] = defaultdict(dict)
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
                        self.related_biclusters_and_genes_for_each_input_gene[gene] = dict(cooccurrence_dict_each_gene)

    # the function below returns a dictionary listing all biclusters which occur in the input with a count of how many times each bicluster occurs
    def bicluster_occurrences_dict(self):
        bicluster_occurrences_dict = defaultdict(dict)
        for related_biclusters in self.related_biclusters_and_genes_for_each_input_gene.values():
            for bicluster_id in related_biclusters['related_biclusters'].keys():
                if bicluster_id in bicluster_occurrences_dict:
                    bicluster_occurrences_dict[bicluster_id] += 1
                else:
                    bicluster_occurrences_dict[bicluster_id] = 1
        return bicluster_occurrences_dict

    def unique_biclusters(self, bicluster_occurrences_dict):
        list_of_unique_biclusters = []
        for key, value in bicluster_occurrences_dict.items():
            if value == 1:
                list_of_unique_biclusters.append(key)
        return list_of_unique_biclusters

    # the method below lends itself to async ... reprogram it
    def genes_in_unique_biclusters(self, list_of_unique_biclusters):
        dict_of_genes_in_unique_biclusters = defaultdict(Dict[str, List])
        for related_biclusters in self.related_biclusters_and_genes_for_each_input_gene.values():
            for bicluster_id, genes in related_biclusters['related_biclusters'].items():
                if bicluster_id in list_of_unique_biclusters and \
                        bicluster_id not in dict_of_genes_in_unique_biclusters:
                    dict_of_genes_in_unique_biclusters[bicluster_id] = list(genes)
        return dict_of_genes_in_unique_biclusters

    @staticmethod
    def genes_in_unique_biclusters_not_in_input_gene_list(curated_id_list, dict_of_genes_in_unique_biclusters):
        dict_of_genes_in_unique_biclusters_not_in_inputs = defaultdict(dict)
        for gene_list in dict_of_genes_in_unique_biclusters.values():
            if gene_list:
                # using an array here in case a unique
                # bicluster shares more than one input gene
                input_id = []
                for gene in gene_list:
                    # curated input id's may be not have versions therefore need
                    # to only compare the object_id part with the curated input list
                    id_part = gene.split('.')
                    if id_part[0] in curated_id_list or gene in curated_id_list:
                        input_id.append(gene)
                        continue
                    if gene not in dict_of_genes_in_unique_biclusters_not_in_inputs:
                        dict_of_genes_in_unique_biclusters_not_in_inputs[gene] = {'input_id': input_id, 'score': 1}
                    else:
                        dict_of_genes_in_unique_biclusters_not_in_inputs[gene]['score'] += 1
        return dict_of_genes_in_unique_biclusters_not_in_inputs

    @staticmethod
    def list_of_output_genes_sorted_high_to_low_count(dict_of_genes_in_unique_biclusters_not_in_inputs):
        score_list = [
            {
                'input_id': ','.join(fix_curies(tally['input_id'], prefix='ENSEMBL')),
                'hit_id': gene,
                'score': tally['score']
            } for (gene, tally) in dict_of_genes_in_unique_biclusters_not_in_inputs.items()
        ]
        sorted_list_of_output_genes = sorted(score_list, key=lambda item: item['score'], reverse=True)
        return sorted_list_of_output_genes

    @staticmethod
    # Not sure that this function is ever used in the module anymore?
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
    def ids_in_unique_biclusters_not_in_input_id_list(curated_id_list, dict_of_ids_in_unique_biclusters):
        dict_of_ids_in_unique_biclusters_not_in_inputs = defaultdict(dict)
        for key, value in dict_of_ids_in_unique_biclusters.items():
            if value:
                for ID in value[0]:
                    # try inserting a split fcn here and basically making
                    # a dictionary where every gene gets split and counted, etc, idk...
                    if ID in curated_id_list:
                        continue
                    if not dict_of_ids_in_unique_biclusters_not_in_inputs[ID]:
                        dict_of_ids_in_unique_biclusters_not_in_inputs[ID] = 1
                    else:
                        dict_of_ids_in_unique_biclusters_not_in_inputs[ID] += 1
        return dict_of_ids_in_unique_biclusters_not_in_inputs

    def summmarize(self, input_gene_set):

        bicluster_occurrences_dict = self.bicluster_occurrences_dict()

        unique_biclusters = self.unique_biclusters(bicluster_occurrences_dict)

        genes_in_unique_biclusters = self.genes_in_unique_biclusters(unique_biclusters)

        genes_in_unique_biclusters_not_in_input_gene_list = \
            self.genes_in_unique_biclusters_not_in_input_gene_list(input_gene_set, genes_in_unique_biclusters)

        # need to convert the raw Ensembl ID's to CURIES
        genes_in_unique_biclusters_not_in_input_gene_list = \
            fix_curies(genes_in_unique_biclusters_not_in_input_gene_list, prefix='ENSEMBL')

        sorted_list_of_output_genes = \
            self.list_of_output_genes_sorted_high_to_low_count(genes_in_unique_biclusters_not_in_input_gene_list)

        return sorted_list_of_output_genes


class GeneToGeneBiclusters(Payload):

    def __init__(self, input_genes):

        super(GeneToGeneBiclusters, self).__init__(
            module=BiclusterByGeneToGene(),
            metadata=ModuleMetaData(
                name="Mod9A - Gene-to-Gene Bicluster",
                source='RNAseqDB Biclustering',
                association=GeneToGeneAssociation,
                domain=ConceptSpace(Gene, ['ENSEMBL']),
                relationship='related_to',
                range=ConceptSpace(Gene, ['ENSEMBL']),
            )
        )

        input_gene_set = get_simple_input_gene_list(input_genes)

        asyncio.run(self.module.gene_to_gene_biclusters_async(input_gene_set))

        sorted_list_of_output_genes = self.module.summarize(input_gene_set)

        self.results = pd.DataFrame.from_records(sorted_list_of_output_genes)


if __name__ == '__main__':
    fire.Fire(GeneToGeneBiclusters)
