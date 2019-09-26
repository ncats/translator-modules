# Disease to Phenotypic Feature Modules

The modules in this package generally take a disease specification (usually something like a MONDO identifier) 
as input, to retrieve a list of related genes.

## disease_to_phenotype_bicluster

**NOTE: This module is under active development**

This module retrieves a disease associated list phenotypes coupled in expression data. To run:

```
disease_to_phenotype_bicluster --input-diseases "MONDO:0007030" get-data-frame to-csv
```

will give a CSV formatted table of phenotypes associated with the disease. Note that, as with all the modules,
other (possibly richer) format outputs are available (and perhaps more informative)
