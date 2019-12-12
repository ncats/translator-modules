#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool

# Original baseCommand
baseCommand: [ functional_similarity, get-data-frame, to-json,--orient, records ]

# ResultList-driven baseCommand
# baseCommand: [ functional_similarity.py, get-result-list, to-json ]
inputs:
  input_genes:
    type: File
    inputBinding:
      position: 0
      prefix: --input_genes
  threshold:
    type: float
    default: 0.1
    inputBinding:
      position: 1
      prefix: --threshold
outputs:
  functionally_similar_genes:
    type: stdout
stdout: functional_similarity.records.json