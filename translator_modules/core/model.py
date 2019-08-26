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
      category:
        type: string
        description: >-
          Biolink Model concept category globally applicable to the results (e.g. 'gene')
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
      # Generally as found in the Biolink Model json-ld context file
      # at https://github.com/biolink/biolink-model/blob/master/context.jsonld
      # For example, for genes: NCBIGene, HGNC, ENSEMBL, MIM (actually missing from the context.jsonld?)
      xmlns:
        type: string
      id:
        type: string

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
