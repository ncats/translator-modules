#!/usr/bin/env python3

# Workflow 9, Gene-to-CellLine Bicluster
import asyncio
import fire
import pandas as pd

from biolink.model import GeneToGeneAssociation, Gene, CellLine

from ncats.translator.core.module_payload import Payload
from ncats.translator.core.data_transfer_model import ModuleMetaData, ConceptSpace

from ncats.translator.modules.gene.gene_bicluster_shared import GenericGeneByGeneBicluster


class DepMapBiclusters(Payload):

    def __init__(self, input_genes=None, keep_input_id=True):
        super(DepMapBiclusters, self).__init__(
            module=GenericGeneByGeneBicluster(
                bicluster_url='https://smartbag-crispridepmap.ncats.io/biclusters_DepMap_gene_to_cellline_v1_gene/',
                bicluster_bicluster_url='https://smartbag-crispridepmap.ncats.io/biclusters_DepMap_gene_to_cellline_v1_bicluster/',
                target_prefix='NCBI'
            )
        )

        if not input_genes:
            raise RuntimeError("DepMapBiclusters ERROR: missing mandatory input_genes parameter")

        input_gene_set = self.get_simple_input_identifier_list(input_genes)

        asyncio.run(self.module.gene_to_gene_biclusters_async(input_gene_set))

        sorted_list_of_output_genes = self.module.gene_to_gene_bicluster_summarize(input_gene_set, keep_input_id)

        self.results = pd.DataFrame.from_records(sorted_list_of_output_genes)


DepMapBiclusters.set_metadata(
    ModuleMetaData(
        name="Mod9B - Gene-to-CellLine Bicluster",
        source='DepMap Biclustering',
        association=GeneToGeneAssociation,
        domain=ConceptSpace(Gene, ['NCBI']),
        relationship='related_to',
        range=ConceptSpace(CellLine, ['ACH'])
    )
)


def metadata():
    """
    Retrieve Module Metadata
    """
    return DepMapBiclusters.get_metadata()


def main():
    fire.Fire(DepMapBiclusters)


if __name__ == '__main__':
    main()