#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ phenotype_to_disease_bicluster, get-result-list, to-json ]
inputs:
  input_phenotypes:
    type: string
    inputBinding:
      position: 0
      prefix: --input_phenotypes
outputs:
  phenotype_to_disease_bicluster_list:
    type: stdout
stdout: phenotype_to_disease_bicluster.json