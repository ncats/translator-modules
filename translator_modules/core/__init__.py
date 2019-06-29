from abc import ABC

class Payload(ABC):
    """
    A Payload is a dataclass that carries composites of Biolink Types as a way of constructing its own fields.

    It follows the example set in module0's DiseaseAssociatedGene object as far as its behavior, but its construction
    would be more general.

    If we were to replace DiseaseAssociatedGenes with a Payload, we would want to have something like

    payload = Payload(
        input=Disease().sparse(),
        output=BiolinkType("gene").sparse(),
        slot=Slot("slot name")
    )

    as a construction, and methods like

    payload.get_dataframe().to_json()

    would allow us to get the output in CWL, for instance.

    And during construction there would be runtime tests to assert whether or not the input and output types
    are appropriate for the given slot.

    And if we still use workflows, workflow units take payloads, and would output payloads as a workflow_step.result()

    The advantage of having a Payload is it would be:
    (1) a standard way of accessing the same data under different projections
        (a) ... which would be necessary if we support writing scripts as python modules, which would
                require the objects in some runtime-environment format
        (b) ... or otherwise support using the CWL standard, which we will prefer as JSON (which is a
                de-facto format of the web)
        (c) ... or support data processing the outputs of the workflow which will often be in CSV
    (2) a way of enforcing the inputs and outputs against biolink types by making the required at the point
        of construction of an object (rather than requiring wrappers for further abstraction: this would serve the same
        role, and we could use the CWL spec plus schemas and runners as the sole wrapping layer)
    (3) it would allow for naming conventions to become more consistent with the kind of data being passed around, rather
        than just if it was the input or output of a previous workflow step. If a workflow's domain and range are fully
        determined, why are we asking for `input_id` and `hit_id`? Naming them as e.g. `disease_id` and `gene_id` at least
        gives a hint of what to expect.
        * a counter-argument might lie in the fact that we lose which part of incoming data was input and which was output,
        but this is arguably better as meta-data on the Payload rather than data for it?
        PROBLEMS:
        - The interface would still have to discern input/output types under the current module code

    [ BiolinkType("gene").sparse() would output an object with fields gene_name and gene_id, which would
        be enough to reconstruct the remaining features of the type given a reconciliation against an API
        that would be called based on the datasources implied by the curie. Disease() would inherit from BiolinkType()
    ]

    Going further, could we have a service which is more general than each module, using CURIEs and biolink types
    to access some kind of registry?

    author: kbruskiewicz
    """

    def __init__(self):
        """
        Conventions for Payloads:
        - They expect CSV/TSV files or JSON files in 'record' form (a list of dictionaries that name-index tuples of data)
        - Their internal representation of these datatypes
        - If the internal representation needs to be transformed into something usable by one of its methods, it is the
            responsibility of the method to do the data conversion. For example, if we need to iterate over records, the dictionary
            conversion is done inside the method.
            - This is tenable as a design principle due to the first convention causing us to expect DataFrames by default, but
            we shouldn't know what the method is going to require and do the conversion, **as that leaks out information
            about the method into a higher layer of the code.**

        Accept
        """
        pass

    def get_hits(self):
        pass