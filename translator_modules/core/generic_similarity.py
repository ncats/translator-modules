# Shared core similarity functions
from ontobio.ontol_factory import OntologyFactory
from ontobio.io.gafparser import GafParser
from ontobio.assoc_factory import AssociationSetFactory
from typing import List
import pandas as pd

# We override the Ontobio version of the jaccard_similarity
# function below, to return shared ontology term annotation
#
# from ontobio.analysis.semsim import jaccard_similarity

from ontobio.assocmodel import AssociationSet

###################################################################
# First, before loading all our ontobio dependent analysis modules,
# we need to tweak OntoBio to disable its @cachier cache. Our
# patched Ontobio has an 'ignore_cache' flag which may be
# overridden here before the rest of the system is loaded.
# We do this because cachier seems to introduce an odd system
# instability resulting in deep recursion on one method,
# creating new threads and consuming stack memory to the point
# of system resource exhaustion!  We conjecture that cachier
# caching is unnecessary since we read the pertinent ontology
# catalogs in just once into memory, for readonly reuse.
###################################################################
from ontobio.config import get_config
get_config().ignore_cache = True


class GenericSimilarity(object):

    def __init__(self) -> None:
        self.associations = ''
        self.ontology = ''
        self.assocs = ''
        self.afactory = AssociationSetFactory()

    def load_associations(self, taxon):
        taxon_map = {
            'human': 'NCBITaxon:9606',
            'mouse': 'NCBITaxon:10090',
        }
        ofactory = OntologyFactory()
        self.ontology = ofactory.create(self.ont)
        p = GafParser()
        url = ''
        if self.ont == 'go':
            # CX: GO:0008150 is biological_process, GO:0003674 is molecular_function. 
            # CX: These are 2 out of 3 top-level terms in GO ontology. 
            # CX: The excluded term is cellular_component (where gene carries out a molecular function)
            go_roots = set(self.ontology.descendants('GO:0008150') + self.ontology.descendants('GO:0003674'))
            sub_ont = self.ontology.subontology(go_roots)
            if taxon == 'mouse':
                url = "http://current.geneontology.org/annotations/mgi.gaf.gz"
            if taxon == 'human':
                url = "http://current.geneontology.org/annotations/goa_human.gaf.gz"
            assocs = p.parse(url)
            self.assocs = assocs
            assocs = [x for x in assocs if 'header' not in x.keys()]
            assocs = [x for x in assocs if x['object']['id'] in go_roots]
            self.associations = self.afactory.create_from_assocs(assocs, ontology=sub_ont)
        else:
            self.associations = \
                self.afactory.create(
                        ontology=self.ontology,
                        subject_category='gene',
                        object_category='phenotype',
                        taxon=taxon_map[taxon]
            )

    @staticmethod
    def jaccard_similarity(aset: AssociationSet, s1: str, s2: str) -> float:
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
            return 0.0, set()

        shared_terms = a1.intersection(a2)
        
        return len(shared_terms) / num_union, shared_terms

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
    def trim_mgi_prefix(input_gene, subject_curie):
        if 'MGI:MGI:' in subject_curie and 'MGI:MGI:' in input_gene:
            return input_gene
        elif 'MGI:MGI:' not in subject_curie and 'MGI:MGI:' in input_gene:
            return input_gene[4:]

        else:
            return input_gene

    @staticmethod
    def sort_results(input_gene_set, results):
        results = pd.DataFrame(results)

        # TODO: KCB deprecated until it can be debugged
        """
        print(~results['hit_id'].isin(annotated_gene_set))
        # annotated_gene_set = input_gene_set['hit_id'].tolist()
        # CX: Some users need to know the scores that input genes have for each other. 
        #     replacing code to remove GeneA input = GeneA output results
        results = \
            results[~(results.hit_id==results.input_id)]. \
            sort_values('score', ascending=False)
        """
        return results
