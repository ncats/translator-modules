# TranslatorCWL

Get started immediately by **[using TranslatorCWL](#using-translatorcwl).**

For the justification of this project, find out **[How TranslatorCWL works](#how-translatorcwl-works).**

If you want to take Translator Modules and bring them into CWL, see **[Writing a CWL tool for an existing module](#writing-a-cwl-tool-for-an-existing-module).** *(Requires an intermediate understanding of Python 3, including how the class system works.)*

An introduction to Common Workflow Language can be found on the **[CWL website](https://www.commonwl.org).**

# Using TranslatorCWL

## Quickstart

### Prerequisites

* Since CWL runs its code inside Docker modules, [install Docker](#installation-of-docker).  It is recommended that 
you commit to running this CWL workflow on a *nix system (Linux, Mac OSX or VM equivalent) since Docker for Windows 
tends to be a bit more problematic to operate than its counterparts on Linux and OSX.

* The system is currently validated to work only with Python 3.7 or better.  We therefore recommend the installation 
of a **virtualenv** to enforce this:

``` 
virtualenv -p python3.7 py37
source py37/bin/activate
```

or, alternately, use **conda env** to manage packages and the development environment:

```
conda create -n translator-modules python=3.7
conda activate translator-modules
```

* Next you install CWL engine:

```bash
python -m pip install cwltool
```

* Finally, follow the instructions for [preparing the workflow modules for use](#preparing-the-workflow-modules-for-use). 
Note in particular the general need to put the modules on your path (if you don't set this up automatically
for all your shell sessions, you'll need to set the PATH up for each new terminal session within which you
wish to run the CWL workflows)

### Running the CWL Workflow

#### NCATS Translator Workflow 2

You can run a CWL workflow constructed to implement the NCATS Translator Workflow 2.
In the project directory, run

```bash
cwltool cwl/workflows/wf2/wf2.cwl test/data/fanconi.yaml
```

A series of JSON files marked "module*.records.json" will contain the output of the run.

If you can run `wf2.cwl` with `fanconi.yaml` successfully,
* You have just run a CWL tool.
* You have just used multiple modules chained together at once.
* You have replicated the NCATS Translator Workflow 2 [Fanconi Anaemia Tidbit]().

#### NCATS Translator Workflow 9

Similarly, a CWL workflow can be run which executes (a portion of(*)) the NCATS Translator Workflow 9, as follows:


```bash
cwltool cwl/workflows/wf9/wf9_for_genes.cwl test/data/bicluster/yaml/input_genes.yaml
```

Result files **gene_to_gene_bicluster.records.json** and **gene_to_tissue_bicluster.records.json** will be outputted.

Similar additional workflow 9 CWL scripts are alongside this one, which take tissue, phenotype and disease identifiers, 
taking analogous input (YAML) files and outputting analogous (JSON) result files.

## Alternate CWL Workflow Data Exchange Formats

The **\*\_rl.cwl** files in the **result_list** subdirectories for each workflow are rewritten to use the 
new **ResultList** JSON format (see core data_transfer_model.py); the cwl files in the core workflow subdirectories,
lacking the **\_rl** infix, use the legacy **Pandas DataFrame** JSON for data sharing.

# Full CWL Installation & Configuration

## Installation of Docker

Follow the [Docker installation instructions](https://docs.docker.com/engine/installation/) in your target operating 
system environment. For example, if you use Ubuntu Linux, there is an [Ubuntu-specific docker installation using the repository](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-using-the-repository).

Note that you should have 'curl' installed first before installing Docker:

```
$ sudo apt-get install curl
```

For other installations, please find instructions specific to your choice of operating system, on the Docker site.

In order to ensure that docker is working correctly, run the following command:

```
$ sudo docker run hello-world
```

This should result in the following output:
```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
ca4f61b1923c: Pull complete
Digest: sha256:be0cd392e45be79ffeffa6b05338b98ebb16c87b255f48e297ec7f98e123905c
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://cloud.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/engine/userguide/
```

If you are running the system under Linux, there are some 
[post-installation configuration](https://docs.docker.com/install/linux/linux-postinstall/) 
which you can apply so that Docker can be run directly without sudo.

## Preparing the Workflow Modules for Use

By default, each translator module should have `#!/usr/bin/env python3` specified at the top of the module, as their 
specified interpreter, written at the top of the file (Note: double check if your system has tagged Python 3 as the
executable *python3*. If not, you should probably add a *python3* symbolic link to resolve to the actual interpreter).

Additionally, ensure that each module is kept executable by performing `chmod a+x *` within `translator_modules`.

Finally, if you are developing on Windows, ensure that you are enforcing Unix-style newlines in these files.
You can do this using a tool like `dos2unix`, or by running the Vim command `set: fileformat=unix` on the file.

For the system to run, you will now need to 
[install the Python dependencies for the translator-modules project](../README.md#installation-of-dependencies).

In order to use the CWL tools in `cwl/workflows/`, one must then put those `translator_modules/modules<*>/` modules 
on the system path.  This lets your CWL Runner use these modules by identifying them on the absolute path, and lets 
the codebase be portable across systems if you are not using a virtual machine.

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

Our CWL specs can now be kept terse, as they don't require an absolute path to access them nor a python call to run 
them, like so.

```yaml
#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ disease_associated_genes.py, get-data-frame, to-json ]
```

## Running a CWL tool

### CWL File

CWL tools are not scripts, but blueprints for running scripts. They let users clarify beforehand the kinds of data they 
should expected for a script: names for the data, their types and formats, and what arguments they satisfy. 
Let's take a simple example:

```yaml
cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ disease_associated_genes.py, get-data-frame, to-json, --orient, records ]
inputs:
  disease_name:
    type: string
    inputBinding:
      prefix: --input-disease-name
  disease_id:
    type: string
    inputBinding:
      prefix: --input-disease-mondo
outputs:
  disease_list:
    type: stdout
stdout: disease_associated_genes.records.json
```

This is `cwl/workflows/disease_associated_genes.cwl` wrapping `translator_modules/disease_associated_genes.py`. All CWL tools for Translator Modules share this
structure. We will run `disease_associated_genes.py` with inputs given by `disease_name` and `disease_id`, corresponding to the flags 
`--input-disease-name`, and `--input-disease-mondo`, which are the names of variables inside the module. 
The tokens `get-data-frame to-json --orient records` make `disease_associated_genes.py` return a list of JSON records; see 
[exposing your module to the command line](#exposing-your-module-to-the-command-line) for details.

### Data File

If CWL is a blueprint, what makes it real? Inputs to CWL tools are YAML files that share the same keywords as the tool's
inputs. For `disease_associated_genes.cwl`, this means we want a YAML file with `disease_name` and `disease_id`, 
like in `test/data/fanconi.yaml`:

```yaml
disease_name: "FA"
disease_id: "MONDO:0019391"
```

**Running a CWL tool uses the following command:**
```bash
cwltool <translator cwl tool> <file with keywords matching the tool's inputs>
```

And taken together, it means that this UNIX command:

```bash
disease_associated_genes.py --inputs-disease-name "FA" --input-disease-mondo "MONDO:0019391" get-data-frame to-json --orient records
```

Is *equivalent to* **this CWL tool running Translator Module 0:**

```bash
cwltool cwl/workflows/disease_associated_genes.cwl test/data/fanconi.yaml
```

## Writing a CWL tool for an existing module

To make the magic happen, there are a few standard practices needed to obeyed by developers seeking to turn a Translator
Module, into a TranslatorCWL tool. **Note:** This section is undergoing changes while an optimal approach is sought for developing workflow modules.

### Exposing your module to the command line

The NCATS ecosystem contains a diverse array of APIs and resources, which means that sometimes information which is
conceptually similar, might only be accessible in irregular ways, or come in heterogenuous formats.

As such, the way we get information ought to be decoupled from the way we view information. Consumers shouldn't have to solve these problems: they should ask for information in the simplest way possible, and find it 
easy to transform data however they like.

Our answer to this requirement is to ask modules to use a class called `Payload` to help turn the module into a command line tool.
This involves the following:

* Extend the `Payload` class with a constructor that takes workflow parameters (e.g. `disease_id`, `input_genes`, 
`threshold`...) as its arguments;
* Finding a way to expose these arguments to the command line (such as with [Python Fire](https://github.com/google/python-fire));
* Transform the module's results into a [Pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html);
* Use `Payload`'s accessor methods to return output in TranslatorCWL tools.

The most important accessor is just `get_data_frame`, returning the `Payload`'s results. Otherwise, what matters is how we shape the `Payload`'s constructor.

Here is an example of these modifications in `translator_modules/module1/module1a.py`. This class, `FunctionallySimilarGenes`, is defined at the bottom of the file, underneath `FunctionalSimilarity`.

```python
from translator_modules.core.module_payload import Payload
import fire

class FunctionallySimilarGenes(Payload):

    def __init__(self, input_genes, threshold, file=False):
        super(FunctionallySimilarGenes, self).__init__(FunctionalSimilarity('human'))

        if file:
            with open(input_genes) as stream:
                # assuming it's JSON and it's a record list
                input_gene_set = pd.read_json(stream, orient='records')
        else:
            gene_ids = [gene.gene_id for gene in input_genes]
            symbols = [attribute.value for gene in input_genes for attribute in gene.attributes if attribute.name == 'gene_symbol']
            genes = {"hit_id": gene_ids, "hit_symbol": symbols}
            input_gene_set = pd.DataFrame(data=genes)

        self.results = self.mod.compute_similarity(input_gene_set, threshold)

if __name__ == '__main__':
    fire.Fire(FunctionallySimilarGenes)
```

The constructor takes two arguments, 'input_genes' and `threshold`, which will correspond to flags and prefixes in
the CWL tool. These are the only two parameters required to run `compute_similarity`, which is 
Module1A's primary function.

Both `self.results` and `self.mod` are fields of `Payload`: the value of `self.mod` is equal to the initialized module
`FunctoinalSimilarity('human')` that was passed in to the super-constructor. By returning `self.mod.compute_similarity()`
into `self.results`, the accessor methods do not have to guess where their results are going to be.

#### DIY

Let's say you want to do this for your own module. If exposing your own module to the command line, you need to guarantee that it's on the path and executable ([see here](#placing-modules-on-the-path)).

After you've ensured that your module is executable, add the following to the bottom of its script:

```python
from translator_modules.core.module_payload import Payload
import fire
import pandas as pd

class <ModuleOutputName>(Payload):
    def __init__(self, workflow, args, go, here):
        super(<ModuleOutputName>, self).__init__(<ModuleClassName>())
        self.result = _<result_procedure>(workflow, args, go, here)
        
    def _<result_procedure>(self, workflow, args, go, here):
        delegated_results = self.mod.<results_giving_function>()
        pandas_dataframe_results = pd.DataFrame(delegated_results)
        return pandas_dataframe_results

if __name__ == '__main__':
    fire.Fire(<ModuleOutputName>)
```

The code above will obviously not interpret correctly: it is meant to illustrate the general strategy for exposing modules.

The names within the triangular brackets `< >` don't matter except by the content they describe. Just remember that ModuleClassName
means the class of the module this code is pasted in, and ModuleOutputName means actual biological content being returned by the module.

`_<result_procedure>` is private because it only should ever be run as many times as the entire object is called during the workflow,
else the object is not behaving like a function or command. So there's no need to expose it to the user.

#### Why output JSON?

JSON is a lingua franca format on the web, you can represent objects with it (including Biolink objects), it's the format 
that many schema standards like OWL and JSON-LD expect to be handling other than YAML or XML. CSV is preferable for researchers though. Some thinking on how to go from JSON to tables in a nice way will need to be done.

#### Why use Pandas DataFrames inside scripts?

DataFrames are powerful objects that can be built from several formats, and output several formats. As such it is 
adequate to represent information in DataFrames when you have many serialization formats within the ecosystem that need 
to be handled regularly. They will also be flexible enough to handle our changing understanding of what formats are needed for 
SMEs and application developers.

#### Why Python Fire?

Fire makes it simple to expose any Python class to the command-line, in only **two lines of code**. This means it is easy for
maintainers to add command-line functionality to modules, and it's easy to delete Fire if we change our minds about the approach.

It does have limitations: complex arguments (like mutually exclusive yet simultaneously required arguments) are not supported.
And you can't pipe commands with it, although you can compose the functions of a single module easily.

An argument can be made for moving to `argsparse` instead, or even eliminating the need to expose modules in this way, as
 the CWL ecosystem does support tool generation from Python files under various conditions.

### Creating the CWL tool file

Going through the [Common Workflow Language User Guide](https://www.commonwl.org/user_guide/), we often end up with files that look like this:

```yaml
cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ myModule.py, get-data-frame, to-json, --orient, records ]
inputs:
  disease_name:
    type: string
    inputBinding:
      prefix: --input-disease-name
outputs:
  my_module_output:
    type: stdout
stdout: myModule.records.json
```

As your module should be on the path by now, we can put it inside of `baseCommand` given that this CWL tool has `CommandLineTool` 
as its `class`.

Using Python Fire or equivalent, you should be exposing the object extending the `Payload` class in your module's 
script, rather than the module class itself. Thus we can use `get-data-frame to-json --orient records` to call out the results of 
your module as a list of JSON records.

The `type` for given `inputs` correspond to JavaScript types. For Python, `float`, `int`, and `string` have common-sense 
equivalents. A list in Python becomes an `array` here, and a dict in Python becomes a `record`. You *can* have complex types, 
constructed by nesting `type: <datatype>` pairs in the YAML entry. There are also `File` types, referring to complex or custom 
types and their `formats`. None are used by the project thusfar.

There doesn't have to be a correlation between the names under `inputs` and the `prefixes`, but the `prefixes` have to match
the names of your `Payload` object's arguments in its constructor. Likewise, the names under `outputs` do not matter, but for
`stdout` the file name ought to be consistent with the format given by the `baseCommand`. 

**Note:** this might change in future iterations.

### Testing the tool

Just run it:

```bash
cwltool <your cwl file> <your data file>
```

## Combining multiple CWL tools

`wf2.cwl` in `cwl/workflows` is an example of combining multiple CWL tools (taking a subset of `wf2.cwl`). Here is a part of it:

```yaml
cwlVersion: v1.0
class: Workflow
inputs:
    disease_name: string
    disease_id: string
    threshold:
      type: float
      default: 0.75
outputs:
  functionally_similar_genes:
    type: File
    outputSource: functional_similarity/functionally_similar_genes
steps:
  diseases:
    run: disease_associated_genes.cwl
    in:
      disease_name: disease_name
      disease_id: disease_id
    out: [ disease_list ]

  functional_similarity:
    run: functional_similarity.cwl
    in:
      input_genes: diseases/disease_list
      threshold: threshold
    out: [ functionally_similar_genes ]
```

It is like creating a large CWL tool out of smaller ones. Like in a simple CWL tool, you need `inputs` and `outputs` to 
be specified. Multiple tools are used together by linking the outputs of one tool, into the inputs of another.

For instance, the tool `diseases` runs `disease_associated_genes.cwl`, that outputs a `disease_list`, which we address specifically in the 
property `out`.  We place `disease_list` into `functional_similarity`'s inputs by referencing what it is and where it came 
from, `diseases/disease_list`, and placing it as the value of the relevant input, `input_genes`.

A similar process is performed with the final results of `m0_m1.cwl`, where the output of `module1a.cwl` is connected to
former's outputs, by writing `outputSource: functional_similarity/functionally_similar_genes`.

Sometimes, your inputs cross-cut among many tools: it might be useful to set a `default` value like we did
with `threshold`, so we don't have to put so many arguments into our input file, or re-use the input file of 
an existing script. So this:

```yaml
disease_name: "FA"
disease_id: "MONDO:0019391"
```

Or this:

```yaml
disease_name: "FA"
disease_id: "MONDO:0019391"
threshold: 0.35
```

... are both valid input files.

Note that the order in which modules are run, depends solely on when one tool has finished computing the required data 
for another. Thus `module1a.cwl` runs after `disease_associated_genes.cwl` because of `diseases/disease_list` being referenced as an input.

Also note that there can be multiple outputs: you don't need to generally receive the results of one script, but can list
out the results of each script if necessary.

# How TranslatorCWL Works

## What's the point?

Each Translator Module acts as your data source for biomedical concepts from NCATS. Getting lists of genes is as simple 
as downloading the module from PyPI, and importing it into a Python script or Jupyter notebook for immediate use.

However, these Python scripts can be "brittle" or "inconsistent": these modules rely on the rest of the script to handle their 
results in a way that can be re-used by other modules, and NCATS gives no guarantee of this. Notebooks - excellent tools 
for finding and explaining results - do not compose into larger systems, which makes these results difficult to build upon.

This is the problem that TranslatorCWL hopes to improve.

### Chaining

*Tested*

Sometimes you don't need to use just one module: you need several. However, to string modules together requires a guarantee
that each module's outputs can be transformed to the formats required for the next module's inputs.

### Recombination

*Tested*

Additionally, sometimes you only need some modules, or the number of modules you are using changes. If there is a single Python script that used
all the modules, you would need to either comment them all out then comment them back in, or add feature flags to manage their execution.

This is cumbersome. With the approach in TranslatorCWL, files are much smaller and chaining modules is simpler, so it is at least
less cumbersome to construct workflows of different orders and sizes.

### Paralellism

*Untested*

This same properties that let modules be combined in any order, also let you run them in parralel (to "scatter" them).

Since certain modules tend to feature long-running queries, one ought to be able to let modules that can provide data independently, run separately, to save time.
Where it would be a headache to do implement this in a Python script, you can tell the CWL tool to do it just by adding a couple of lines of text to its spec.

### Portability

*Untested*

CWL's capacity to run in Docker environments eliminates the need to worry about system compatibility when it comes to running
workflows, and should be able to streamline the ability to run Translator Modules across platforms, if you're a user instead 
of a developer.

### Validation

*Untested*

The final benefit is that CWL can integrate with the BiolinkML standard remotely. By ensuring the Biolink Model is used throughout, you can have 
confidence that the data you're getting will be usable by other tools in NCATS, and refer to concepts in your domain of expertise.

## How do I use it? How do I write a new CWL tool?

See [Using TranslatorCWL](#using-translatorcwl).

## Is this *the* Common Workflow Language?

TranslatorCWL acts as the next logical step towards a "common language" for NCATS Translator. With a couple exceptions 
(given below), it encodes the same properties as the [configuration shown in this presentation](https://docs.google.com/presentation/d/19ieHAN-6DLvfRUR0WqCokiJTTfuA6TPL9GHbf5UENUs/edit#slide=id.g4201216ac9_0_38). 
In principle you can do anything a bash script would do, but now you can set it up with less mental hassle, run it with 
less worry about whether it will work on your computer, get Biolink data, and share your solution with others remotely 
either as a script or as its own data-source.

Nonetheless, it has certain drawbacks. 

### Could the interface be simpler?

CWL buys us [the advantages mentioned above](#whats-the-point). But it still requires [some boilerplate](#exposing-your-module-to-the-command-line) to set up, in the form of module wrappers, input files, and specs for the tools themselves. 
This boilerplate still features concepts and terminology which are more relevant to a developer or bioinformatician, than a "subject matter expert" (SME).

In an ideal situation, assuming that SMEs know the *kind* of information they seek, they should write queries in terms of biological entities rather than workflow chains. 
Ensuring the terms used in CWL workflows conform to the Biolink Model helps, but more work may be required to achieve the simplicity of, say, GraphQL syntax. 

Could we have something as simple as:

```graphql
{
    expand { 
      similarity(level: phenotype, threshold: 0.75) {
        disease(name: "FA") -> gene {
            id
        }
    }
}
```

On the other hand, the CWL ecosystem has tools like [Rabix](https://github.com/rabix/composer) that eliminate
text via their GUI, which would be a win for SMEs as long as developers take care of the tooling.

### Are these tools expanders and sharpeners?

It's currently implicit whether or not a module counts as a sharpener, expander, or set-theoretic operation. Therefore we 
would still rely on developers to obey a convention somewhere to make sure that expanders are actually expanders, sharpeners
are sharpeners, and everyone knows this, including perhaps the workflow and its users.

Options to treat these operations as concepts that can be validated, need to be explored.

### Do workflows correspond to the Biolink Model?

#### TODO check this against orange team biolink experts
In theory: any mapping from one concept to another, if not mediated by any other mapping, ought to be a `slot` within the 
Biolink model. Thus each module, if not each workflow, ought to correspond to a slot or a set of slots.

The correspondence seems to break with meta-data. For example, although the addition of scores to slots like `blw:macromolecular machine 
to biological process association` seems natural, `score` is (currently?) not a coordinate for a slot. As such, `score` is only a property of the 
slot *given the module computing it*, rather than its meaning being determined by the slot itself. It therefore depends on the module's
developers to ensure their interpretation of `score` is consistent with everyone else's.

This issue is not necessarily one to be handled by TranslatorCWL - it's a question of what role we want the ontology to 
play in the project. Even if we want all data to be closed under Biolink types, CWL could only enforce what's already in 
a given schema. It would be up to the modules to do adequate conversions.

In lieu of this, we rely on developer convention to give proper names to the inputs and outputs of CWL scripts, which
we shouldn't necessarily hinder in the case where the Biolink Model can't close over the computations *in principle*, but 
should attempt to bolster with the validator *whenever possible* to prevent inevitable mistakes and stop the Tower of Babel 
from bifurcating further.

## TODO
* Refactor `Payload` in `Module1a`, `Module1b` properly
* Rename `Payload` to something better
* Find better nomenclature for modules than "module< number >"
  * Can it be related to their biological content in some way? Lets us anticipate the kinds of modules ahead of time
  * Do all modules adhere to [the standard](https://docs.google.com/presentation/d/19ieHAN-6DLvfRUR0WqCokiJTTfuA6TPL9GHbf5UENUs/edit)?
* Create CWL types corresponding to NCATS domain
* Use BiolinkML types inside of `*.cwl` specs
* Replace current path strategy with use of GNU `stow`
* Revise input/outputs formats of BioCWL tools with Biolink Types
* Enforce types with formats in CWL spec
* Move away from Python Fire to leverage other CWL tools that can autogenerate workflows
* Is the approach of using intermediary files the correct one?

## Wishlist
* What further relations might make sense between `.cwl` and `.py`?
  * Is there a translator workflow spec lurking between both of them? (i.e. the role of the input object as payload, or spec)
  * Should one enforce the types of the other?
  * Could a CWL workflow be solved from a Biolink Model specification that chains together against e.g. the SmartAPI registry?
  * Would this buy us anything?
