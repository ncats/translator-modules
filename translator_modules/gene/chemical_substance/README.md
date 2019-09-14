# Disease to Gene Modules

The modules in this package generally take a list of genes as input, and returns a list
of interacting chemical substances.

## chemical_gene_interaction.py

**NOTE: This module is still under active development**

This module retrieves list, from CTD, of chemicals with which interactions are known with specified genes. To run:

``` 
chemical_gene_interaction.py --input-genes "ENSG00000148584,ENSG00000070018,ENSG00000175899" \
                             get-data-frame to-csv
```

will give a CSV formatted chemical substances interacting with the list of input genes. 
Note that, as with all the modules, other (possibly richer) format outputs are available (and perhaps more informative)
