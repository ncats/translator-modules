#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ gene_interaction, get-result-list, to-json ]
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
  interacting_genes:
    type: stdout
stdout: gene_interaction.json