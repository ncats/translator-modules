#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ tissue_to_gene_bicluster.py, get-result-list, to-json ]
inputs:
  input_tissues:
    type: string
    inputBinding:
      position: 0
      prefix: --input_tissues
outputs:
  tissue_to_gene_bicluster_list:
    type: stdout
stdout: tissue_to_gene_bicluster.json