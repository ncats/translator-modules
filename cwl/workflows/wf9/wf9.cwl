#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
    gene_list:
        type: File
outputs:
  gene_bicluster_list:
    type: File
    outputSource: geneToGeneBicluster/bicluster_list
steps:
  geneToGeneBicluster:
    run: geneToGeneBicluster.cwl
    in:
      gene_list: gene_list
    out: [ bicluster_list ]
