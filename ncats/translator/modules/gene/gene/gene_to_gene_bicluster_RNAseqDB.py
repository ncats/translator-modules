#!/usr/bin/env python3

# Workflow 9, Gene-to-CellLine Bicluster
import asyncio
import fire
import pandas as pd

from biolink.model import GeneToGeneAssociation, Gene

from ncats.translator.core.module_payload import Payload
from ncats.translator.core.data_transfer_model import ModuleMetaData, ConceptSpace

from ncats.translator.modules.gene.gene_bicluster_shared import GenericGeneByGeneBicluster


class GeneToGeneRNASeqDbBiclusters(Payload):

    def __init__(self, input_genes=None, keep_input_id=True):

        super(GeneToGeneRNASeqDbBiclusters, self).__init__(
            module=GenericGeneByGeneBicluster(
                bicluster_url='https://smartbag.ncats.io/RNAseqDB_bicluster_gene_to_tissue_v3_gene/',
                bicluster_bicluster_url='https://smartbag.ncats.io/RNAseqDB_bicluster_gene_to_tissue_v3_bicluster/',
                target_prefix='ENSEMBL'
            )
        )

        if not input_genes:
            raise RuntimeError("GeneToGeneRNASeqDbBiclusters ERROR: missing mandatory input_genes parameter")

        input_gene_set = self.get_simple_input_identifier_list(input_genes)

        asyncio.run(self.module.gene_to_gene_biclusters_async(input_gene_set))

        sorted_list_of_output_genes = self.module.gene_to_gene_bicluster_summarize(input_gene_set, keep_input_id)

        self.results = pd.DataFrame.from_records(sorted_list_of_output_genes)


GeneToGeneRNASeqDbBiclusters.set_metadata(
    ModuleMetaData(
        name="Mod9B - Gene-to-Gene Bicluster",
        source='RNAseqDB Biclustering',
        association=GeneToGeneAssociation,
        domain=ConceptSpace(Gene, ['ENSEMBL']),
        relationship='related_to',
        range=ConceptSpace(Gene, ['ENSEMBL']),
    )
)


def metadata():
    """
    Retrieve Module Metadata
    """
    return GeneToGeneRNASeqDbBiclusters.get_metadata()


def main():
    fire.Fire(GeneToGeneRNASeqDbBiclusters)


if __name__ == '__main__':
    main()