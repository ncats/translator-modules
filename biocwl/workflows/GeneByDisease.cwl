#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [GeneByDisease.py, run]
inputs:
  disease_id:
    type: string
    inputBinding:
      position: 1
outputs:
  genes:
    type:
      type: array
      items: string
    outputBinding:
        glob: "*.txt"