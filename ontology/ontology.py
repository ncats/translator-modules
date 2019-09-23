# Shared core similarity functions
from typing import List, Tuple

import pandas as pd
from ontobio.assoc_factory import AssociationSetFactory
from ontobio.assocmodel import AssociationSet
from ontobio.io.gafparser import GafParser
from ontobio.ontol_factory import OntologyFactory

# We override the Ontobio version of the jaccard_similarity
# function below, to return shared ontology term annotation
#
# from ontobio.analysis.semsim import jaccard_similarity


class Ontology(object):

    def __init__(self) -> None:
        self.associations = None
        self.ont = ''
        self.ontology = ''
        self.assocs = ''
        self.afactory = AssociationSetFactory()

    def load_associations(self, taxon) -> None:
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
