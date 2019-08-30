#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
    disease_id:
        type: string
    threshold_functional_similarity:
      type: float
      default: 0.75
    threshold_phenotype_similarity:
      type: float
      default: 0.10
    threshold_gene_interaction:
      type: int
      default: 12
outputs:
  functionally_similar_genes:
    type: File
    outputSource: functional_similarity/functionally_similar_genes
  phenotypically_similar_genes:
    type: File
    outputSource: phenotype_similarity/phenotypically_similar_genes
  interacting_genes:
    type: File
    outputSource: gene_interactions/interacting_genes
steps:
  diseases:
    run: module0.cwl
    in:
      disease_id: disease_id
    out: [ disease_list ]

  functional_similarity:
    run: module1a.cwl
    in:
      input_genes: diseases/disease_list
      threshold: threshold_functional_similarity
    out: [ functionally_similar_genes ]

  phenotype_similarity:
    run: module1b.cwl
    in:
      input_genes: diseases/disease_list
      threshold: threshold_phenotype_similarity
    out: [ phenotypically_similar_genes ]

  gene_interactions:
     run: module1e.cwl
     in:
       input_genes: diseases/disease_list
       threshold: threshold_gene_interaction
     out: [ interacting_genes ]