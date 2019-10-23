# Ontology Jaccard Similarity Service

This subproject implements a client/server version of the Ontology-driven Jaccard Simiilarity computation as
a REST API driven client/server service, run either standalone or within a Docker Container.

Refer to the Ontology Jaccard Similarity computation
 [Python Flask server](./server)
 implementation documentation and the corresponding
[Python client](./client) is
 documentation for details about such usage of the system.  

### (Re-)Generating the Server and Client
 
The implementation of the identifiers client/server system uses code generation from an 
 [OpenAPI 3.* Identifiers Resolution API specification](./ncats_translator_module_ontology_api.yaml), 
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
openapi-generator validate (-i | --input-spec) ncats/translator/ontology/ncats_translator_module_ontology_api.yaml
```

If the specification passes muster, then to recreate the Python Flask *server* stubs, the following command may 
be typed from within the root directory:

```bash
openapi-generator generate --input-spec=ncats/translator/ontology/ncats_translator_module_ontology_api.yaml \
                    --model-package=model \
                    --output=ncats/translator/ontology/server \
                    --generator-name=python-flask \
                    --additional-properties="\
--packageName=ncats.translator.ontology.server.openapi_server,\
--projectName=jaccard-similarity-server,\
—-packageVersion=\"0.0.1\",\
--packageUrl=https://github.com/ncats/translator-modules/tree/master/ncats/translator/ontology/server,\
--serverPort=8082"
```

To recreate the matching *client* Python access stubs, something along the lines of the following command is typed:

```bash
openapi-generator generate  --input-spec=ncats/translator/ontology/ncats_translator_module_ontology_api.yaml \
                    --model-package=model \
                    --output=ncats/translator/ontology/client \
                    --generator-name=python \
                    --additional-properties="\
--packageName=ncats.translator.ontology.client.openapi_client,\
--projectName=jaccard-similarity-client,\
—-packageVersion=\"0.0.1\",\
--packageUrl=https://github.com/ncats/translator-modules/tree/master/ncats/translator/ontology/client"
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
*ncats.translator.ontology.client.* to *openapi_client* prefixed packages. Also,  in the  _api_client.py_ module, 
an code embedded *openapi_client.model*  client package name is best repaired by adding the full package prefix *and* 
importing the root *ncats* package by itself, i.e.

``` 
import ncats
```
plus to add imports of all the model classes inside the client *model* ```__init__.py```  package level file.

Also, the *server* and *client* subdirectory _README.md_ and _setup.py_ files are overwritten by the code generation. 
These should be restored from the \*-master.\* versions of these files in each directory.
 
Finally, check if the `server/openapi_server/__main__.py` file has the correct Jaccard server port (8082).
 