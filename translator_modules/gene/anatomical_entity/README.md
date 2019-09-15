# Gene to Anatomical Entity Modules

The modules in this package generally take a list of genes (usually Ensembl identifiers) 
as input, to retrieve a list of anatomical locations within which they are expressed.

## gene_to_tissue_bicluster.py

This module associates genes with tissues within which they are found most commonly
expressed in the available RNASeqDb dataset. To run:

``` 
gene_to_tissue_bicluster.py --input_genes '[ "ENSG00000148584", "ENSG00000070018", "ENSG00000175899"]' \
                            get-data-frame to-csv
```

will give a CSV formatted table of tissues commonly exhibiting expression of the specified genes. 
Note that, as with all the modules, other (possibly richer) format outputs are available (and perhaps more informative)
