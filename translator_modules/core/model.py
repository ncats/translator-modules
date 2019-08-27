"""
Working on an NCATS (Biolink Model) compliant data model and JSON standard...

Partially inspired by the Indigo (Broad) team 'Gene Sharpener" data model for gene lists,
plus a small bit of the ReasonerAPI nomenclature (here expressed in OpenAPI YAML=like notation)

"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Attribute():
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


@dataclass
class Identifier():
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
          id:
            type: string
        required:
          - xmlns
          - id
    """
    xmlns: str
    id: str


@dataclass
class Result():
    """
    # A 'Result' is a single data record about a single entity
    # in a possible list of results discovered by a computation.

      Result:
        type: object
        properties:
          primary_id:
            type: string
            description: >-
              Canonical Id of the result item.
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
        required:
          - result_id
    """
    primary_id: str
    identifiers: List[Identifier] = field(default_factory=list)
    attributes: List[Attribute] = field(default_factory=list)


@dataclass
class ResultList():
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
          input_category:
            type: string
            description: >-
              Biolink Model concept category globally applicable to the module input data type (e.g. 'disease')
          output_category:
            type: string
            description: >-
              Biolink Model concept category globally applicable to the module output data type  (e.g. 'gene')
          relationship:
            type: string
            description: >-
              Biolink Model predicate tagging of the relationship (relating to the "edge label" of a knowledge graph)
          attributes:
            type: array
            items:
              $ref: '#/definitions/Attribute'
            description: Additional information and provenance about the result list.
          results:
            type: array
            items:
              $ref: '#/definitions/Result'
            description: Members of the list of result entries.
        required:
          - list_id
          - source
          - entries
    """
    list_id: str
    source: str = ''
    input_category: str = ''
    output_category: str = ''
    relationship: str = ''
    attributes: List[Attribute] = field(default_factory=list)
    results: List[Result] = field(default_factory=list)
