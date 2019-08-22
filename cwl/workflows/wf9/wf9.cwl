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
    run: geneToGeneBicluster.cwl
    in:
      input_genes: input_genes
    out: [ gene_to_gene_bicluster_list ]
  geneToTissueBicluster:
    run: geneToTissueBicluster.cwl
    in:
      input_genes: input_genes
    out: [ gene_to_tissue_bicluster_list ]
