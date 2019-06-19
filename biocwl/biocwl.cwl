#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [python3, /mnt/c/Users/Ken/git/translator-modules/biocwl/biocwl.py, run]
inputs:
  input:
    type: string
    inputBinding:
      position: 3
outputs: []
