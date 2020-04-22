# NCATS Translator Modules

This package provides a (Python-based) implementation of various NCATS Translator bioinformatics workflow modules.

- [Getting Started](#getting-started)
    - [Getting and Configuring the Project](#getting-and-configuring-the-project)
    - [Installation of Dependencies and Making Modules Visible as Command Line Programs](#installation-of-dependencies-and-making-modules-visible-as-command-line-programs)
    - [Special Prerequisites for Running the Translator Modules: Utility Web Services](#special-prerequisites-for-running-the-translator-modules-utility-web-services)
        - [Running the Utility Web Services](#running-the-utility-web-services)
        - [Accessing the Utility Web Services run on the NCATS Cloud](#accessing-the-utility-web-services-run-on-the-ncats-cloud)
        - [Resolving Utility Web Service Host Names](#resolving-utility-web-service-host-names)
        - [Building and Running the Utility Web Services as Docker Containers](#building-and-running-the-utility-web-services-as-docker-containers)
        - [Directly Running the Utility Web Services](#directly-running-the-utility-web-services)
- [Using the Translator Modules and Building Workflows](#using-the-translator-modules-and-building-workflows)
    - [1. Workflows in Jupyter Notebooks](#1-workflows-in-jupyter-notebooks)
    - [2. Running Complete Workflows in Custom Python Scripts](#2-running-complete-workflows-in-custom-python-scripts)
    - [3. Running Workflow Modules individually from the Command line](#3-running-workflow-modules-individually-from-the-command-line)
    - [4. Running Translator Workflows using Common Workflow Language Specifications](#4-running-translator-workflows-using-common-workflow-language-specifications)
    - [5. Calling the Code Directly in your own Python Clients](#5-calling-the-code-directly-in-your-own-python-clients)
        - [Workflow 2 Gene Similarities and Interactions](#workflow-2-gene-similarities-and-interactions)
    - [6. Running the Translator Module System with Docker (Compose)](#6-running-the-translator-module-system-with-docker-compose)
 - [Future Directions](#future-directions)

# Getting Started

The software in this project has been (and may largely continue to be run) in various ways, enumerated below in the
section [Using the Translator Modules and Building Workflows](#using-the-translator-modules-and-building-workflows).

However, as of October 2019, the simplest way to run this application may now be as a Docker container based system, is 
now  detailed [here](#6-running-the-translator-module-system-with-docker-compose). In fact, some duplicate computations 
in the workflows have been offloaded to REST web services, which are easily provisioned and run within Docker containers 
(although, of course, with a bit more care and effort, may also be run without Docker). This web service are described 
in [Special Prerequisite for Running the Translator Modules](\special-prerequisite-for-running-the-translator-modules).

That said, a more hands-on "classical" approach to getting started, is described in the next subsection below.

## Getting and Configuring the Project

The **translator-modules** package is not yet available through PyPI, thus, to install, clone this repo using git.

```bash
git clone --recursive https://github.com/ncats/translator-modules.git

# ... then  enter  into your cloned project repository
cd translator-modules
```

Note the use of the *recursive* flag to include defined submodules of the project (in this case, the  Reasoner API).

The code is now validated to work only with Python 3.7 only.  We recommend using a **virtualenv** to enforce this.

```
virtualenv -p python3.7 venv
source venv/bin/activate
```

or, alternately, use **python venv** to manage packages and the development environment:

```
python3.7 -m venv venv
source venv/bin/activate
```

To exit the environment, type:

```  
deactivate
```

To reenter, source the _activate_ command again.

Alternately, you can also use use **conda env** to manage packages and the development environment:

```
conda create -n translator-modules python=3.7
conda activate translator-modules
```

Some IDE's (e.g. PyCharm) may also have provisions for directly creating such a **virtualenv**. This should work fine.

## Installation of Dependencies and Making Modules Visible as Command Line Programs

Make sure that your pip version is 3.7 compliant. It is also a good idea to ensure that you have the latest version of 
pip for your venv:

```
python -m pip install --upgrade pip
```

Then, run the following command within the `translator_modules` directory:

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

## Special Note (April 22, 2020)

A Pandas bug interfering with the CLI of the `translator-modules` module code was (eventually) fixed but is awaiting 
formal release to the community. For the moment, the patch is in the *master* branch of Pandas and may be applied by:

```
python -m pip install git+https://github.com/pandas-dev/pandas@master#egg=pandas
```

This extra step may be obsoleted once Pandas 1.0.4 (or better) is released.

## Utility Service Dependencies

The current version of the NCATS Translator Modules library now outsources some of its computations to specialized 
utility web services, which must be visible before many of the modules will properly work.

At this time, there are two such utility web services:

- *Identifiers Resolution Service:* performance maps  (mostly gene) identifiers in between namespaces
- *Jaccard Similarity Service:* manages an _in memory_ copy of ontology catalogs for Jaccard Similarity computations

Most of the modules, when given _incomplete or incompatible identifiers_, will try to access the *Identifiers* server 
to resolve such identifiers; the *Functional Similarity*  and *Phenotype Similarity* modules need to access 
the *Jaccard* server. Those modules will fail to execute otherwise.

The Translator Modules software accesses these utility web services using Python client libraries which have 
some module dependencies that should be installed. From the _translator-modules_ directory, you need to change 
directory into the respective clients and install these dependencies, as follows:

```bash
cd ncats/translator/identifiers/client
python -m pip install -r requirements.txt -e .
cd ../../../../ncats/translator/ontology/client
python -m pip install -r requirements.txt -e .
cd ../../../..  # back to the translator-modules root directory
```

## Running the Utility Web Services

There are three ways of ensuring that such web services are available and visible to the system (in their recommended 
order of preference):

1. Accessing an available online utility web service endpoints
2. Running the utility web services inside a Docker container
3. Directly running the utility web services on your workstation (outside Docker)

### Accessing the Utility Web Services run on the NCATS Cloud

The system default configuration is (as of January 2020) to access the online web services running on a cloud 
server hosted by NCATS (for the moment).  Unless overridden with the setting of suitable environment variables (see 
[Service Host Name Resolution](#service-host-name-resolution) below), the default endpoints of those external web 
services are hardcoded to be the following (as the time of this writing):

- *Identifiers resolution service:* https://kba.ncats.io/module/identifiers
- *Ontology ("Jaccard") web service:* https://kba.ncats.io/module/ontology

### Resolving Utility Web Service Host Names Run Elsewhere

With the default configuration noted above, the endpoints (as long as NCATS runs them!) are automatically visible to 
a default installation of the Translator Modules system... no further configuration should be required.

To run the Translator Modules from _inside_ a Docker container (see below), one needs to point to the services using 
two environment variables (here, we show the `bash` way of doing this. The exact manner in which environment variables 
are declared and made visible also  differs between operating systems and Integrated Development Environments (IDEs). 
Consult your documentation to find out how to properly set them):

```bash
export IDENTIFIERS_RESOLUTION_SERVER_HOST="http://identifiers:8081"
export JACCARD_SIMILARITY_SERVER_HOST="http://jaccard:8082"
```

Note the distinct port numbers for the two microservices.

In contrast, to run the Translator Modules from _outside_ a Docker container (see below), one needs to point to the 
services as if they are published by `localhost`. This is the case irrespective if the utility services themselves are 
run from within a Docker container or directly on the machine (see below).

```bash
export IDENTIFIERS_RESOLUTION_SERVER_HOST="http://0.0.0.0:8081"
export JACCARD_SIMILARITY_SERVER_HOST="http://0.0.0.0:8082"
```

If you want the flexibility of running the utility web services inside Docker containers (using Compose - see below) but 
 running the Translator Modules themselves either either inside or outside Docker containers, you can set the 
 environmental variables as for _inside_ Docker operation (above) then also set the docker-compose service names 
 (i.e. "identifiers" and "jaccard") can also be recorded in your operating system `hosts` configuration file 
 as resolving to 127.0.0.1 ("localhost"). That is, add the following lines into the `hosts` file:

```bash
127.0.0.1   identifiers
127.0.0.1   jaccard
```

The file is found at the path */etc/hosts* under Linux and Mac OSX; on Windows, look for it at 
*:wq*).  Recording this `hosts` setting will ensure that, for example, 
CWL run workflows will find the microservices even when run from outside of a Docker container.

### Building and Running the Utility Web Services as Docker Containers

Although you can [run both web services directly on a workstation](#directly-running-the-utility-web-services), 
the easiest option is to run them as Docker containers.  Assuming the necessary Docker and Compose software are properly 
installed, building and running the required microservices involves typing in following commands, from within 
the project root directory:

```
docker-compose build
docker-compose up --detach identifiers jaccard
```

This will fire up the microservices inside their corresponding Docker containers, for access by the rest of the system. 

Note that a basic concern relating to some of the web services is memory management (primarily, of the *Jaccard* 
web service, which caches a significant portion of GO terms into memory and is empirically observed to require 
about 5GB to run) will be Docker-imposed container RAM limits. On Linux, this limit defaults to "all of memory" thus, 
memory intensive services will likely have enough memory on a decent sized machine; however, the Docker for Mac and 
Docker for Windows variants impose stricter limits, usually about 2.0 GB. This limit may be reset manually through 
the Docker Desktop resource in the Docker Desktop Preferences.. dialog. At the time of this writing, a setting of at 
least 3 GB is needed to run the Jaccard on the Mac. Users on Macs can see https://docs.docker.com/docker-for-mac/ for 
details about how to adjust the maximum container memory 'Resource' using Docker for Mac Desktop Preferences dialog 
(invoked from the in context popup menu of the Docker Desktop icon seen at the top right hand corner of the menu bar). 
The "Advanced" settings for Docker for Windows Desktop preferences provide similar facilities (see 
https://docs.docker.com/docker-for-windows/).
 
Interestingly, the Jaccard service running in a guest Ubuntu Linux VM running on a Windows 10 machine, requires over 
4.77 GB of RAM to run fully loaded with ontology. One conjectures that Mac and Linux have very distinct memory models!

### Directly Running the Utility Web Services

The utility web services may also be run directly outside Docker. For this purpose, additional Python dependencies need 
to be installed. It is highly recommended that each web service its own virtual environment within which to install its 
Python dependencies and be run, to avoid Python library version clashes with the main Translator Module system. After 
activating their respective `venv`, the dependencies then the software may be run within a fresh command line terminal:

```
# from the root project directory
virtualenv -p python3.7 identifiers-venv
source identifiers-venv/bin/activate
(identifiers-venv): cd ncats/translator/identifiers/server
(identifiers-venv): python -m pip install --no-cache-dir -r requirements.txt
(identifiers-venv): python -m openapi_server
```

and in a second fresh command line terminal:

```
# from the root project directory again
virtualenv -p python3.7 ontology-venv
source ontology-venv/bin/activate
(ontology-venv): cd ncats/translator/ontology/server
(ontology-venv): python -m pip install --no-cache-dir -r requirements.txt
(ontology-venv): python -m openapi_server
```

[Back to top](#ncats-translator-modules)

# Using the Translator Modules and Building Workflows

The modules in this repository may be composed into larger scientific workflows, managed by suitable software 
frameworks. A number of execution frameworks for doing this have been explored to date within NCATS:

1. Jupyter Notebooks
2. Complete workflows can scripted
3. Workflow modules may be run individually from the command line (see below)
4. Using the Common Workflow Language (CWL) standard
5. Roll your own: call workflow modules from your own clients

Note again that most of these options run the code "externally to docker" thus if they use the current code base, it 
will necessary to take the _identifier resolution_ and _Jaccard similarity_ microservices into account, both by setting 
the \*SERVER_HOST environment variables then firing them up, generally using using *docker-compose* (although in 
principle, with some careful systems administrative effort, the services could be run in a non-docker configuration). 

[Back to top](#ncats-translator-modules)

## 1. Workflows in Jupyter Notebooks

See https://github.com/ncats/translator-workflows for numerous examples. The compatibility of classical Jupyter 
notebook  versions of the workflows has not been tested against the new micro  services noted above.

[Back to top](#ncats-translator-modules)

## 2. Running Complete Workflows in Custom Python Scripts

### Usage

A sample Python 3 command line script [WF2_automation.py script](./scripts) is currently provided that will directly 
execute the relevant modules and commands for the *NCATS Translator Workflow 2*.
  
To display the full parameters of the script, type:

```
./scripts/WF2_automation.py --help
```

A folder named  *Tidbit* will contain the results as HTML and JSON files. The latter (JSON) files include
an extra column called "shared_terms" which is the list of the intersection set of ontology terms identified during 
Jaccard scoring of the functional (GO term) or phenotype (HP term) overlap of the input gene list with the other 
genes listed in the given row.

When the '--verbose' flag is used, the script also echos tabular results to the standard output ("console").

A similar script is in the works for Translator 
[Workflow 9](https://www.lucidchart.com/documents/edit/22689882-2099-4acb-961a-fa6202f2cfd8/0_0).


The script (as are the modules) are marked up with the "hash bang ("#!") Unix script comment at the top so generally
if marked as executable, may be run directly as above, but in some environments (e.g. Windows) you may need to 
explicitly run them as a Python script, i.e.

```
python scripts/WF2_automation.py --help
```

[Back to top](#ncats-translator-modules)

## 3. Running Workflow Modules individually from the Command line

Assuming that you have [properly configured things](#installation-of-dependencies-and-make-modules-visible-as-command-line-programs), 
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

In fact, all the various Pandas DataFrame output methods are available (see the
[Pandas IO docs](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html#serialization-io-conversion)).

Just substitute the 'to-json' and 'to-csv' method command keywords with your chosen target format (e.g. to-excel, etc.)

An alternate "ResultList" JSON output forma, which is more complete with additional annotation and the Biolink model 
metadata, may be generated as follows:

``` 
gene_interaction --input-genes "HGNC:1100,HGNC:12829" get-result-list to-json       
```

This Translators-specific JSON format is mainly to empower interoperability of the modules with one another and with 
other Translator tools. A sample version of it (from a  'functional similarity' run) may be found 
[here](https://github.com/ncats/translator-modules/blob/master/docs/functional_similarity.json) 
(Hint: use the FireFox web browser for a convenient view of this JSON). The Python code defining and 
manipulating the "ResultList" module data model is in the module 
[data_transfer_model.py](https://github.com/ncats/translator-modules/blob/master/translator_modules/core/data_transfer_model.py).

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

More information about the modules are found [here](./ncats/translator/modules).

## 4. Running Translator Workflows using Common Workflow Language Specifications

See the [Translator CWL workflow scripts and documentation](./cwl)

[Back to top](#ncats-translator-modules)

## 5. Calling the Code Directly in your own Python Clients

Review of the available workflow scripts (e.g. for workflow  2 and  9) provides some guidance on how to use the modules
directly. You can also directly review the modules themselves.  As an example, we discuss here the Workflow 2 modules.

[Back to top](#ncats-translator-modules)

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

[Back to top](#ncats-translator-modules)

## 6. Running the Translator Module System with Docker (Compose)

With this "cutting edge" option, we use the [Docker Container Technology](https://www.docker.com) to simplify 
packaging and running of the Translator workflows. 

After [installing the necessary Docker and Docker Compose dependencies](DOCKER_README.md), type the following 
into the terminal to build and run the system. Note that 'identifiers' and 'jaccard' are two REST microservices running 
inside their own containers, and providing utility services to the primary module code.

```
cd translator-modules
docker-compose build
docker-compose up --detach identifiers jaccard
docker volume create --name mydata
docker run -i --rm  --network translator-modules_ncats -v mydata:/results  --name workflows translator-modules_workflows
```

The last `docker run` command starts up a workflow container shell, connected to associated micro service  
containers on a local bridge network.  

The second to last command creates a persistent docker data volume called 
'mydata' which is then bound to the *workflows* container. This volume can be used to persistent your workflow results 
for later access by other containers or externally.  Details about the volume (including its host machine location) 
may be viewed by typing: 

```bash
docker volume inspect mydata
```

See the [Docker Storage Volume Documentation](https://docs.docker.com/storage/volumes/) for 
more information.

Note that the *workflows* container run command shell doesn't give a prompt but you can type in Linux commands 
(e.g. `ls`) to convince yourself that it is running.  The last command above activates the virtual CLI environment 
within which Translator module scripts may be directly executed. For example, you can try running the following:

```
disease_associated_genes --disease-identifier "MONDO:0005361" get-data-frame to-csv >/results/disease_genes.json
```
retrieves genes associated with the disease "eosinophilic esophagitis", in a json stored in the results volume.

Common Workflow Language (CWL) workflows may also be run inside the container, for example:

```bash
cwltool cwl/workflows/wf2/result_list/wf2_rl.cwl tests/data/fanconi.yaml
```

In this case, "ResultList" JSON formatted files with a *.json* file extension will contain the output of the run.

**Note:** If the docker-compose commands are is giving you trouble, try running them as the system administrator with 
the `sudo` command. Remember, though, that if you are running  your commands as 'sudo', then depending on how your 
OS instance configures sudo, in some cases, $HOME may actually be '/root' or it may otherwise still be in your 
normal user home.

The REST API should now be running at http://localhost: on ports 8081 and 8082, the OpenAPI web interface at 
http://localhost:<port#>>/api/ui. You can open your browser with these addresses to see these applications in action.

More details about the architecture of the system is available on the 
[modules documentation overview page](./ncats/translator).

[Back to top](#ncats-translator-modules)

# Query API for a "Next Generation" NCATS Automated Reasoning Agent (ARA) 

We are prototyping a  NCATS development phase ARA to further automate the NCATS workflows. Information about this 
effort is currently under development in its own README [here](./ARA_README.md).

[Back to top](#ncats-translator-modules)

# Future Directions

We are implementing a simple (CWL) graphical user interface (GUI) on top of a (CWL?) workflow runner, to 
facilitate user interaction with the system. We also aspire to wrap the system in some fashion with the emerging 
Translator "Reasoner API"  REST computing access standard, to facilitate programmatic access to the workflows. Finally,
we'd like to add more biologically interesting modules and workflows to the existing collection, such as analysing 
post-translational modification (PTM) biology.

[Back to top](#ncats-translator-modules)
