#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ module1e.py, get-data-frame, to-json, --orient, records ]
inputs:
  gene_set:
    type: File
    inputBinding:
      position: 0
      prefix: --input_gene_set_file
    threshold:
    # the other module thresholds are floats but
    # in this case, we have an integer counts?
    type: integer
    inputBinding:
      position: 1
      prefix: --threshold
outputs:
  gene_interaction_set:
    type: stdout
stdout: module1e.records.json