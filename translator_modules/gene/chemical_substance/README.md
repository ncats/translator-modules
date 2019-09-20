# Chemical Substance to Gene Modules

The modules in this package generally take a list of chemical substance identifiers as input, and returns a list
of gene with which such chemicals have an interaction.

## chemical_to_gene_interaction

This module retrieves list, from CTD, of genes with which interactions are known with specified chemicals. To run:

```
chemical_to_gene_interaction --input-chemicals "D000082,D006632" get-data-frame to-csv
```

will give a CSV formatted gene hits interacting with the list of input chemicals 
(in this case, acetaminophen and histamine, in human beings)

THe identifiers which this module accepts may be inferred from [the CTD data dictionary here](http://ctdbase.org/downloads/).

Note that, as with all the modules, other (possibly richer) format outputs are available (and perhaps more informative)
