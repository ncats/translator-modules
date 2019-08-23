#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ DiseaseToPhenotypeBicluster.py, get-data-frame, to-json, --orient, records ]
inputs:
  input_diseases:
    type: string
    inputBinding:
      position: 0
      prefix: --input_diseases
outputs:
  disease_to_phenotype_bicluster_list:
    type: stdout
stdout: diseaseToPhenotypeBicluster.records.json