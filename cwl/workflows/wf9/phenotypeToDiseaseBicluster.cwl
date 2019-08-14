#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ PhenotypeToDiseaseBicluster.py, get-data-frame, to-json, --orient, records ]
inputs:
  input_phenotype:
    type: string[]
    inputBinding:
      position: 0
      prefix: --input_phenotype
outputs:
  bicluster_list:
    type: stdout
stdout: phenotypeToDiseaseBicluster.records.json