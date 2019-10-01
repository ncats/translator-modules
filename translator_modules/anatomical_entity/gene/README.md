# Anatomical Entity to Gene Modules

The modules in this package generally take a tissue specification as input, to retrieve a list of related genes.

## tissue_to_gene_bicluster

This module retrieves lists of genes expressed in tissues. To run:

```
tissue_to_gene_bicluster --input-tissues "UBERON:0002107" get-data-frame to-csv
```

will give a CSV formatted table of genes associated with specified tissues. Note that, as with all the modules,
other (possibly richer) format outputs are available (and perhaps more informative)
