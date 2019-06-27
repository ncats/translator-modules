#!/usr/bin/python3

import fire
from biocwl import BiolinkWorkflow


class GeneByDisease(BiolinkWorkflow):
    def __init__(self):
        #self.spec = self._read_spec()
        super().__init__()
        """
        {
            'input_type': {
                'complexity': 'single',
                'id_type': ['MONDO', 'DO', 'OMIM'],
                'data_type': 'disease'
            },cd 
            'output_type': {
                'complexity': 'set',
                'id_type': 'HGNC',
                'data_type': 'gene'
            },
            'taxon': 'human',
            'limit': None,
            'source': 'Monarch Biolink',
            'predicate': 'blm:gene associated with condition'
        }
        """

    # todo: how do we ensure integrity between these type arguments and the spec
        # in this case there is no bridge for inference from the spec. on the other hand these types are only
        # weakly enforced and are thus strictly optional, meant mainly for the developer's convenience
    def _process_input(self, input):
        # todo delegate the mod0 processing into here!
        dataFrame = module0.DiseaseAssociatedGeneSet(input_disease_name='', input_disease_mondo='').get_data_frame()
        return dataFrame


if __name__ == '__main__':
    fire.Fire(GeneByDisease)
