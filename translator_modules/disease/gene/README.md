# Disease to Gene Modules

The modules in this package generally take a disease specification (usually soemthing like a MONDO identifier) 
as input, to retrieve a list of related genes.

## disease_associated_genes.py

This module retrieves a disease associated list of genes from Monarch. To run:

``` 
disease_associated_genes.py --disease-id "MONDO:0019391" get-data-frame to-csv
```

will give a CSV formatted table of genes associated with the disease. Note that, as with all the nmodules,
other (possibly richer) format outputs are available (and perhaps more informative)
