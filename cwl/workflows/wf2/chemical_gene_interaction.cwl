#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ chemical_gene_interaction.py, get-data-frame, to-json, --orient, records ]
inputs:
  input_genes:
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