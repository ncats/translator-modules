#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ GeneToGeneBicluster.py, get-data-frame, to-json, --orient, records ]
inputs:
  # TODO: does this take HGNC ids, to bridge WF2 to WF9?
  input_genes:
    type: string[]  # TODO: make polymorphic to eg Files
    # TODO: add biolink model
    inputBinding:
      position: 0
      prefix: --input_genes
outputs:
  bicluster_list:
    type: stdout
stdout: geneToGeneBicluster.records.json