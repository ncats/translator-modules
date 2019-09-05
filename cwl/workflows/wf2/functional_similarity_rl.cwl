#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
# ResultList-driven baseCommand
baseCommand: [ functional_similarity.py, get-result-list, to-json ]
inputs:
  input_genes:
    type: File
    inputBinding:
      position: 0
      prefix: --input_genes
  threshold:
    type: float
    inputBinding:
      position: 1
      prefix: --threshold
outputs:
  functionally_similar_genes:
    type: stdout
stdout: functional_similarity.ncats