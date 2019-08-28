"""
Working on an NCATS (Biolink Model) compliant data model and JSON standard...

Partially inspired by the Indigo (Broad) team 'Gene Sharpener" data model for gene lists,
plus a small bit of the ReasonerAPI nomenclature (here expressed in OpenAPI YAML=like notation)

"""

from dataclasses import dataclass, field, asdict
from typing import List, Tuple

from rdflib import Namespace
from BioLink.model import Association, NamedThing


class BaseModel():
    def to_json(self):
        return str(asdict(self))

@dataclass(frozen=True)
class Attribute(BaseModel):
    """
    # Both 'Result' data objects and their aggregate collections
    # may be documented with additional metadata attributes.
      Attribute:
        type: object
        properties:
          name:
            type: string
          value:
            type: string
          source:
            type: string
        required:
          - name
          - value
    """
    name: str
    value: str
    source: str = ''


@dataclass(frozen=True)
class Identifier(BaseModel):
    """
    # Data objects in a 'Result' may be globally identified by different identifiers asserted by
    # diverse bioinformatics authorities as indexed by their XML Namespace prefix

      Identifier:
        type: object
        properties:
          # The namespaces will be a data type specific list
          # Generally as found in the Biolink Model json-ld context file at
          # https://github.com/biolink/biolink-model/blob/master/context.jsonld
          # For example, for genes: NCBIGene, HGNC, ENSEMBL, MIM (actually missing from the context.jsonld?)
          xmlns:
            type: string
          object_id:
            type: string
        required:
          - xmlns
          - id
    """
    xmlns: Namespace
    object_id: str

    def __post_init__(self):
        if not isinstance(self.xmlns, Namespace):
            raise RuntimeError("Identifier.xmlns must be specified as an instance of rdflib.Namespace!")

    def curie(self):
        return self.xmlns+":"+self.object_id

    @classmethod
    def parse(cls, curie):
        xmlns, object_id = curie.split(':', 1)
        if object_id is None:
            raise RuntimeError("String '"+curie+"' is not a CURIE?")
        return Identifier(xmlns, object_id)


@dataclass(frozen=True)
class Concept(BaseModel):
    """
    # A 'Concept' is a single data record about a single conceptual entity
    # which could be found in the input and/or output of a Result within a ResultList
    Concept:
        type: object
        properties:
          primary_id:
            type: $ref: '#/definitions/Identifier'
            description: >-
              Canonical Id of the Concept
              For example, for genes, preferably HGNC id; can be NCBIGene or ENSEMBL id if HGNC id is not available.
          identifiers:
            type: array
            items:
              $ref: '#/definitions/Identifier'
            description: >-
              A standard list of equivalent identifiers for a given result (see below)
          attributes:
            type: array
            items:
              $ref: '#/definitions/Attribute'
            description: >-
              Additional information about the gene and provenance about result membership, possibly including various
              scores associated with a given result.
              For example, for genes, maybe use myGene.info to add the following attributes to every gene: 'gene_symbol',
              'synonyms', 'gene_name',  and 'myGene.info id'. Multiple synonyms are separated by semicolons.
    """
    primary_id: Identifier
    identifiers: List[Identifier] = field(default_factory=list)
    attributes: List[Attribute] = field(default_factory=list)

@dataclass(frozen=True)
class Result(BaseModel):
    """
    # A 'Result' is a single data record about a single entity
    # in a possible list of results discovered by a computation.

      Result:
        type: object
        properties:
          input_id:
            type: string
            description: >-
              Canonical CURIE identifier of a given result item input ("query") concept.
              For example, for genes, preferably from HGNC but can be from NCBIGene or ENSEMBL if HGNC ID not available.
          output_id:
            type: string
            description: >-
              Canonical CURIE identifier of a given result item output ("hit") concept.
              For example, for genes, preferably from HGNC but can be from NCBIGene or ENSEMBL if HGNC ID not available.
          score:
            type: string
            description: >-
              The computational generation of each result may (optionally) be associated with a score, which is
              managed as a string variable. If the string is empty, then it is assumed that no score is available.
          attributes:
            type: array
            items:
              $ref: '#/definitions/Attribute'
            description: >-
              Additional information about the provenance of the result membership.
        required:
          - input_id
          - output_id
          - score
    """
    input_id:  str   # should be a CURIE
    output_id: str   # should be a CURIE
    score: str = ''
    attributes: List[Attribute] = field(default_factory=list)


@dataclass(frozen=True)
class ResultList(BaseModel):
    """
    # A 'ResultList' is a (possibly ordered) documented collection of
    # 'Result' data objects returned by a computation.
    #
    # Such a list of results is documented with mandatory metadata (e.g. Biolink Model
    # characterization of the data types returned, and their inferred relationships to input data)
    # and possibly with optional attributes documenting provenance and global characteristics of the results.

      ResultList:
        type: object
        properties:
          list_id:
            type: string
            description: Id of the list of results. Generally an anonymous, globally unique UUID
          source:
            type: string
            description: Module that produced the result list.
          attributes:
            type: array
            items:
                $ref: '#/definitions/Attribute'
            description: Additional global information and provenance about the result list.
          domain:
            category:
                type: string
                description: >-
                    Biolink Model concept category applicable to the module input 'domain' data type (e.g. 'disease')
            namespace:
                type: string
                description: >-
                    Namespace of identifiers for input data, following the Biolink Model context catalog
                    documented at https://github.com/biolink/biolink-model/blob/master/context.jsonld
          relationship:
                type: string
                description: >-
                    Biolink Model predicate mapping of the relationship (relating to "edge label" of a knowledge graph)
          range:
            category:
                type: string
                description: >-
                    Biolink Model concept category applicable to the module output 'range' data type  (e.g. 'gene')
            namespace:
                type: string
                description: >-
                    Namespace of identifiers for output data, following the Biolink Model context catalog
                    documented at https://github.com/biolink/biolink-model/blob/master/context.jsonld
          results:
            type: array
            items:
                $ref: '#/definitions/Result'
            description: Members of the list of result entries.
        required:
          - list_id
          - source
          - domain
          - relationship
          - range
          - concepts
          - results
    """
    list_id: str
    source:  str = ''
    attributes: List[Attribute] = field(default_factory=list)
    domain: Tuple[str] = (NamedThing.class_name, 'SEMMEDDB')
    relationship:  str = Association.class_name
    range:  Tuple[str] = (NamedThing.class_name, 'SEMMEDDB')
    concepts: List[Concept] = field(default_factory=list)
    results:  List[Result] = field(default_factory=list)
