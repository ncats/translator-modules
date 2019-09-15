"""
Working on an NCATS (Biolink Model) compliant data model and JSON standard...

Partially inspired by the Indigo (Broad) team 'Gene Sharpener" data model for gene lists,
plus a small bit of the ReasonerAPI nomenclature (here expressed in OpenAPI YAML=like notation)

"""
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, List, ClassVar

import pandas as pd
from json.encoder import JSONEncoder

from BioLink.model import Association, NamedThing

# Also serves as the default "ResultList.version" tag
__version__ = '0.0.2'


class ResultListJSONEncoder(JSONEncoder):

    # Need to override the JSONEncoder.default() to handle 'set'
    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)

        if issubclass(o, NamedThing) or issubclass(o, Association):
            return o.class_name

        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, o)


@dataclass(frozen=True)
class BaseModel:

    def to_json(self) -> str:
        """
        Given an instance of data_transfer_model class, dumps a JSON representation as a String
        :
        return: String representation of the model
        """
        result_obj = asdict(self)
        return json.dumps(result_obj, cls=ResultListJSONEncoder)


@dataclass(frozen=True)
class ConceptSpace(BaseModel):
    """
    A ConceptSpace tracks namespace id_prefixes (xmlns prefixes) and associated concept category of
    about a given set of Concept identifiers and types
    """
    category: Any  # but should be Biolink Model registered concept 'category' inheriting from NamedType

    # list of xmlns prefixes drawn from Biolink Model context.jsonld
    id_prefixes: List[str] = field(default_factory=list)

    def __post_init__(self):
        # Can the id_prefixes and category values be validated here against the Biolink Model?
        if not issubclass(self.category, NamedThing):
            raise TypeError("ConceptSpace() type error: category '" + str(self.category) +
                            "' must be a subclass of the BioLink.NamedThing")

@dataclass(frozen=True)
class ModuleMetaData:
    """
     # ModuleMetaData is meant to wrap the module self.meta
     # This is an example from the FunctionalSimilarity module

     # We're going to ignore the 'complexity' argument for now

     self.meta = {
        'source': 'Monarch Biolink',
        'association': FunctionalAssociation,
        'input_type': {
            'complexity': 'set',
            'category': Gene,
            'id_prefixes': 'HGNC',
        },
        'relationship': 'related_to',
        'output_type': {
            'complexity': 'set',
            'category': Gene,
            'id_prefixes': 'HGNC',
        },
    }
    """
    name: str  # name of the module
    source: str  # knowledge source authority of the module
    association: Any  # but should be BioLink Model class inheriting from Association
    domain: ConceptSpace  # Input domain - category, id_prefixes - of the input data to the module
    relationship: str  # BioLink Model minimal predicate defined the relationship of inputs to output
    range: ConceptSpace  # Output Range - category, id_prefixes - of the results of the module


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


