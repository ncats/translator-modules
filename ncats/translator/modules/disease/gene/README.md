# Disease to Gene Modules

The modules in this package generally take a disease specification (usually something like a MONDO identifier) 
as input, to retrieve a list of related genes.

## disease_associated_genes

This module retrieves a disease associated list of genes from Monarch. To run:

```
disease_associated_genes --disease-id "MONDO:0019391" get-data-frame to-csv
```

will give a CSV formatted table of genes associated with the disease. Note that, as with all the modules,
other (possibly richer) format outputs are available (and perhaps more informative)
