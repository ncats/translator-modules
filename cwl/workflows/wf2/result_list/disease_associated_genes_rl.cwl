#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
# ResultList-driven baseCommand
baseCommand: [ disease_associated_genes, get-result-list, to-json ]
inputs:
  disease_id:
    type: string
    inputBinding:
      prefix: --disease_id
outputs:
  disease_list:
    type: stdout
stdout: disease_associated_genes.json