#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ phenotype_similarity.py, get-result-list, to-json ]
inputs:
  input_genes:
    type: File
    inputBinding:
      position: 0
      prefix: --input_genes
  threshold:
    type: float
    default: 0.10
    inputBinding:
      position: 1
      prefix: --threshold
outputs:
  phenotypically_similar_genes:
    type: stdout
stdout: phenotype_similarity.json