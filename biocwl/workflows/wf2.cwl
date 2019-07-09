#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
    disease_name: string
    disease_id: string
    threshold_functional:
      type: float
      default: 0.75
    threshold_phenotype:
      type: float
      default: 0.10
outputs:
  functionally_similar_genes:
    type: File
    outputSource: functional_similarity/functionally_similar_genes
  phenotypically_similar_genes:
    type: File
    outputSource: phenotype_similarity/phenotypically_similar_genes
  gene_interaction_set:
    type: File
    outputSource: gene_interactions/gene_interaction_set
steps:
  diseases:
    run: module0.cwl
    in:
      disease_name: disease_name
      disease_id: disease_id
    out: [ disease_list ]

  functional_similarity:
    run: module1a.cwl
    in:
      gene_set: diseases/disease_list
      threshold: threshold_functional
    out: [ functionally_similar_genes ]

  phenotype_similarity:
    run: module1b.cwl
    in:
      gene_set: diseases/disease_list
      threshold: threshold_phenotype
    out: [ phenotypically_similar_genes ]

  gene_interactions:
    run: module1e.cwl
    in:
      gene_set: diseases/disease_list
    out: [ gene_interaction_set ]