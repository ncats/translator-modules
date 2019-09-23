# Gene to Chemical Substance Modules

The modules in this package generally take a list of genes as input, and returns a list
of interacting chemical substances.

## gene_to_chemical_interaction

This module retrieves list, from CTD, of chemicals with which interactions are known with specified genes. To run:

```
gene_to_chemical_interaction --input-genes "NCBIGene:4149,NCBIGene:4609,NCBIGene:3785" get-data-frame to-csv
```

will give a CSV formatted chemical substances interacting with the list of input genes.

Note that, as with all the modules, other (possibly richer) format outputs are available (and perhaps more informative)

