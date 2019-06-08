# Translator Modules

This package provides a Python-based implementation of the NCATS Translator workflow modules.

## Installation

**Note:** code has been tested with Python 3.7 only.

The **translator-modules** package is not yet available through PyPI. To install, clone this repo and run the following command within the `translator_modules` directory:

```
pip install -r requirements.txt .
```

## Development

We recommend using a **virtualenv** or **conda env** to manage packages and the development environment:

```
conda create -n translator-modules python=3.7
conda activate translator-modules
```

To install the package in "developer" mode (such that code changes are automatically reflected in the local library), include the `-e` flag with `pip`:

```
pip install -r requirements.txt -e .
```

### Ontobio Patch (temporary)

The workflow 2 script relies on the Biolink "Ontobio" module to import its ontology for functional and phenotypic similarity computations. It is a known issue, however, that the use of the Python "cachier" cache library in Ontobio causes some runtime problems.
We therefore disable it in our code using the following:

    from ontobio.config import session
    session.config.ignore_cache = True
    
where the Ontobio version we are using is a patched version which has an  _ignore_cache_ flag in the library's 
_ontobio/config.yaml_ file) to disable the cachier cache. As of June 4th, 2019, this code is only available on a Git 
repository forked from the main Biolink Ontobio project. 

This patch version may be installed after the above pip requirements is run, as follows:

``` 
# Uninstall the default version installed by the requirements file
python -m pip uninstall ontobio

# install a fresh version of the forked code
python -m pip install git+https://github.com/STARInformatics/ontobio@master#egg=ontobio
```

Once the main Biolink Ontobio project has validated the pull request for this code, this patch will not be required and these README instructions will therefore be revised.

## Usage

A command line script is currently provided that will execute the relevant modules and commands for 
Translator "Workflow 2".  To display the full parameters of the script, type:

``` 
python WF2_automation.py --help
```

A folder named  *Tidbit* will contain the results as HTML and JSON files. The latter (JSON) files include
an extra column called "shared_terms" which is the list of the intersection set of ontology terms 
identified during Jaccard scoring of the functional (GO term) or phenotype (HP term) overlap 
of the input gene list with the other genes listed in the given row.

When the '--verbose' flag is used, the script also echos tabular results to the standard output ("console").

## Calling the Code Directly in your own Python Clients

Examination of the standalone script reveals how to use the code directly in other software. Assuming that the pip dependencies
have been installed, you'll reset the *ignore_cache* flag to **True** at the top of your main Python application file _before_ importing 
any of the main modules, as we mentioned above:

    from ontobio.config import session
    session.config.ignore_cache = True
    
Within your application, there is a three step process for similarity searching:

I. An _in memory_ copy of the relevant ontology and annotation catalogs plus other setup processes are 
triggered by instantiating the following three class objects (again, at the top of your file, run once outside of any data loops):

a) ```FunctionalSimilarity('human')``` for GO molecular function and biological process comparisons.
b) ```PhenotypeSimilarity('human')``` for phenotype ontology comparisons.
c) ```GeneInteractions()``` for accessing Monarch Biolink catalog of gene interactions

Note that the object handles returned by each of the three functions are then used to call associated computations on
each kind of catalog. Such computations may be done repeatedly on the handle, since the ontology catalogs are only used 
'read-only'.

II. Next, obtain a "seed" list of (disease) related genes for input to the comparison. This may be obtained by running 
the *disease_gene_lookup()* function using the disease name and mondo identifier as input parameters. Alternately, any *ad hoc* 
list of genes may be compiled as long as they have the structure implied by the output Pandas data frame of 
the *disease_gene_lookup()* function.

III.  Finally, call the model-associated method - similarity() (for the FunctionalSimilarity and PhenotypeSimilarity)
or gene_interactions() (for GeneInteractions()) - with the gene list from III with any other applicable parameters.

Repeat steps II and III above for each disease you wish to analyze.
