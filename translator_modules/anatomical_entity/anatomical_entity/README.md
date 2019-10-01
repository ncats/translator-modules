# Anatomical Entity to Anatomical Entity Association Modules

The modules in this package identify tissue to tissue correlations from expression data.

## tissue_to_tissue_bicluster

**NOTE: This module is under active development**

This module retrieves gene expression correlations between tissues. To run:

```
tissue_to_tissue_bicluster --input-tissues "UBERON:0001157" get-data-frame to-csv
```

will give a CSV formatted table of associated tissues. Note that, as with all the modules,
other (possibly richer) format outputs are available (and perhaps more informative)
