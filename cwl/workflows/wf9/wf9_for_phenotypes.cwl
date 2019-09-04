#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
    input_phenotypes:
        type: string
outputs:
  phenotype_to_disease_bicluster_list:
    type: File
    outputSource: phenotypeToDiseaseBicluster/phenotype_to_disease_bicluster_list
steps:
  phenotypeToDiseaseBicluster:
    run: phenotype_to_disease_bicluster.cwl
    in:
      input_phenotypes: input_phenotypes
    out: [ phenotype_to_disease_bicluster_list ]
