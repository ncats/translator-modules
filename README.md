# Translator Modules

This package provides a Python-based implementation of the NCATS Translator workflow modules.

## Installation

The **translator-modules** package is not yet available through PyPI, thus, to install, clone this repo using git.

```bash
git clone https://github.com/ncats/translator-modules.git
```

The code is now validated to work only with Python 3.7 only.  We recommend using a **virtualenv** to enforce this.

``` 
virtualenv -p python3.7 py37
source py37/bin/activate
```

or, alternately, use **python venv** to manage packages and the development environment:

``` 
python3.7 -m venv venv
source venv/bin/activate
```

or, alternately, use **conda env** to manage packages and the development environment:

```
conda create -n translator-modules python=3.7
conda activate translator-modules
```

Some IDE's (e.g. PyCharm) may also have provisions for directly creating such a **virtualenv**. This should work fine.

## Installation of Dependencies

Make sure that your pip version is 3.7 compliant.  Then, run the following command within 
the `translator_modules` directory:

``` 
# sometimes better to use the 'python -m pip' version of pip rather than just 'pip'
# to ensure that the proper Python3.7 version of pip is used...
python -m pip install -r requirements.txt .
```

To install the package in "developer" mode (such that code changes are automatically reflected in the local library), 
include the `-e` flag with `pip`:

```
python -m pip install -r requirements.txt -e .
```

## Put the Modules on your System PATH

Some development tools (e.g. PyCharms, Eclipse) will do this for you but you often need to explicitly put the 
modules on your operating system path,

Assuming that you are in the project directory (as the 'present working directory'), then a way to do this is by 
adding `translator_modules` onto the system path directly.  On Linux, type the following

```bash
export PATH=$PATH$( find `pwd`/translator_modules/ -type d ! -name "__pycache__"  -printf ":%p" )
```

