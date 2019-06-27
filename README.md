# Translator Modules

This package provides a Python-based implementation of the NCATS Translator workflow modules.


## Development

**Note:** code is now validated to work only with Python 3.7 only.  We recommend using a **virtualenv** 

``` 
virtualenv -p python3.7 py37
source py37/bin/activate
```

or **conda env** to manage packages and the development environment:

```
conda create -n translator-modules python=3.7
conda activate translator-modules
```

## Installation of Dependencies

Making sure that your pip version is 3.7 compliant.  The **translator-modules** package is not yet available 
through PyPI. To install, clone this repo and run the following command within the `translator_modules` directory:

```
pip install -r requirements.txt .
```

or

``` 
# sometimes better, to ensure that the proper Python3.7 version of pip is used...
python -m pip install -r requirements.txt .
```

To install the package in "developer" mode (such that code changes are automatically reflected in the local library), 
include the `-e` flag with `pip`:

```
pip install -r requirements.txt -e .
```

or

``` 
python -m pip install -r requirements.txt -e .
```
    
## Usage

A command line script is currently provided that will execute the relevant modules and commands for 
Translator "Workflow 2".  To display the full parameters of the script, type:

``` 
python scripts/WF2_automation.py --help
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

### Ontobio Cache Configuration

Note that the workflow 2 script relies on the Biolink "Ontobio" module to import its ontology for functional and 
phenotypic similarity computations. It is a known issue, however, that the use of the Python "cachier" cache library 
in Ontobio causes some runtime problems.

We therefore disable it in our code using the following ontobio configuration flag override (the flag defaults to 
'False' as it is defined in the library's _ontobio/config.yaml_ file):

    from ontobio.config import session
    session.config.ignore_cache = True
