#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
    disease_name:
        type: string
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
    action:
       type: string
       default: ""
outputs:
  functionally_similar_genes:
    type: File
    outputSource: functional_similarity/functionally_similar_genes
  phenotypically_similar_genes:
    type: File
    outputSource: phenotype_similarity/phenotypically_similar_genes
  gene_interaction_list:
    type: File
    outputSource: gene_interactions/gene_interaction_list
  chemical_interaction_list:
    type: File
    outputSource: chemical_interactions/chemical_interaction_list

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
      threshold_functional_similarity: threshold_functional_similarity
    out: [ functionally_similar_genes ]

  phenotype_similarity:
    run: module1b.cwl
    in:
      gene_set: diseases/disease_list
      threshold_phenotype_similarity: threshold_phenotype_similarity
    out: [ phenotypically_similar_genes ]

  chemical_interactions:
    run: module1d.cwl
    in:
        gene_set: diseases/disease_list
        action: action
    out: [ chemical_interaction_list ]

  gene_interactions:
     run: module1e.cwl
     in:
       gene_set: diseases/disease_list
       threshold_interaction: threshold_gene_interaction
     out: [ gene_interaction_list ]