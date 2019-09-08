#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ disease_to_phenotype_bicluster.py, get-result-list, to-json ]
inputs:
  input_diseases:
    type: string
    inputBinding:
      position: 0
      prefix: --input_diseases
outputs:
  disease_to_phenotype_bicluster_list:
    type: stdout
stdout: disease_to_phenotype_bicluster.json