#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
    input_tissues:
        type: string
outputs:
  tissue_to_gene_bicluster_list:
    type: File
    outputSource: tissueToGeneBicluster/tissue_to_gene_bicluster_list
steps:
  tissueToGeneBicluster:
    run: tissue_to_gene_bicluster_rl.cwl
    in:
      input_tissues: input_tissues
    out: [ tissue_to_gene_bicluster_list ]
