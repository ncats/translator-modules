# Disease to Gene Modules

The modules in this package generally take a disease specification (usually soemthing like a MONDO identifier) 
as input, to retrieve a list of related genes.

## disease_associated_genes.py

This module retrieves a disease associated list of genes from Monarch. To run:

``` 
gene_to_gene_bicluster.py --input_genes "ENSG00000121410,ENSG00000268895,ENSG00000148584" get-result-list to-json       
```

