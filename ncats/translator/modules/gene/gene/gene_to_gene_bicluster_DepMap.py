#!/usr/bin/env python3

# Workflow 9, Gene-to-CellLine Bicluster
import asyncio
import fire
import pandas as pd

from biolink.model import GeneToGeneAssociation, Gene

from ncats.translator.modules.gene.gene_bicluster_shared import GenericGeneByGeneBicluster

from ncats.translator.core.module_payload import Payload
from ncats.translator.core.data_transfer_model import ModuleMetaData, ConceptSpace


class GeneToGeneDepMapBiclusters(Payload):

    def __init__(self, input_genes=None, keep_input_id=True):

        super(GeneToGeneDepMapBiclusters, self).__init__(
            module=GenericGeneByGeneBicluster(
                bicluster_url='https://smartbag-crispridepmap.ncats.io/biclusters_DepMap_gene_to_cellline_v1_gene/',
                bicluster_bicluster_url='https://smartbag-crispridepmap.ncats.io/biclusters_DepMap_gene_to_cellline_v1_bicluster/',
                target_prefix='NCBI'
            )
        )

        if not input_genes:
            raise RuntimeError("GeneToGeneDepMapBiclusters ERROR: missing mandatory input_genes parameter")

        input_gene_set = self.get_simple_input_identifier_list(input_genes)

        asyncio.run(self.module.gene_to_gene_biclusters_async(input_gene_set))

        sorted_list_of_output_genes = self.module.gene_to_gene_bicluster_summarize(input_gene_set, keep_input_id)

        self.results = pd.DataFrame.from_records(sorted_list_of_output_genes)


GeneToGeneDepMapBiclusters.set_metadata(
    ModuleMetaData(
        name="Mod9B - Gene-to-Gene Bicluster",
        source='DepMap Biclustering',
        association=GeneToGeneAssociation,
        domain=ConceptSpace(Gene, ['NCBI']),
        relationship='related_to',
        range=ConceptSpace(Gene, ['NCBI'])
    )
)


def metadata():
    """
    Retrieve Module Metadata
    """
    return GeneToGeneDepMapBiclusters.get_metadata()


def main():
    fire.Fire(GeneToGeneDepMapBiclusters)


if __name__ == '__main__':
    main()