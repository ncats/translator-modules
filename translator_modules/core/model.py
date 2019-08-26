"""
Working on an NCATS (Biolink Model) compliant data model and JSON standard...

Partially inspired by the Indigo (Broad) team 'Gene Sharpener" data model for gene lists,
plus a small bit of the ReasonerAPI nomenclature (here expressed in OpenAPI YAML=like notation)

definitions:
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
      input_output_relationship:
        type: string
        description: >-
          Biolink Model predicate tagging of the relationship
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

class ResultList():

    def __init__(self, list_id, source=''):
        self.list_id = list_id
        self.source = source

class Result():

    def __init__(self, primary_id):
        self.primary_id = primary_id

    def getPrimaryId(self):
        return self.primary_id

    def setIdentifiers(self, identifiers):
        self.identifiers = identifiers

    def getIdentifiers(self):
        return self.identifiers

    def setAttributes(self, attributes):
        self.attributes = attributes

    def getAttributes(self):
        return self.attributes


class Identifier():

    def __init__(self, xmlns, id):
        self.xmlns = xmlns
        self.id = id


class Attribute():

    def __init__(self, name, value, source=''):
        self.name = name
        self.value = value
        self.source = source
