#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ DiseaseToPhenotypeBicluster.py, get-data-frame, to-json, --orient, records ]
inputs:
  input_disease:
    type: string[]
    inputBinding:
      position: 0
      prefix: --input_disease
outputs:
  bicluster_list:
    type: stdout
stdout: diseaseToPhenotypeBicluster.records.json