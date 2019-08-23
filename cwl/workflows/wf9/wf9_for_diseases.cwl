#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
    input_diseases:
        type: string
outputs:
  disease_to_phenotype_bicluster_list:
    type: File
    outputSource: diseaseToPhenotypeBicluster/disease_to_phenotype_bicluster_list
steps:
  diseaseToPhenotypeBiclusterBicluster:
    run: diseaseToPhenotypeBicluster.cwl
    in:
      input_diseases: input_diseases
    out: [ disease_to_phenotype_bicluster_list ]
