"""
Working on an NCATS (Biolink Model) compliant data model and JSON standard...

Partially inspired by the Indigo (Broad) team 'Gene Sharpener" data model for gene lists,
plus a small bit of the ReasonerAPI nomenclature (here expressed in OpenAPI YAML=like notation)

"""
import json
import pandas as pd

from dataclasses import dataclass, field, asdict
from typing import List

from BioLink.model import Association, NamedThing

__version__ = '0.0.1'


@dataclass(frozen=True)
class BaseModel():

    def to_json(self) -> str:
        """
        Given an instance of data_transfer_model class, dumps a JSON representation as a String
        :
        return: String representation of the model
        """
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
          xmlns:
            type: string
            description: >-
                The namespaces will be a data type specific list of namespaces
                Generally as found in the Biolink Model json-ld context file at
                https://github.com/biolink/biolink-model/blob/master/context.jsonld
                For example, for genes: NCBIGene, HGNC, ENSEMBL, MIM (actually missing from the context.jsonld?)
          object_id:
            type: string
        required:
          - xmlns
          - id
    """
    xmlns: str  # generally should be a namespace prefix as found in the Biolink Model context.jsonld file
    object_id: str

    # We might validate the xmlns against registered ones in the future.
    # Enforcing use of the rdfLib.Namespace is deprecated for now

    # def __post_init__(self):
    #    if not isinstance(self.xmlns, Namespace):
    #        raise RuntimeError("Identifier.xmlns must be specified as an instance of rdflib.Namespace!")

    def curie(self) -> str:
        return self.xmlns+":"+self.object_id

    @classmethod # returns an instance of Identifier constructed from a CURIE
    def parse(cls, curie):
        part = curie.split(':', 1)
        if len(part) < 2 :
            raise RuntimeError("String '"+curie+"' is not a CURIE?")
        xmlns = part[0]
        object_id = part[1]
        return Identifier(xmlns, object_id)


@dataclass(frozen=True)
class ConceptSpace(BaseModel):
    """
    A ConceptSpace tracks metadata about a class of Concept identifiers and types
    """
    namespace: str  # should be Biolink Model registered identifier namespace
    category: str   # should be Biolink Model registered category

    def __post_init__(self):
        # Can the namespace and category be validated here as Biolink Model compliant?
        pass

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
    attributes:  List[Attribute]  = field(default_factory=list)


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
            type: '#/definitions/ConceptSpace'
            description: >-
                Namespace and Category of identifiers for input data, following the Biolink Model context catalog
                documented at https://github.com/biolink/biolink-model/blob/master/context.jsonld
          relationship:
                type: string
                description: >-
                    Biolink Model predicate mapping of the relationship (relating to "edge label" of a knowledge graph)
          range:
            type: '#/definitions/ConceptSpace'
            description: >-
                Namespace and Category of identifiers for output data, following the Biolink Model context catalog
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
    domain: ConceptSpace = ConceptSpace('SEMMEDDB', NamedThing.class_name)
    relationship:  str = Association.class_name
    range:  ConceptSpace = ConceptSpace('SEMMEDDB', NamedThing.class_name)
    concepts: List[Concept] = field(default_factory=list)
    results:  List[Result]  = field(default_factory=list)

    def __post_init__(self):
        if self.domain is None or not isinstance(self.domain, ConceptSpace):
            raise RuntimeError("Value of Domain '" +
                               str(self.domain) + "' of Result List '" + self.list_id +
                               "' is uninitialized or not a ConceptSpace")
        if self.range is None or not isinstance(self.range, ConceptSpace):
            raise RuntimeError("Range '" +
                               str(self.range) + "' of Result List '" + self.list_id +
                               "' is uninitialized or not a ConceptSpace")

    @classmethod
    def load(cls, result_list_json: str):
        """
        Loads a JSON String representation of ResultList into a new ResultList instance

        :param result_list_json: the input JSON String
        :return: returns a new ResultList instance

        rl = ResultList(
            'Stub Resultlist',
            source='ncats',
            domain=ConceptSpace('SEMMEDDB', NamedThing.class_name),
            relationship=Association.class_name,
            range=ConceptSpace('SEMMEDDB', NamedThing.class_name)
        )
        rl.attributes.append(Attributes...)
        rl.concepts.append(Concepts...)
        rl.results.append(Results...)

        """
        python_obj = json.loads(result_list_json)

        return ResultList('ResultList.load(): Stub ResultList')

    @classmethod
    def import_data_frame(cls, data_frame: pd.DataFrame):
        """
        Convert a Pandas DataFrame into a ResultList
        :param data_frame: a Pandas DataFrame with results
        :return: ResultList data instance

        rl = ResultList(
            'Stub Resultlist',
            source='ncats',
            domain=ConceptSpace('SEMMEDDB', NamedThing.class_name),
            relationship=Association.class_name,
            range=ConceptSpace('SEMMEDDB', NamedThing.class_name)
        )
        rl.attributes.append(Attributes...)
        rl.concepts.append(Concepts...)
        rl.results.append(Results...)

        """
        return ResultList('ResultList.import_data_frame(): Stub ResultList')

    def export_data_frame(self) -> pd.DataFrame:
        """
        Convert this ResultList into a Pandas DataFrame
        :return: a Python Pandas DataFrame representation of (most of) the data in a given ResultList
        """
        return pd.DataFrame()
