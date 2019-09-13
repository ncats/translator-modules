## ID Translation Module v0.2.0

### From the command-line:
```bash
 translator_modules.core.identifier.py \
--identifier-map `readlink -f ./HUGO_geneids_download_v2.txt` --source "Ensembl" --target "HGNC" \
load-identifiers --identifiers `readlink -f ../../../test/data/bicluster/csv/gene_list.csv`  \
translate
```

Note: when being given `--identifiers`, it looks for a column equivalent to the name of the ID namespace 
(like "Ensembl" or "HGNC"). If you think there's a better alternative, open an issue and we'll figure it out.

(All `readlink -f` does is let you point to relative paths and resolve them as absolute ones. Note that on Mac OSX,
you need to ```brew install coreutils``` then  use *greadlink* instead of *readlink*)

Inputting a list of IDs instead of a CSV file path should also work.

```bash
 translator_modules.core.identifier.py \
--identifier-map `readlink -f ./HUGO_geneids_download_v2.txt` --source "Ensembl" --target "HGNC" \
load-identifiers --identifiers \
'["ENSG00000121410", "ENSG00000268895", "ENSG00000148584", "ENSG00000070018", "ENSG00000175899", "ENSG00000245105"]'  \
translate
```

Note: it's important for there to be quotes around the list if your list contains strings (`'["like this"]'`, or `"['like that']"`). Else the list gets handled as if it was one marked up string instead: that's what Bash wants over Python.

Speaking of which. 

### In Python 3:
```python
from translator_modules.core.identifier import Resolver

ids = ["ENSG00000121410", "ENSG00000268895", "ENSG00000148584", "ENSG00000070018", "ENSG00000175899", "ENSG00000245105"]
    
identifier_map = "absolute/path/to/HUGO_geneids_download_v2.csv"
resolver = Resolver(identifier_map, source="Ensembl", target="HGNC")
converted_ids = resolver.translate(input_ids=ids)

print(converted_ids)
```

In either case, you should get something like this:

```
["ENSG00000121410", "HGNC:5"]
["ENSG00000268895", null]
["ENSG00000148584", null]
["ENSG00000070018", "HGNC:6698"]
["ENSG00000175899", null]
["ENSG00000245105", "HGNC:27057"]
["ENSG00000166535", null]
["ENSG00000256661", "HGNC:41022"]
["ENSG00000256904", "HGNC:41523"]
["ENSG00000256069", "HGNC:8"]
["ENSG00000234906", "HGNC:609"]
["ENSG00000068305", null]
["ENSG00000070018", "HGNC:6698"]
```

Which you can now manipulate in other programs.
