#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

inputs:
    disease_id:
        type: string
outputs:
  disease_list:
    type: File
    outputSource: diseases/disease_list
  chemically_interacting_genes:
    type: File
    outputSource: chemical_gene_interaction/chemically_interacting_genes
steps:
  diseases:
    run: disease_associated_genes_rl.cwl
    in:
      disease_id: disease_id
    out: [ disease_list ]

  chemical_gene_interaction:
    run: chemical_gene_interaction_rl.cwl
    in:
      input_genes: diseases/disease_list
    out: [ chemically_interacting_genes ]
