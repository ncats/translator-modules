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

 ## Developer Addition or Modification of a System Service

We have specified the web services in OpenAPI 3.0 YAML specification files are found in each subdirectory 
- i.e. _identifiers_ and _ontology_ - related to each microservice. These subdirectories also have the corresponding 
client/server code in *client* and  *server* subfolders. For modifying one of the existing services, see the
relevant section in the corresponding READMEs, e.g. for  [the Identifier Resolution Service](./identifiers/README.md) 
and [the Ontology Jaccard Similarity service](./ontology/README.md).

If a novel service is required, use one of the existing services - including corresponding root project level
Dockerfile - to guide service development and inclusion of the new service into the Docker Compose deployment of the
Translator Module system.

[Back to top](#ncats-translator-module-project-components)
