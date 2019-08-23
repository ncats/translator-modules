#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
    input_genes:
        type: string
outputs:
  phenotype_to_disease_bicluster_list:
    type: File
    outputSource: phenotypeToDiseaseBicluster/phenotype_to_disease_bicluster_list
steps:
  phenotypeToDiseaseBicluster:
    run: phenotypeToDiseaseBicluster.cwl
    in:
      input_phenotypes: input_phenotypes
    out: [ phenotype_to_disease_bicluster_list ]
