#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
    input_genes:
        type: string

outputs:
  gene_to_gene_bicluster_RNAseqDB_list:
    type: File
    outputSource: geneToGeneBicluster/gene_to_gene_bicluster_RNAseqDB_list
  gene_to_gene_bicluster_DepMap_list:
    type: File
    outputSource: geneToGeneBicluster/gene_to_gene_bicluster_DepMap_list
  gene_to_tissue_bicluster_list:
    type: File
    outputSource: geneToTissueBicluster/gene_to_tissue_bicluster_list

steps:
  geneToGeneBiclusterRNAseqDB:
    run: gene_to_gene_bicluster_RNAseqDB_rl.cwl
    in:
      input_genes: input_genes
    out: [ gene_to_gene_bicluster_RNAseqDB_list ]

  geneToGeneBiclusterDepMap:
    run: gene_to_gene_bicluster_DepMap_rl.cwl
    in:
      input_genes: input_genes
    out: [ gene_to_gene_bicluster_DepMap_list ]

  geneToTissueBicluster:
    run: gene_to_tissue_bicluster_rl.cwl
    in:
      input_genes: input_genes
    out: [ gene_to_tissue_bicluster_list ]
