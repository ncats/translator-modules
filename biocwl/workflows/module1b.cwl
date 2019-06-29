#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ module1a.py, get-data-frame, to-json ]
inputs:
  gene_set:
    type: File
    format: iana:application/json
    inputBinding:
      position: 0
      prefix: --input-gene-set
  threshold:
    type: float
    inputBinding:
      position: 1
      prefix: --threshold
outputs:
  functionally_similar_genes:
    type: stdout
stdout: module1a.json

$namespaces:
  iana: https://www.iana.org/assignments/media-types/