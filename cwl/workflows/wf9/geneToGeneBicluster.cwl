#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ GeneToGeneBicluster.py, get-data-frame, to-json, --orient, records ]
inputs:
  gene_list:
    type: File
    inputBinding:
      position: 0
      prefix: --input_gene_set_file
outputs:
  bicluster_list:
    type: stdout
stdout: geneToGeneBicluster.records.json