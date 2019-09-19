# Gene to Gene Modules

The modules in this package generally take a list of genes (in some cases,  HGNC identifiers; otherwise, Ensembl IDs)
as input, to retrieve a list of related genes. Generally, the output table consists of input gene identifiers
(and gene symbols) matched up with output 'hit' identifiers (and gene symbols),  with a possible score and some 
metric of provenance (e.g. shared identifiers).

## functional_similarity.py

This module retrieves a functionally similar genes as measured by Jaccard similarity of Gene Ontology. To run:

``` 
functional_similarity.py --input-genes "HGNC:1100,HGNC:12829,HGNC:20473,HGNC:20748,HGNC:23168" \
                            get-data-frame to-csv
```

will give a CSV formatted table of associated genes, plus a score, "shared term names" and 
"shared terms" (specified as GO identifiers). Note that, as with all the modules,
other (possibly richer) format outputs are available (and perhaps more informative)

## phenotype_similarity.py

This module retrieves a phenotypically similar genes  as measured by Jaccard similarity of phenotype ontology 
annotation of the genes. To run:

``` 
phenotype_similarity.py --input-genes "HGNC:1100,HGNC:12829,HGNC:20473,HGNC:20748,HGNC:23168" \
                            get-data-frame to-csv
```

will give a CSV formatted table of associated genes, plus a score, "shared term names" and 
"shared terms" (specified as HP ontology identifiers). Note that, as with all the modules,
other (possibly richer) format outputs are available (and perhaps more informative)

## gene_interaction.py

This module retrieves sets of interacting genes from Monarch Biolink. To run:

``` 
gene_interaction.py --input-genes "HGNC:1100,HGNC:12829,HGNC:20473,HGNC:20748,HGNC:23168" \
                     get-data-frame to-csv
```

will give a CSV formatted table of associated genes. Note that, as with all the modules,
other (possibly richer) format outputs are available (and perhaps more informative)

## gene_to_gene_bicluster_RNAseqDB.py

This module retrieves sets of co-occuring genes from RNaseqDB gene expression data biclusters. To run:

``` 

gene_to_gene_bicluster_RNAseqDB.py --input_genes "ENSG00000148584,ENSG00000070018,ENSG00000175899" \
                       get-data-frame to-csv
```

will give a CSV formatted table of associated genes. Note that, as with all the modules,
other (possibly richer) format outputs are available (and perhaps more informative)

## gene_gene_bicluster.py

This module retrieves sets of co-occuring genes from DepMap gene knockout fitness data biclusters. To run:

``` 
gene_to_gene_bicluster_DepMap.py --input_genes "NCBI:214,NCBI:84896,NCBI:55299,NCBI:9184,NCBI:144608" \
                       get-data-frame to-csv
```

will give a CSV formatted table of associated genes. Note that, as with all the modules,
other (possibly richer) format outputs are available (and perhaps more informative)
