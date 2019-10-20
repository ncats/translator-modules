# Shared core similarity functions

from typing import List, Tuple

import pandas as pd
from ontobio.assocmodel import AssociationSet

#
# We override the direct Ontobio version of the Jaccard_Similarity
# function below, to return shared ontology term annotation
#
# from ontobio.analysis.semsim import jaccard_similarity


class GenericSimilarity(object):

    def __init__(self) -> None:
        self.ont = ''
        self.taxon = ''

    def compute_jaccard(self, input_genes: List[dict], lower_bound: float = 0.7) -> List[dict]:
        similarities = []
        # need to call the remote service here, tagged  with self.taxon and self.ont to be used
        return similarities

    @staticmethod
    def sort_results(results) -> pd.DataFrame:

        results = pd.DataFrame(results)

        if not results.empty:
            # CX: Some users need to know the scores that input genes have for each other.
            #     replacing code to remove GeneA input = GeneA output results
            results = \
                results[~(results.hit_id == results.input_id)]. \
                sort_values('score', ascending=False)

        return results
