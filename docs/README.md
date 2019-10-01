# Adding New Modules

The following developer guidelines (or suggestions) apply to new modules:

## Wrap your Modules using the Standard Module Design Pattern

The following is a sample Python module design pattern which could be generally emulated (substituting the pertinent
module *biolink.model* semantics which apply to your particular module)

```bash


from biolink.model import DiseaseToGeneAssociation, Disease, Gene

from translator_modules.core.data_transfer_model import ModuleMetaData, ConceptSpace

from translator_modules.core.module_payload import Payload

class MyModule:
    def __init__(self):
        pass

    def process_genes(self, input_gene_set, threshold):
        # do your processing here
        ...
        for item in my_local_results:
            chemical_hits.append({
                'input_id': ...  input id of starting query
                'input_symbol': ... human-meaningful symbolic acroymn for input id
                'hit_id': ... identifier hit id matched by algorithm to  input id
                'hit_symbol': ... human-meaningful symbolic acroymn for hit id
                'score': ...  score should be provided even if just 'one' (i.e. is a hit)
            })

        return pd.DataFrame(chemical_hits)

class MyModulePayload(Payload):

    def __init__(self, input_genes, threshold):

        super(MyModulePayload, self).__init__(
            module=MyModule(),
            metadata=ModuleMetaData(
                name="My New Module",
                source='My Knowledge Source',
                association=DiseaseToGeneAssociation,
                domain=ConceptSpace(Disease, ['MONDO']),
                relationship='related_to',
                range=ConceptSpace(Gene, ['HGNC']),
            )
        )

        input_gene_data_frame = self.get_input_data_frame(input_genes)

        self.results = self.module.process_genes(input_gene_data_frame, threshold)

def main():
    fire.Fire(MyModulePayload)

if __name__ == '__main__':
    main()
```


## Required Output Data  Format

The *self.results* variable returned by your module should  generally be a Pandas DataFrame with at least the following 
minimal set of column fields:

- input_id
- input_symbol
- hit_id
- hit_symbol
- score
 
Additional fields may be provided which add 'attribute' metadata for your results  (e.g. provenance metadata)
 

## Add your Module to the Package Index

To make your new module visible to the users of *ncats/translator-modules*, you need to update the package accordingly:

1. Place your module into the applicable translator_modules input/output subdirectory
2. Add your basic module documentation (i.e. with a basic command line execution example) to the README in the directory
3. Make sure that your module is tagged as 'executable' (i.e. chmod ugo+x the file)
4. Add your module name to the pip *setup.py* file as an *entrypoint*; Add any required *package_data* there if needed.
5. You can probably increment the minor version of the *setup.py* module *version* to account for your module addition.
