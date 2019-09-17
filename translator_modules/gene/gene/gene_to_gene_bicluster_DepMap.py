#!/usr/bin/env python3

# Workflow 9, Gene-to-CellLine Bicluster
import asyncio
import fire
import pandas as pd

from biolink.model import GeneToGeneAssociation, Gene, CellLine

from translator_modules.core.module_payload import Payload
from translator_modules.core.data_transfer_model import ModuleMetaData, ConceptSpace
from translator_modules.gene.gene_bicluster_shared import BiclusterByGene


class GeneToGeneDepMapBiclusters(Payload):

    def __init__(self, input_genes):
        super(GeneToGeneDepMapBiclusters, self).__init__(
            module=BiclusterByGene(
                bicluster_url='https://smartbag-crispridepmap.ncats.io/biclusters_DepMap_gene_to_cellline_v1_gene/',
                bicluster_bicluster_url='https://smartbag-crispridepmap.ncats.io/biclusters_DepMap_gene_to_cellline_v1_bicluster/',
                target_prefix=''
            ),
            metadata=ModuleMetaData(
                name="Mod9B - Gene-to-Gene Bicluster",
                source='DepMap Biclustering',
                association=GeneToGeneAssociation,
                domain=ConceptSpace(Gene, ['NCBI']),
                relationship='related_to',
                range=ConceptSpace(Gene, ['NCBI'])
            )
        )

        input_gene_set = self.get_simple_input_identifier_list(input_genes)

        asyncio.run(self.module.gene_to_gene_biclusters_async(input_gene_set))

        sorted_list_of_output_genes = self.module.gene_to_gene_bicluster_summarize(input_gene_set)

        self.results = pd.DataFrame.from_records(sorted_list_of_output_genes)


if __name__ == '__main__':
    fire.Fire(GeneToGeneDepMapBiclusters)
