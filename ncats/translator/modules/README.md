# Translator Modules

The Translator Modules are partitioned into packages indexed by their input and output Biolink Model concept categories.
For example, the **disease_associated_genes.py** module is found under the *ncats.translator.modules.disease.gene* 
package [here](https://github.com/ncats/translator-modules/blob/master/ncats/translator/modules/disease/gene)

Additional documentation for the various scripts will generally be found within each package containing the scripts,
for example, 
[here](https://github.com/ncats/translator-modules/blob/master/ncats/translator/modules/disease/gene/README.md)

Here is a summary table of the current inventory of Biolink data type categories processed with their associated modules

| Input Category | Output Category | Module(s) |
| --- | --- | --- |
| anatomical entity | [anatomical entity](https://github.com/ncats/translator-modules/blob/master/ncats/translator/modules/anatomical_entity/anatomical_entity/README.md) | tissue_to_tissue_bicluster |
|   | [gene](https://github.com/ncats/translator-modules/blob/master/ncats/translator/modules/anatomical_entity/gene/README.md)| tissue_to_gene_bicluster |
| chemical substance | [gene](https://github.com/ncats/translator-modules/blob/master/ncats/translator/modules/chemical_substance/gene/README.md)| chemical_to_gene_interaction |
| disease | [gene](https://github.com/ncats/translator-modules/blob/master/ncats/translator/modules/disease/gene/README.md)| disease_associated_genes |
|  | [phenotypic feature](https://github.com/ncats/translator-modules/blob/master/ncats/translator/modules/disease/phenotypic_feature/README.md)| disease_to_phenotype_bicluster |
| gene | [anatomical entity](https://github.com/ncats/translator-modules/blob/master/ncats/translator/modules/gene/anatomical_entity/README.md)| gene_to_tissue_bicluster |
|  |  [chemical substance](https://github.com/ncats/translator-modules/blob/master/ncats/translator/modules/gene/chemical_substance/README.md)| gene_to_chemical_interaction |
|  |  [gene](https://github.com/ncats/translator-modules/blob/master/ncats/translator/modules/gene/gene/README.md)| functional_similarity<br>gene_interaction<br>gene_to_gene_bicluster_RNAseqDB<br>gene_to_gene_bicluster_DepMap<br>phenotype_similarity |
| phenotypic feature | [disease](https://github.com/ncats/translator-modules/blob/master/ncats/translator/modules/phenotypic_feature/disease/README.md)| phenotype_to_disease_bicluster |


### Adding New Modules

See [the general guidelines for adding new modules](../../../docs).
