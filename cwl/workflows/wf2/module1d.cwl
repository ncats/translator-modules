#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ module1d.py, get-data-frame, to-json, --orient, records ]
inputs:
  gene_set:
    type: File
    inputBinding:
      position: 0
      prefix: --input_gene_set_file
  action:
    type: string
    inputBinding:
      position: 1
      prefix: --action
outputs:
  chemical_interaction_list:
    type: stdout
stdout: module1d.records.json