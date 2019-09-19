#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
    input_genes:
        type: string
outputs:
  gene_to_gene_bicluster_list:
    type: File
    outputSource: geneToGeneBicluster/gene_to_gene_bicluster_list
  gene_to_tissue_bicluster_list:
    type: File
    outputSource: geneToTissueBicluster/gene_to_tissue_bicluster_list
steps:
  geneToGeneBicluster:
    run: gene_to_gene_bicluster_RNAseqDB.cwl
    in:
      input_genes: input_genes
    out: [ gene_to_gene_bicluster_RNAseqDB_list ]
  geneToGeneBicluster:
    run: gene_to_gene_bicluster_DepMap.cwl
    in:
      input_genes: input_genes
    out: [ gene_to_gene_bicluster_DepMap_list ]

  geneToTissueBicluster:
    run: gene_to_tissue_bicluster.cwl
    in:
      input_genes: input_genes
    out: [ gene_to_tissue_bicluster_list ]
