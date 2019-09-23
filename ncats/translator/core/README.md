# Identifier Resolution Module v0.2.0

## Configuration

From within the project root directory, you need to configure the environment:

```  
python -m pip install .
```

## From the command-line:
```bash
resolver --identifier-map "absolute_or_relative/path/to/HUGO_geneids_download_v2.txt" \
--source "Ensembl Gene ID" --target "HGNC ID" \
load-identifiers --identifiers ../../tests/data/bicluster/csv/gene_list.csv   translate
```

Note: when being given `--identifiers`, it looks for a column equivalent to the name of the ID namespace 
(like "Ensembl Gene ID" or "HGNC ID").

Inputting a list of IDs instead of a CSV file path should also work.

```bash
resolver --identifier-map "absolute_or_relative/path/to/HUGO_geneids_download_v2.txt" \
--source "Ensembl Gene ID" --target "HGNC ID" \
load-identifiers --identifiers \
"ENSG00000121410,ENSG00000268895,ENSG00000148584,ENSG00000070018,ENSG00000175899,ENSG00000245105" translate
```

## Calling Identifier Resolution from Python Code

```python
from ncats.translator.identifiers.client.resolver import Resolver

ids = ["ENSG00000121410", "ENSG00000268895", "ENSG00000148584", "ENSG00000070018", "ENSG00000175899", "ENSG00000245105"]
    
identifier_map = "absolute/path/to/HUGO_geneids_download_v2.txt"
resolver = Resolver(identifier_map, domain="Ensembl", range="HGNC")
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
