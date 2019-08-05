#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ module1b.py, --file=True, get-data-frame, to-json, --orient, records ]
inputs:
  gene_set:
    type: File
    inputBinding:
      position: 0
      prefix: --input_genes
  threshold_phenotype_similarity:
    type: float
    default: 0.10
    inputBinding:
      position: 1
      prefix: --threshold
outputs:
  phenotypically_similar_genes:
    type: stdout
stdout: module1b.records.json