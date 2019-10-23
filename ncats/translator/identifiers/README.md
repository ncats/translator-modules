# Identifier Resolution Module v0.2.0

## Command Line Usage

To use the resolution service easily from the command line, you need to configure the environment, From within the 
Translator Modules project root directory, type the following:

```  
python -m pip install -e .
```

The usage of the  system as a script may be seen by:

```bash
identifier_resolver --help
```


For a batch translation of identifiers, for example, run the  script From the command line as follows:

```bash
identifier_resolver --identifier-map "absolute_or_relative/path/to/HUGO_geneids_download_v2.txt" \
--source "Ensembl Gene ID" --target "HGNC ID" \
load-identifiers --identifiers ../../tests/data/bicluster/csv/gene_list.csv   translate
```

Note: when being given `--identifiers`, it looks for a column equivalent to the name of the ID namespace 
(like "Ensembl Gene ID" or "HGNC ID").

Inputting a simple list of identifiers, instead of a CSV file path should also work.

```bash
identifier_resolver --identifier-map "absolute_or_relative/path/to/HUGO_geneids_download_v2.txt" \
--source "Ensembl Gene ID" --target "HGNC ID" \
load-identifiers --identifiers \
"ENSG00000121410,ENSG00000268895,ENSG00000148584,ENSG00000070018,ENSG00000175899,ENSG00000245105" translate
```

## Calling Identifier Resolution Directly from a Python Script

```python
from ncats.translator.identifiers.server.resolver import Resolver

ids = ["ENSG00000121410", "ENSG00000268895", "ENSG00000148584", "ENSG00000070018", "ENSG00000175899", "ENSG00000245105"]

resolver = Resolver.get_the_resolver()
resolver.directly_load_identifiers(ids)
converted_ids = resolver.translate(target="HGNC_ID")

print(converted_ids)
```

You should get something like this:

```
['ENSG00000121410', '']
['ENSG00000268895', 'HGNC:37133']
['ENSG00000148584', 'HGNC:24086']
['ENSG00000070018', 'HGNC:6698']
['ENSG00000175899', 'HGNC:7']
['ENSG00000245105', 'HGNC:27057']
['ENSG00000166535', 'HGNC:23336']
['ENSG00000256661', 'HGNC:41022']
['ENSG00000256904', 'HGNC:41523']
['ENSG00000256069', 'HGNC:8']
['ENSG00000234906', 'HGNC:609']
['ENSG00000068305', 'HGNC:6993']
['ENSG00000070018', 'HGNC:6698']
```

Which you can now manipulate in other programs.

Note that the available conversion 'target' keys may be listed using the Resolver call:

```python
from ncats.translator.identifiers.server.resolver import Resolver
resolver.list_identifier_keys()
```

The above example uses a default identifier map. Another identifier map may be substituted in the resolver (see the 
Python module code for details; in essence, your JSON tags or text/csv column  headers will be the conversion keys)

```python
from ncats.translator.identifiers.server.resolver import Resolver
..
identifier_map = "absolute/path/to/your/identifier_map.txt"
resolver = Resolver(identifier_map)
..
```

## Identifiers Resolution run as a REST Web Service (Perhaps using Docker)

The Identifiers Resolution is also run as a REST Web Service, either standalone or within a Docker Container.

Refer to the Identifiers Resolution
 [Python Flask server](./server)
 implementation documentation and the corresponding
[Python client](./client) is
 documentation for details about such usage of the system.  

### (Re-)Generating the Server and Client
 
The implementation of the identifiers client/server system uses code generation from an 
 [OpenAPI 3.* Identifiers Resolution API specification](./ncats_translator_module_identifiers_api.yaml), 
 which is used as a template to generate the code base, which is then wired up by delegation to additional
 handler code.  These generated and other client/server code is found in the *client* and  *server* subfolders. 
 The *client* is a direct Python web service client and the *server* is a simple Python Flask server implementation.

By [installing a local copy of the OpenAPI Code Generator](https://openapi-generator.tech/docs/installation), 
modified OpenAPI 3.0 YAML specifications can be processed to recreate the Python client and Python Flask server stubs.

The code generation commands are generally run from the *translator-modules* directory:

```bash
cd translator-modules
```

First, one should check new or modified OpenAPI YAML specifications using the _validate_ command:

```bash
openapi-generator validate (-i | --input-spec) ncats/translator/identifiers/ncats_translator_module_identifiers_api.yaml
```

If the specification passes muster, then to recreate the Python Flask *server* stubs, the following command may 
be typed from within the root directory:

```bash
openapi-generator generate --input-spec=ncats/translator/identifiers/ncats_translator_module_identifiers_api.yaml \
                    --model-package=model \
                    --output=ncats/translator/identifiers/server \
                    --generator-name=python-flask \
                    --additional-properties="\
--packageName=ncats.translator.identifiers.server.openapi_server,\
--projectName=identifier-resolver-server,\
—-packageVersion=\"0.0.1\",\
--packageUrl=https://github.com/ncats/translator-modules/tree/master/ncats/translator/identifiers/server,\
--serverPort=8081"
```

To recreate the matching *client* Python access stubs, something along the lines of the following command is typed:

```bash
openapi-generator generate  --input-spec=ncats/translator/identifiers/ncats_translator_module_identifiers_api.yaml \
                    --model-package=model \
                    --output=ncats/translator/identifiers/client \
                    --generator-name=python \
                    --additional-properties="\
--packageName=ncats.translator.identifiers.client.openapi_client,\
--projectName=identifier-resolver-client,\
—-packageVersion=\"0.0.1\",\
--packageUrl=https://github.com/ncats/translator-modules/tree/master/ncats/translator/identifiers/client"
```

The [OpenAPI 3.0 'generate' command usage](https://openapi-generator.tech/docs/usage#generate) may be consulted
for more specific details on available code generation options and for acceptable program flag abbreviations (here we
used the long form of the flags)

# Repairing the Generated Code

In  both cases, after generating the code stubs, a developer needs to repair the regenerated code a bit.

First, the code stubs must be reconnected to the (delegated) business logic to 
the REST processing front end as required to get the system working again.  Developers can scrutinize recent working 
releases of the code to best understand how the code stubs need to be reconnected or how to add new business logic.

Generally, the nature of the *ncats.translator.* package structure can cause some runtime failures in import resolution 
within the client generated code stubs. The solution seems to be to add the package prefixes 
*ncats.translator.identifiers.client.* to *openapi_client* prefixed packages. Also,  in the  _api_client.py_ module, 
an code embedded *openapi_client.model*  client package name is best repaired by adding the full package prefix *and* 
importing the root *ncats* package by itself, i.e.

``` 
import ncats
```
plus to add imports of all the model classes inside the client *model* ```__init__.py```  package level file.

Also, the *server* and *client* subdirectory _README.md_ and _setup.py_ files are overwritten by the code generation. 
These should be restored from the \*-master.\* versions of these files in each directory.
 
Finally, check if the `server/openapi_server/__main__.py` file has the correct Identifiers server port (8081).

For good measure, after such extensive rebuilding of the libraries, the 'pip' environment dependencies should also 
be updated, as documented for the client and server, prior to re-testing and using the updated software.
