#  NCATS Translator Module Project Components

This package aggregates project code specifically related to the 
[NCATS Biomedical Data Translator Project](https://ncats.nih.gov/translator).

In particular, this Github repository manages Python code packages integrating into an implementation of 
Translator bioinformatics computational workflows. These packages are enumerated here.

## core

[Shared code modules](./core)

## identifiers

[Identifier Resolution Service](./identifiers) 
providing mechanisms for retrieving equivalent identifiers (and related metadata) across distinct namespaces.

## ontology

[Ontology](https://github.com/ncats/translator-modules/tree/docker-compose-system/ncats/translator/ontology) catalog 
access services, used by some Translator Modules such as the 
[functional_similarity and phenotype_similarity modules](./modules/gene/gene/README.md)

## modules

[Translator Modules](./modules).

[Back to top](#ncats-translator-module-project-components)

# Translator Module Workflow System Services

Running the latest version of the  Translator Modules ecosystem involved conversion of some components of the system to 
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

[Back to top](#ncats-translator-module-project-components)

## Identifiers Resolution Service

The [Identifiers Resolution Service](https://github.com/ncats/translator-modules/tree/docker-compose-system/ncats/translator/identifiers) 
provides an API for translating concept identifiers from one namespace to another.
The initial implementation focuses on gene identifiers (e.g. HGNC identifiers to gene symbols, Ensembl, NCBIGene, etc.)

[Back to top](#ncats-translator-module-project-components)

## Ontology Lookup Service

This [Ontology Lookup Service](https://github.com/ncats/translator-modules/tree/docker-compose-system/ncats/translator/ontology) 
is still under development.

[Back to top](#ncats-translator-module-project-components)

## Developer Modification of System Service APIs or Addition of New Services

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

[Back to top](#ncats-translator-module-project-components)
