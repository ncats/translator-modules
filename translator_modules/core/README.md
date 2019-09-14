# Module Payloads

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

# Identifier Resolution Module v0.2.0

## From the command-line:
```bash
 translator_modules/core/identifiers.py \
--identifier-map ./HUGO_geneids_download_v2.txt --source "Ensembl Gene ID" --target "HGNC ID" \
load-identifiers --identifiers ../../tests/data/bicluster/csv/gene_list.csv \
translate
```

Note: when being given `--identifiers`, it looks for a column equivalent to the name of the ID namespace 
(like "Ensembl Gene ID" or "HGNC ID").

Inputting a list of IDs instead of a CSV file path should also work.

```bash
 translator_modules/core/identifiers.py \
--identifier-map ./HUGO_geneids_download_v2.txt --source "Ensembl Gene ID" --target "HGNC ID" \
load-identifiers --identifiers \
'["ENSG00000121410", "ENSG00000268895", "ENSG00000148584", "ENSG00000070018", "ENSG00000175899", "ENSG00000245105"]'  \
translate
```

Note: it's important for there to be quotes around the list if your list contains strings (`'["like this"]'`, or `"['like that']"`). Else the list gets handled as if it was one marked up string instead: that's what Bash wants over Python.

Speaking of which. 

## In Python 3:

```python
from translator_modules.core.identifiers import Resolver

ids = ["ENSG00000121410", "ENSG00000268895", "ENSG00000148584", "ENSG00000070018", "ENSG00000175899", "ENSG00000245105"]
    
identifier_map = "absolute/path/to/HUGO_geneids_download_v2.csv"
resolver = Resolver(identifier_map, source="Ensembl", target="HGNC")
converted_ids = resolver.translate(input_ids=ids)

print(converted_ids)
```

In either case, you should get something like this:

```
["ENSG00000121410", ""]
["ENSG00000268895", "HGNC:37133"]
["ENSG00000148584", "HGNC:24086"]
["ENSG00000070018", "HGNC:6698"]
["ENSG00000175899", "HGNC:7"]
["ENSG00000245105", "HGNC:27057"]
["ENSG00000166535", "HGNC:23336"]
["ENSG00000256661", "HGNC:41022"]
["ENSG00000256904", "HGNC:41523"]
["ENSG00000256069", "HGNC:8"]
["ENSG00000234906", "HGNC:609"]
["ENSG00000068305", "HGNC:6993"]
["ENSG00000070018", "HGNC:6698"]
```

Which you can now manipulate in other programs.
