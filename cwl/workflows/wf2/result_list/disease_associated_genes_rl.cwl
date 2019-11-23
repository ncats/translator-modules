#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool

# ResultList-driven baseCommand
baseCommand: [ disease_associated_genes, get-result-list, to-json ]

inputs:
  disease_identifier:
    type: string
    inputBinding:
      prefix: --disease_identifier
  disease_label:
    type: string
    inputBinding:
      prefix: --disease_label
outputs:
  disease_list:
    type: stdout
stdout: disease_associated_genes.json