def timestamp():
    # current date and time.
    now = datetime.now()
    ts = datetime.timestamp(now)
    return str(datetime.fromtimestamp(ts))


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
                The xmlns will be a data type specific list of namespaces
                Generally as found in the Biolink Model json-ld context file at
                https://github.com/biolink/biolink-model/blob/master/context.jsonld
                For example, for genes: NCBIGene, HGNC, ENSEMBL, MIM (actually missing from the context.jsonld?)
          object_id:
            type: string
          name:
            type: string
            description: longer human readable name of a given conceptual entity
          symbol:
            type: string
            description: (optional) symbol representing a given conceptual entity, e.g. gene symbol
          version:
            type: string
            description: (optional) identifier version string
        required:
          - xmlns
          - id
    """
    xmlns: str
    object_id: str
    name: str = ''
    symbol: str = ''
    version: str = ''
    timestamp: str = timestamp()

    # We might validate the xmlns against registered ones in the future.
    # Enforcing use of the rdfLib.Namespace is deprecated for now

    # def __post_init__(self):
    #    if not isinstance(self.xmlns, Namespace):
    #        raise RuntimeError("Identifier.xmlns must be specified as an instance of rdflib.Namespace!")

    def curie(self) -> str:
        curie = self.xmlns + ":" + self.object_id
        if self.version:
            curie = curie + "." + self.version
        return curie

    @classmethod  # returns an instance of Identifier constructed from a CURIE
    def parse(cls, curie, name='', symbol='', version=''):
        part = curie.split(':', 1)
        if len(part) < 2:
            raise RuntimeError("String '" + curie + "' is not a CURIE?")
        xmlns = part[0]
        identifier = part[1].split('.', 1)  # split out optional 'dot' delimited version number
        object_id = identifier[0]
        if len(identifier) == 2:
            version = identifier[1]

        return Identifier(xmlns, object_id, name=name, symbol=symbol, version=version)


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

    def __post_init__(self):
        """
        Here we'll add 'value added' identifier resolution
        :return:
        """

        pass


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
    input_id: str  # should be a CURIE
    output_id: str  # should be a CURIE
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
          result_list_name:
            type: string
            description: Human readable name of the result list.
          source:
            type: string
            description: Module that produced the result list.
          identifiers:
            type: array
            items:
                $ref: '#/definitions/Identifier'
            description: identifiers associated with a ResultList; identifiers[0] is the primary one
          association:
                type: string
                description: >-
                    Biolink Model association ("association type" of a knowledge graph)
          domain:
            type: '#/definitions/ConceptSpace'
            description: >-
                Namespace and Category of identifiers for input data, following the Biolink Model context catalog
                documented at https://github.com/biolink/biolink-model/blob/master/context.jsonld
          relationship:
                type: string
                description: >-
                    Biolink Model predicate of the relationship type ("edge label" of a knowledge graph)
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
          attributes:
            type: array
            items:
                $ref: '#/definitions/Attribute'
            description: Additional global information and provenance about the Result List.
        required:
          - identifiers # at least, identifiers[0] == canonical
          - source
          - association
          - domain
          - relationship
          - range
          - concepts
          - results
    """
    result_list_name: str = None
    result_list_version: str = __version__
    module_name: str = ''
    source: str = ''
    association: str = str(Association)
    domain: ConceptSpace = ConceptSpace(category=NamedThing, id_prefixes=['SEMMEDDB'])
    relationship: str = "related_to"  # should correspond with a Biolink Model minimal predicate ("relationship type")
    range: ConceptSpace = ConceptSpace(category=NamedThing, id_prefixes=['SEMMEDDB'])
    identifiers: List[Identifier] = field(default_factory=list)
    attributes: List[Attribute] = field(default_factory=list)
    concepts: List[Concept] = field(default_factory=list)
    results: List[Result] = field(default_factory=list)

    list_number: ClassVar[List[int]] = [0]

    def size(self) -> int:
        return self.results.count()

    def __post_init__(self):

        # identifiers is an empty array upon initialization, so
        # identifiers[0] is set to a constructed canonical identifier
        self.list_number[0] += 1  # maybe a UUID later?
        object_id = str(self.list_number[0])
        self.identifiers.append(
            Identifier(
                xmlns='NCATS',
                object_id=object_id,
                name=self.result_list_name if self.result_list_name else 'ResultList ' + object_id
            )
        )

        # Not sure how essential to do this validation here since the dataclass has typed its attributes?
        if self.domain is None or not isinstance(self.domain, ConceptSpace):
            raise RuntimeError("Value of Domain '" +
                               str(self.domain) + "' of Result List '" + self.identifiers[0].curie() +
                               "' is uninitialized or not a ConceptSpace")
        if self.range is None or not isinstance(self.range, ConceptSpace):
            raise RuntimeError("Range '" +
                               str(self.range) + "' of Result List '" + self.identifiers[0].curie() +
                               "' is uninitialized or not a ConceptSpace")

    @classmethod
    def load(cls, result_list_obj: dict):
        """
        Loads a JSON String representation of ResultList into a new ResultList instance

        :param result_list_json: the input JSON String
        :return: returns a new ResultList instance

        rl = ResultList(
            result_list_name='Stub Resultlist',
            source='ncats',
            association=str(Association),
            domain=ConceptSpace(category=NamedThing, id_prefixes=['SEMMEDDB']),
            relationship='related_to',
            range=ConceptSpace(category=NamedThing, id_prefixes=['SEMMEDDB']),
        )
        rl.concepts.extend(Concept,...)
        rl.results.extend(Result,...)
        rl.attributes.extend(Attributes...)
        """

        def parse_attribute(a_obj):
            return Attribute(
                name=a_obj['name'],
                value=a_obj['value'],
                source=a_obj['source']
            )

        def parse_concept_space(cs_obj):
            return ConceptSpace(
                id_prefixes=cs_obj['id_prefixes'],
                category=cs_obj['category'],
            )

        # Load the resulting Python object into a ResultList instance
        rl = ResultList(
            result_list_name=result_list_obj['result_list_name'],
            result_list_version=result_list_obj['result_list_version'],
            source=result_list_obj['source'],
            domain=parse_concept_space(result_list_obj['domain']),
            association=result_list_obj['association'],
            relationship=result_list_obj['relationship'],
            range=parse_concept_space(result_list_obj['range'])
        )

        def parse_identifier(i_obj):
            return Identifier(
                xmlns=i_obj['xmlns'],
                object_id=i_obj['object_id'],
                name=i_obj['name'],
                symbol=i_obj['symbol'],
                version=i_obj['version'],
                timestamp=i_obj['timestamp']
            )

        rl.identifiers.extend([parse_identifier(i_obj) for i_obj in result_list_obj['identifiers']])

        def parse_concept(c_obj):
            c = Concept(
                primary_id=parse_identifier(c_obj['primary_id'])
            )
            c.identifiers.extend([parse_identifier(i_obj) for i_obj in c_obj['identifiers']])
            c.attributes.extend([parse_attribute(a_obj) for a_obj in c_obj['attributes']])
            return c

        rl.concepts.extend([parse_concept(c_obj) for c_obj in result_list_obj['concepts']])

        def parse_result(r_obj):
            r = Result(
                input_id=r_obj['input_id'],
                output_id=r_obj['output_id'],
                score=r_obj['score'],
            )
            r.attributes.extend([parse_attribute(a_obj) for a_obj in r_obj['attributes']])
            return r

        rl.results.extend([parse_result(r_obj) for r_obj in result_list_obj['results']])

        rl.attributes.extend([parse_attribute(a_obj) for a_obj in result_list_obj['attributes']])

        return rl

    @classmethod
    def import_data_frame(cls, data_frame: pd.DataFrame, metadata: ModuleMetaData):
        """
        Convert standard Pandas DataFrame "results" into Results of an NCATS ResultList instance.

        For now (first iteration), we assume a static mapping of Workflow 2 style of DataFrame columns
        into a list of Results, combined with Payload metadata provided alongside.

        :param data_frame: a Pandas DataFrame with results
        :param metadata:
        :return: ResultList data instance
        """

        module_domain = metadata.domain
        module_range = metadata.range

        # Load the resulting Python object into a ResultList instance
        result_list_name = \
            metadata.source + ' ' + \
            str(module_domain.category) + ' ' + \
            metadata.relationship.replace('_', ' ') + ' ' + \
            str(module_range.category)

        rl = ResultList(
            result_list_name=result_list_name,
            module_name=metadata.name,
            source=metadata.source,
            association=metadata.association,
            domain=module_domain,
            relationship=metadata.relationship,
            range=module_range
        )

        if data_frame.empty:
            return rl  # sends back an empty ResultList

        # Convert all the records from the DataFrame into ResultList recorded data
        concepts = {}

        def add_concept(concept_id):
            concept_curie = concept_id.curie()
            if concept_curie not in concepts:
                concepts[concept_curie] = concept_id

        for entry in data_frame.to_dict(orient='records'):

            # Initial iteration: assume a simple Pandas DataFrame with columns
            # 'input_id', 'input_symbol', 'hit_id', 'hit_symbol', 'score'

            if entry['hit_id'] == 'NONE':
                # null entry, for some reason? not meaningful? Ignore?
                continue

            # Second iteration: , i.e. biclustering?
            input_id_list = []
            if 'input_id' in entry:
                # maybe only one identifier but accommodates multiple hits as well
                input_id_list.extend(entry['input_id'].split(','))

            # assume that input_symbol id_prefixes may be missing
            # in the output of some algorithms; record a blank input_id
            if not len(input_id_list):
                input_id_list.append('')  # provision for empty identifier

            output_id_list = []
            if 'hit_id' in entry:
                # maybe only one identifier but accommodates multiple hits as well
                output_id_list.extend(entry['hit_id'].split(','))

            score = entry.get('score', '.')

            # Build join of inputs and hits
            for input_id in input_id_list:
                input_id_obj = Identifier.parse(
                    input_id,
                    symbol=entry['input_symbol'] if 'input_symbol' in entry else ''
                )
                add_concept(input_id_obj)

                for output_id in output_id_list:
                    output_id_obj = Identifier.parse(
                        output_id,
                        symbol=entry['hit_symbol'] if 'hit_symbol' in entry else ''
                    )
                    add_concept(output_id_obj)

                    # ... then append the results to the results list
                    # Hmm... note that input_id may be unmapped or
                    # multiply mapped in some situations
                    r = Result(
                        input_id_obj.curie() if input_id_obj else '',
                        output_id_obj.curie(),
                        score
                    )
                    rl.results.append(r)

            # Collect other fields as attributes
            for (key, value) in entry.items():

                # Ignore core data columns...
                if key in ['input_id', 'input_symbol', 'hit_id', 'hit_symbol', 'score']:
                    continue

                # ...capture the rest as attributes for a given Result
                r.attributes.append(Attribute(key, value))

        # compile the list of Concepts seen
        for curie in concepts.keys():
            rl.concepts.append(Concept(concepts[curie]))

        return rl

    def export_data_frame(self) -> pd.DataFrame:
        """
        Convert this ResultList into a Pandas DataFrame
        :return: a Python Pandas DataFrame representation of (most of) the data in a given ResultList
        """
        curie_map = {}
        for concept in self.concepts:
            curie_map[concept.primary_id.curie()] = concept

        input_ids = []
        input_symbols = []
        hit_ids = []
        hit_symbols = []
        scores = []

        def _map_ids(id, curies, symbols):
            if id in curie_map:
                c = curie_map[id]
                cid = c.primary_id
                curies.append(cid.curie())
                symbols.append(cid.symbol)
            else:
                curies.append('')
                symbols.append('')

        for result in self.results:
            _map_ids(result.input_id, input_ids, input_symbols)
            _map_ids(result.output_id, hit_ids, hit_symbols)
            scores.append(result.score)

        # First iteration doesn't consider Result.attributes.. how can we load these?
        entries = {
            "input_id": input_ids,
            "input_symbol": input_symbols,
            "hit_id": hit_ids,
            "hit_symbol": hit_symbols,
            "score": scores
        }

        df = pd.DataFrame(data=entries)

        return df
