#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ functional_similarity.py, get-data-frame, to-json,--orient, records ]
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
stdout: module1a.records.json