On the Mac, the standard (BSD) 'find' doesn't have the -printf flag. A workaround is to install the Gnu findutils using
[Homebrew](https://brew.sh) as follows:

```bash
brew install findutils

```

then substitute the *gfind* command for the *find* command in the PATH command above (Note: we provide a shell script
which you can use to set the environment using the bash 'source' command, as follows:

```bash
source scripts/set_macosx_path.sh
```
to help you. *Note:* you may need to run this script afresh in every new terminal 
session unless you add it into your shell login profile).

# Running the Translator Workflows

The modules in this repository may be composed into larger scientific workflows, managed by suitable software 
frameworks. A number of execution frameworks for doing this have been explored to date within NCATS:

1. Jupyter Notebooks 
2. Complete workflows can scripted
3. Workflow modules may be run individually from the command line (see below)
4. Using the Common Workflow Language (CWL) standard
5. Roll your own: call workflow modules from your own clients

##  1. Workflows in Jupyter Notebooks

See https://github.com/ncats/translator-workflows for numerous examples.

## 2. Running Complete Workflows as Python Scripts

A Python 3 command line script [WF2_automation.py script](direct-command-line-workflow2-script-usage)  
is currently provided that will directly execute the relevant modules and commands for 
the *NCATS Translator Workflow 2*.  To display the full parameters of the script, type:

``` 
./scripts/WF2_automation.py --help
```

A folder named  *Tidbit* will contain the results as HTML and JSON files. The latter (JSON) files include
an extra column called "shared_terms" which is the list of the intersection set of ontology terms 
identified during Jaccard scoring of the functional (GO term) or phenotype (HP term) overlap 
of the input gene list with the other genes listed in the given row.

When the '--verbose' flag is used, the script also echos tabular results to the standard output ("console").

A similar script is available for Translator [Workflow 9](https://www.lucidchart.com/invitations/accept/bd0b90df-45af-48a1-9777-7179a17f0b63), i.e.

``` 
./sn cripts/WF9_automation.py --help
```

The scripts (as are the modules) are marked up with the "hash bang ("#!") Unix script comment at the top so generally
if marked as executable, may be run directly as above, but in some environments (e.g. Windows) you may need to 
explicitly run them as a Python script, i.e.

``` 
python scripts/WF2_automation.py --help
```

## 3. Running Workflow Modules individually from the Command line

Assuming that you have put the translator modules on your path (see section above), then they may be run 
as individual programs from the command line terminal of your operation system.

For example, a "gene to gene bicluster" algorithm (based on RNAseqDB data, module naming convention by data source is in progress) implemented as a module in NCATS Translator Workflow 9 
may be run  as follows:

``` 
gene_to_gene_bicluster.py --input_genes "ENSG00000121410,ENSG00000268895,ENSG00000148584" get-data-frame to-json --orient records
```

This outputs the results as a JSON formatted dump of a Pandas DataFrame.  If a CSV version of the results is desired, 
then a simple change to the command line will generate it:

``` 
gene_to_gene_bicluster.py --input_genes "ENSG00000121410,ENSG00000268895,ENSG00000148584" get-data-frame to-csv
```


In fact, all the various Pandas DataFrame output methods are available (see the 
[Pandas IO docs](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html#serialization-io-conversion)). 
Just substitute the 'to-json' and 'to-csv' method command keywords with your chosen target format (e.g. to-excel, etc.)

An alternate "ResultList" JSON output forma, which is more complete with additional annotation 
and the Biolink model metadata, may be generated as follows:

``` 
gene_to_gene_bicluster.py --input_genes "ENSG00000121410,ENSG00000268895,ENSG00000148584" get-result-list to-json       
```

This Translators-specific JSON format is mainly to empower interoperability of the modules with one another 
and with other Translator tools. A sample version of it (from a  'functional similarity' run) may be found 
[here](https://github.com/ncats/translator-modules/blob/master/docs/functional_similarity.json) (Hint: use the
 FireFox web browser for a convenient view of this JSON). The Python code 
defining and manipulating the "ResultList" module data model is in the module
[data_transfer_model.py](https://github.com/ncats/translator-modules/blob/master/translator_modules/core/data_transfer_model.py).

In both cases above, a relatively short list of genes is provided using a string of comma-delimited identifiers 
which should ideally be CURIE formatted but in some cases (e.g.  *Ensembl* identifiers) may be just the 
object identifiers of the data (the module *may* be clever enough to resolve them - your mileage may vary!). 

That said, these modules can also take CSV, tab delimited text and JSON files or URL-resolvable web (REST) resources 
as the source of module input, as long as those files comply with the expected text format (which can be, in fact, the
text output file from another module, previously run!). 

``` 
gene_to_gene_bicluster.py --input_genes /relative/or/absolute/path/to/your/gene_list.csv get-result-list to-json       
```

For the JSON inputs (which may either
be in Pandas DataFrame or ResultList format), the input process simply checks for a top level JSON object tag
called 'result_list_name' to discriminate (the Pandas DataFrame JSON doesn't contain it!)

### How the Modules are Indexed

The modules themselves have been partitioned in packages indexed by their input and output Biolink concept categories.
For example, the **disease_associated_genes.py** module is found under the *translator_modules.disease.gene* package 
[here](https://github.com/ncats/translator-modules/blob/master/translator_modules/disease/gene)

Additional documentation for the various scripts will generally be found within each package containing the scripts,
for example, [here](https://github.com/ncats/translator-modules/blob/master/translator_modules/disease/gene/README.md)

Here is a summary table of the current inventory of Biolink data type categories processed with their associated modules

| Input Category | Output Category | Module(s) |
| --- | --- | --- |
| anatomical entity | [anatomical entity](https://github.com/ncats/translator-modules/blob/master/translator_modules/anatomical_entity/anatomical_entity/README.md) | tissue_to_tissue_bicluster.py |
|   | [gene](https://github.com/ncats/translator-modules/blob/master/translator_modules/anatomical_entity/gene/README.md)| tissue_to_gene_bicluster.py |
| disease | [gene](https://github.com/ncats/translator-modules/blob/master/translator_modules/disease/gene/README.md)| disease_associated_genes.py |
|  | [phenotypic feature](https://github.com/ncats/translator-modules/blob/master/translator_modules/disease/phenotypic_feature/README.md)| disease_to_phenotype_bicluster.py |
| gene | [anatomical entity](https://github.com/ncats/translator-modules/blob/master/translator_modules/gene/anatomical_entity/README.md)| gene_to_tissue_bicluster.py |
|  |  [chemical substance](https://github.com/ncats/translator-modules/blob/master/translator_modules/gene/chemical_substance/README.md)| chemical_gene_interaction.py |
|  |  [gene](https://github.com/ncats/translator-modules/blob/master/translator_modules/gene/gene/README.md)| functional_similarity.py<br>gene_interaction.py<br>gene_to_gene_bicluster.py<br>phenotype_similarity.py |
| phenotypic feature | [disease](https://github.com/ncats/translator-modules/blob/master/translator_modules/phenotypic_feature/disease/README.md)| phenotype_to_disease_bicluster.py |

## 4. Common Workflow Language Running of Translator Workflows

See the [Translator CWL workflow scripts and documentation](./cwl)

## 5. Calling the Code Directly in your own Python Clients

Review of the available workflow scripts (e.g. for workflow  2 and  9) provides some guidance on how to use the modules
directly. You can also directly review the modules themselves.  As an example, we discuss here the Workflow 2 modules.

### Workflow 2 Gene Similarities and Interactions

Within your application, there is a three step process for similarity searching:

I. An _in memory_ copy of the relevant ontology and annotation catalogs plus other setup processes are 
triggered by instantiating the following three class objects (again, at the top of your file, 
run once outside of any data loops):

a) ```FunctionalSimilarity('human')``` for molecular function and biological process comparisons (GO).
b) ```PhenotypeSimilarity('human')``` for phenotype ontology comparisons (HPO).
c) ```GeneInteractions()``` for accessing protein-protein interactions (Monarch via Biolink API)

Note that the object handles returned by each of the three functions are then used to call associated computations on
each kind of catalog. Such computations may be done repeatedly on the handle, since the ontology catalogs are only used 
'read-only'.

II. Next, obtain a "seed" list of (disease) related genes for input to the comparison. This may be obtained by running 
the *disease_gene_lookup()* function using the disease name and mondo identifier as input parameters. Alternately, 
any *ad hoc* list of genes may be compiled as long as they have the structure implied by the output Pandas data frame of 
the *disease_gene_lookup()* function.

III.  Finally, call the model-associated method - similarity() (for the FunctionalSimilarity and PhenotypeSimilarity)
or gene_interactions() (for GeneInteractions()) - with the gene list from III with any other applicable parameters.

Repeat steps II and III above for each disease you wish to analyze.
