#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ gene_to_gene_bicluster_DepMap, get-data-frame, to-json, --orient, records ]
inputs:
  input_genes:
    type: string
    inputBinding:
      position: 0
      prefix: --input_genes
outputs:
  gene_to_gene_bicluster_DepMap_list:
    type: stdout
stdout: gene_to_gene_bicluster_DepMap.records.json