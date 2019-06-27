#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ module1a.py, get-data-frame, to-json ]
inputs:
  disease_name:
    type: string
    inputBinding:
      position: 0
      prefix: --input-disease-name
  disease_id:
    type: string
    inputBinding:
      position: 1
      prefix: --input-disease-mondo
outputs:
  disease_list:
    type: stdout
stdout: module0.json