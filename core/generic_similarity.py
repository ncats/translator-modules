# Shared core similarity functions
from typing import List, Tuple

import pandas as pd
from ontobio.assoc_factory import AssociationSetFactory
from ontobio.assocmodel import AssociationSet

# We override the Ontobio version of the jaccard_similarity
# function below, to return shared ontology term annotation
#
# from ontobio.analysis.semsim import jaccard_similarity


class GenericSimilarity(object):

    def __init__(self) -> None:
        self.associations = None

    @staticmethod
    def jaccard_similarity(aset: AssociationSet, s1: str, s2: str) -> Tuple[float, list]:
        """
        Calculate jaccard index of inferred associations of two subjects

        |ancs(s1) /\ ancs(s2)|
        ---
        |ancs(s1) \/ ancs(s2)|

        """
        a1 = aset.inferred_types(s1)
        a2 = aset.inferred_types(s2)
        num_union = len(a1.union(a2))
        if num_union == 0:
            return 0.0, list()

        shared_terms = a1.intersection(a2)

        # Note: we need to convert the shared_terms set to a list
        # to avoid later JSON serialization problems
        return len(shared_terms) / num_union, list(shared_terms)

    def compute_jaccard(self, input_genes: List[dict], lower_bound: float = 0.7) -> List[dict]:
        similarities = []
        for index, igene in enumerate(input_genes):
            for subject_curie in self.associations.subject_label_map.keys():
                input_gene = GenericSimilarity.trim_mgi_prefix(
                    input_gene=igene['sim_input_curie'],
                    subject_curie=subject_curie
                )
                if input_gene is not subject_curie:
                    score, shared_terms = \
                        GenericSimilarity.jaccard_similarity(self.associations, input_gene, subject_curie)
                    if float(score) > float(lower_bound):
                        subject_label = self.associations.label(subject_curie)
                        # CX: addition of human-readable labels aka "shared_term_names" 
                        shared_term_names = [self.associations.label(x) for x in shared_terms]
                        similarities.append({
                            'input_id': input_gene,
                            'input_symbol': igene['input_symbol'],
                            'hit_symbol': subject_label,
                            'hit_id': subject_curie,
                            'score': score,
                            'shared_terms': shared_terms,
                            'shared_term_names': shared_term_names
                        })
        return similarities

    @staticmethod
    def trim_mgi_prefix(input_gene, subject_curie) -> str:
        if 'MGI:MGI:' in subject_curie and 'MGI:MGI:' in input_gene:
            return input_gene
        elif 'MGI:MGI:' not in subject_curie and 'MGI:MGI:' in input_gene:
            return input_gene[4:]

        else:
            return input_gene

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
