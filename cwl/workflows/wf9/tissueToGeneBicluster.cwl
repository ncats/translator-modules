#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ TissueToGeneBicluster.py, get-data-frame, to-json, --orient, records ]
inputs:
  input_tissue:
    type: string[]
    inputBinding:
      position: 0
      prefix: --input_tissue
outputs:
  bicluster_list:
    type: stdout
stdout: tissueToGeneBicluster.records.json