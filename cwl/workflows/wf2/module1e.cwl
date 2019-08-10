#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ module1e.py, --file=True, get-data-frame, to-json, --orient, records ]
inputs:
  input_genes:
    type: File
    inputBinding:
      position: 0
      prefix: --input_genes
  threshold:
    type: int
    inputBinding:
      position: 1
      prefix: --threshold
outputs:
  gene_interaction_list:
    type: stdout
stdout: module1e.records.json