#!/usr/bin/env python3

import asyncio
import pandas as pd
import fire

import sys

from translator_modules.wf9.util.biclusterco import CoocurrenceByBicluster
from translator_modules.core import Payload


class GeneToGeneBiclusters(Payload):

    def __init__(self, input_gene_list_file=None):

        GeneCoocurrenceByBiclusterObject = CoocurrenceByBicluster()
        CAD_geneset = {'ENSG00000121410',
                       'ENSG00000268895',
                       'ENSG00000148584',
                       'ENSG00000070018',
                       'ENSG00000175899',
                       'ENSG00000245105',
                       'ENSG00000166535',
                       'ENSG00000256661',
                       'ENSG00000256904',
                       'ENSG00000256069',
                       'ENSG00000234906',
                       'ENSG00000068305',
                       'ENSG00000070018'
                       }

        loop = asyncio.get_event_loop()
        related_biclusters_and_genes_for_each_input_gene = loop.run_until_complete(
            GeneCoocurrenceByBiclusterObject.gene_to_gene_biclusters_async(CAD_geneset))
        bicluster_occurences_dict = GeneCoocurrenceByBiclusterObject.bicluster_occurences_dict(
            related_biclusters_and_genes_for_each_input_gene)
        unique_biclusters = GeneCoocurrenceByBiclusterObject.unique_biclusters(bicluster_occurences_dict)

        print(len(unique_biclusters))


if __name__ == '__main__':
    fire.Fire(GeneToGeneBiclusters)
