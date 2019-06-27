#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [Biocwl.py, run]
inputs:
  input:
    type: string
    inputBinding:
      position: 0
outputs: []
