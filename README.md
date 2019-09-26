# Contents

- [Translator Modules](#translator-modules)
    - [Installation](#installation)
    - [Installation of Dependencies and Make Modules Visible as Command Line Programs](#installation-of-dependencies-and-make-modules-visible-as-command-line-programs)
- [Running the Translator Workflows](#running-the-translator-workflows)
    - [1. Workflows in Jupyter Notebooks](#1.-Workflows-in-jupyter-notebooks)
    - [2. Running Complete Workflows as Python Scripts](#2.-running-completes-workflows-as-python-scripts)
    - [3. Running Workflow Modules individually from the Command line](#3.-running-workflow-modules-individually-from-the-command-line)
        - [How the Modules are Indexed](#how-the-modules-are-indexed)
    - [4. Common Workflow Language Running of Translator Workflows](#4.-common-workflow-language-running-of-translator-workflows)
    - [5. Calling the Code Directly in your own Python Clients](#5.-calling-the-code-directly-in-your-own-python-clients)
        - [Workflow 2 Gene Similarities and Interactions](#workflow-2-gene-similarities-and-interactions)
- [Running the Translator Module System with Docker (Compose)](#running-the-translator-module-system-with-docker-compose)
    - [For Docker Compose System Services](#docker-compose-system-services)
        - [Identifiers Resolution Service](#identifiers-resolution-service)
        - [Ontology Lookup Service](#ontology-lookup-service)
    - [Developer Modification of System Service APIs or Addition of New Services](#developer-modification-of-system-service-apis-or-addition-of-new-services)

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

## Installation of Dependencies and Make Modules Visible as Command Line Programs

Make sure that your pip version is 3.7 compliant.  Then, run the following command within the 
`translator_modules` directory:

```
# sometimes better to use the 'python -m pip' version of pip rather than just 'pip'
# to ensure that the proper Python3.7 version of pip is used...
python -m pip install -r requirements.txt .
```

This also has the side effect of ensuring that all the modules are visible for execution as standalone programs using
the bare module names (without the **.py** file extension; Note that you may have to rerun this command for every new
terminal session on your operating system)

To install the package in "developer" mode (such that code changes are automatically reflected in the local library), 
include the `-e` flag with the `pip` command, namely:

```
python -m pip install -r requirements.txt -e .
```

# Running the Translator Workflows

The modules in this repository may be composed into larger scientific workflows, managed by suitable software 
frameworks. A number of execution frameworks for doing this have been explored to date within NCATS:

1. Jupyter Notebooks
2. Complete workflows can scripted
3. Workflow modules may be run individually from the command line (see below)
4. Using the Common Workflow Language (CWL) standard
5. Roll your own: call workflow modules from your own clients

## 1. Workflows in Jupyter Notebooks

See https://github.com/ncats/translator-workflows for numerous examples.

## 2. Running Complete Workflows as Python Scripts

A Python 3 command line script [WF2_automation.py script](direct-command-line-workflow2-script-usage) is currently 
provided that will directly execute the relevant modules and commands for the *NCATS Translator Workflow 2*.  
To display the full parameters of the script, type:

```
./scripts/WF2_automation.py --help
```

A folder named  *Tidbit* will contain the results as HTML and JSON files. The latter (JSON) files include
an extra column called "shared_terms" which is the list of the intersection set of ontology terms identified during 
Jaccard scoring of the functional (GO term) or phenotype (HP term) overlap of the input gene list with the other 
genes listed in the given row.

When the '--verbose' flag is used, the script also echos tabular results to the standard output ("console").

A similar script is in the works for Translator [Workflow 9](https://www.lucidchart.com/documents/edit/22689882-2099-4acb-961a-fa6202f2cfd8/0_0).


The script (as are the modules) are marked up with the "hash bang ("#!") Unix script comment at the top so generally
if marked as executable, may be run directly as above, but in some environments (e.g. Windows) you may need to 
explicitly run them as a Python script, i.e.

```
python scripts/WF2_automation.py --help
```

## 3. Running Workflow Modules individually from the Command line

Assuming that you have [properly configured things](#installation-of-dependencies-and-make-modules-visible-as-command-line-programs)], 
then the modules may be run as individual programs from the command line terminal of your operation system.

For example, a *gene to gene bicluster* algorithm (based on RNAseqDB data, module naming convention by data source 
is in progress) implemented as a module in NCATS Translator Workflow 9 and may be run  as follows:


``` 
gene_interaction --input-genes "HGNC:1100,HGNC:12829" get-data-frame to-json --orient records

```

This outputs the results as a JSON formatted dump of a Pandas DataFrame.  If a CSV version of the results is desired, 
then a simple change to the command line will generate it:

``` 
gene_interaction --input-genes "HGNC:1100,HGNC:12829" get-data-frame to-csv
```


In fact, all the various Pandas DataFrame output methods are available (see the [Pandas IO docs](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html#serialization-io-conversion)).

Just substitute the 'to-json' and 'to-csv' method command keywords with your chosen target format (e.g. to-excel, etc.)

An alternate "ResultList" JSON output forma, which is more complete with additional annotation and the Biolink model 
metadata, may be generated as follows:

``` 
gene_interaction --input-genes "HGNC:1100,HGNC:12829" get-result-list to-json       
```

This Translators-specific JSON format is mainly to empower interoperability of the modules with one another and with 
other Translator tools. A sample version of it (from a  'functional similarity' run) may be found [here](https://github.com/ncats/translator-modules/blob/master/docs/functional_similarity.json) (Hint: use the FireFox web browser for a convenient view of this JSON). The Python code defining and manipulating the "ResultList" module data model is in the module [data_transfer_model.py](https://github.com/ncats/translator-modules/blob/master/translator_modules/core/data_transfer_model.py).

In both cases above, a relatively short list of genes is provided using a string of comma-delimited identifiers which 
should ideally be CURIE formatted but in some cases (e.g. *Ensembl* identifiers) may be just the object identifiers 
of the data (the module *may* be clever enough to resolve them - your mileage may vary!).

That said, these modules can also take CSV, tab delimited text and JSON files or URL-resolvable web (REST) resources 
as the source of module input, as long as those files comply with the expected text format (which can be, in fact, the 
text output file from another module, previously run!).

``` 
gene_interaction --input-genes /relative/or/absolute/path/to/your/gene_list.csv get-result-list to-json       
```

For the JSON inputs (which may either
be in Pandas DataFrame or ResultList format), the input process simply checks for a top level JSON object tag
called 'result_list_name' to discriminate (the Pandas DataFrame JSON doesn't contain it!)

More information about the modules are found [here]().

## 4. Common Workflow Language Running of Translator Workflows

See the [Translator CWL workflow scripts and documentation](./cwl)

## 5. Calling the Code Directly in your own Python Clients

Review of the available workflow scripts (e.g. for workflow  2 and  9) provides some guidance on how to use the modules
directly. You can also directly review the modules themselves.  As an example, we discuss here the Workflow 2 modules.

### Workflow 2 Gene Similarities and Interactions

Within your application, there is a three step process for similarity searching:

I. An _in memory_ copy of the relevant ontology and annotation catalogs plus other setup processes are triggered by 
instantiating the following three class objects (again, at the top of your file, run once outside of any data loops):

a) ```FunctionalSimilarity('human')``` for molecular function and biological process comparisons (GO).
b) ```PhenotypeSimilarity('human')``` for phenotype ontology comparisons (HPO).
c) ```GeneInteractions()``` for accessing protein-protein interactions (Monarch via Biolink API)

Note that the object handles returned by each of the three functions are then used to call associated computations on
each kind of catalog. Such computations may be done repeatedly on the handle, since the ontology catalogs are only 
used 'read-only'.

II. Next, obtain a "seed" list of (disease) related genes for input to the comparison. This may be obtained by running 
the *disease_gene_lookup()* function using the disease name and mondo identifier as input parameters. Alternately, any 
*ad hoc* list of genes may be compiled as long as they have the structure implied by the output Pandas data frame 
of the *disease_gene_lookup()* function.

III.  Finally, call the model-associated method - similarity() (for the FunctionalSimilarity and PhenotypeSimilarity)
or gene_interactions() (for GeneInteractions()) - with the gene list from III with any other applicable parameters.

Repeat steps II and III above for each disease you wish to analyze.

# Running the Translator Module System with Docker (Compose)

Use [Docker Compose](https://docs.docker.com/compose/) to build and run the application. 
Before using compose in the project, you should first copy the configuration file:

```
cp docker-compose.yaml-template docker-compose.yaml
```

Then type the following into the terminal::

```
cd translator-modules
docker-compose build
docker-compose up
```

**Note:** If the docker-compose commands are is giving you trouble, try running them as the system administrator with 
the `sudo` command. Remember, though, that if you are running  your commands as 'sudo', then depending on how your 
OS instance configures sudo, in some cases, $HOME may actually be '/root' or it may otherwise still be in your 
normal user home.

The REST API should now be running at http://localhost: on ports 8081 and 8082, the OpenAPI web interface at 
http://localhost:<port#>>/api/ui. You can open your browser with these addresses to see these applications in action.

## Docker Compose System Services

This form of running the Translator Modules ecosystem involved conversion of some components of the system to 
persistently running Docker container managed microservices. Initially (as of September 2019) this consists of two
services: the *Identifier Resolution* service and the *Ontology* service.  Basically, these services operate as 
_client/server_ implementations of libraries which load their associated (meta-)data catalogs just once upon startup
of the container, then provide a local OpenAPI compliant web service REST API to perform the various supported queries.

Previously, each of these components were (repetitively) initialized each time a module was started. In the case of 
the Identifier Resolver, a local mapping file was loaded. In the case of the Ontology service, a remote ontology 
database was queries to pull over the entire ontology required (e.g. parts of Gene Ontology). In both cases, this 
resulted in a hugely wasteful overhead. 

The new Docker based services only perform this (meta-) data loading once, after which point, module start-up and 
quick local web service access for the module to needed (meta-)data promises to become orders of magnitude more rapid.

More details about these client/server subsystems, as they are developed, will be mentioned here.

#### Identifiers Resolution Service

The [Identifiers Resolution Service](https://github.com/ncats/translator-modules/tree/docker-compose-system/ncats/translator/identifiers) 
provides an API for translating concept identifiers from one namespace to another.
The initial implementation focuses on gene identifiers (e.g. HGNC identifiers to gene symbols, Ensembl, NCBIGene, etc.)

#### Ontology Lookup Service

This [Ontology Lookup Service](https://github.com/ncats/translator-modules/tree/docker-compose-system/ncats/translator/ontology) 
is still under development.

### Developer Modification of System Service APIs or Addition of New Services

We have specified the web services in OpenAPI 3.0 YAML specification files are found in each subdirectory 
- i.e. _identifiers_ and _ontology_ - related to each microservice. These subdirectories also have the corresponding 
client/server code in *client* and  *server* subfolders.

The *client* is a direct Python web service client and the *server* is a simple Python Flask server implementation.

By [installing a local copy of the OpenAPI Code Generator](https://openapi-generator.tech/docs/installation), 
modified OpenAPI 3.0 YAML specifications can be processed to recreate the Python client and Python Flask server stubs.

First, you may first wish to check your modified OpenAPI YAML specification, using the _validate_ command:

```bash
openapi-generator validate (-i | --input-spec) <spec file>
```

If it passes muster, then  to recreate the Python Flask *server* stubs, type the following 
(run from the root project directory):

```bash
cd translator-modules
openapi-generator generate --input-spec=ncats/translator/identifiers/ncats_translator_module_identifiers_api.yaml \
                    --model-package=model \
                    --output=ncats/translator/identifiers/server \
                    --generator-name=python-flask \
                    --additional-properties=\
--packageName=ncats.translator.identifiers.server.openapi_server,\
--projectName=identifier-resolver-server,\
—-packageVersion="0.0.1",\
--packageUrl=https://github.com/ncats/translator-modules/tree/master/ncats/translator/identifiers/server,\
--serverPort=8081
```

To recreate the matching *client* Python access stubs, type something the following 
(from the root project directory):

```bash
cd translator-modules
openapi-generator generate  --input-spec=ncats/translator/identifiers/ncats_translator_module_identifiers_api.yaml \
                    --model-package=model \
                    --output=ncats/translator/identifiers/client \
                    --generator-name=python \
                    --additional-properties=\
--packageName=ncats.translator.identifiers.client.openapi_client,\
--projectName=identifier-resolver-client,\
—-packageVersion="0.0.1",\
--packageUrl=https://github.com/ncats/translator-modules/tree/master/ncats/translator/identifiers/client
```

Consult the [OpenAPI 3.0 'generate' command usage](https://openapi-generator.tech/docs/usage#generate) 
for more specific details on available code generation options and for acceptable program flag abbreviations (here we
used the long form of the flags)

In  both cases, after generating the code stubs,  a developer needs to reconnect the (delegated) business logic to 
the REST processing front end as required to get the system working again.  Developers can scrutinize recent working 
releases of the code to best understand how the code stubs need to be reconnected or how to add new business logic.
