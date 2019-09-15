# Phenotypic Feature to Disease Modules

The modules in this package generally take a list of phenotypic features to match against diseases.

## disease_to_phenotype_bicluster.py

This module retrieves a disease associated phenotypes identified in expression data To run:

``` 
disease_to_phenotype_bicluster.py --input-diseases "MONDO:0019391" get-data-frame to-csv
```

will give a CSV formatted table of phenotypic features associated with the disease. Note that, 
as with all the modules, other (possibly richer) format outputs are available (and perhaps more informative)
