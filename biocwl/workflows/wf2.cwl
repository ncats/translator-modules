#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
  disease: # TODO -- biolink style file

outputs:
  summary:
    type: File
    outputSource: # TODO

steps:
  diseases:
    run: module0.cwl
    in:
        # TODO
    out: # TODO

  functional_similarity:
    run: module1a.cwl
    in:
      src: # TODO
    out: # TODO

  phenotypic_similarity:
    run: module1b.cwl
    in:
      src: # TODO
    out: # TODO

  gene_interaction:
    run: module1e.cwl
    in:
      src: # TODO
    out: # TODO

  summarize:
    run: module1e.cwl
    in:
      src: # TODO
    out: # TODO