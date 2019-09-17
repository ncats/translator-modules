# Gene to Cell Line Modules

The modules in this package generally take a list of genes (in some cases,  NCBI Gene IDs)
as input, to retrieve a list of cell lines. Generally, the output table consists of input gene identifiers
(and gene symbols) matched up with output 'hit' identifiers,  with a score.

## gene_to_cell_line_bicluster_DepMap.py

This module retrieves sets of cell_lines clustered by similar gene expression in profiles extracted from DepMap. To run:

``` 
gene_to_cell_line_bicluster_DepMap.py --input-genes "NCBIGene:672" get-data-frame to-csv
```

will give a CSV formatted table of cell lines associated with genes. Note that, as with all the modules,
other (possibly richer) format outputs are available (and perhaps more informative)


