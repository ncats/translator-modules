#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
    input_genes:
        type: string
outputs:
  gene_bicluster_list:
    type: File
    outputSource: geneToGeneBicluster/bicluster_list
steps:
  geneToGeneBicluster:
    run: geneToGeneBicluster.cwl
    in:
      input_genes: input_genes
    out: [ bicluster_list ]
