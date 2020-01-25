# Workflow ARA API

This document outlines a prototype query API for a NCATS Automated Reasoning Agent (ARA) which is initially assumed to 
be based on the [Reasoner Application programming Interface](https://github.com/NCATS-Tangerine/NCATS-ReasonerStdAPI).

## Building and Running the Server

The server may be run as a standalone application or within a Docker container. In this section, we assume direct 
execution as a standalone system (see below for Docker). After installing the project as per the 
[main README](./README.MD). 

There are two ways to run the system: directly as a standalone system or within a Docker container.

To install, test and run the server directly: 

```bash
make server-installation
make server-run
```

To build and start the server within a Docker container:

```bash
make server-build
make server-start
```

You can also use `make log` to see the docker containers logs, and `make stop` to stop the docker container.

## Updating the Reasoner API Specification

The Makefile may also be used to regenerate the code.

There is a `validation` target to check the project OpenAPI specifications, prior to regenerating the code:

```bash
make api-validation
```

The *validation* target calls a local shell script `generate.sh` in the root directory of the project.  This script 
checks for the presence of the OpenAPI Code Generator binary and attempts to install it if it is not yet installed 
on the computer. This installation may be problematic on some platforms (e.g. Microsoft Windows) but you can also 
[manually install the OpenAPI Code Generator](https://openapi-generator.tech/docs/installation). If you do this, 
you may need to override the OPENAPI_GENERATOR_CLI and OPENAPI_GENERATOR_CLI_PATH environment variables used by the 
generator script.  

Note also that the `openapi-generator-cli` script depends on  `mvn`, `jq` and `curl` to run (these dependencies
should be installed first).

Even on Unix-type systems, the `generate.sh` script installation of the OpenAPI Code generator may 
fail if not run as 'sudo' since the binary is being installed under _/usr/local/bin_, thus so you may need to run the 
above *validation* make target as `sudo` the first time, to ensure a successful installation (however, the 
installation processes does fix the execute permissions for general access, so 'sudo' should not be needed afterwards).
 
After installing the `openapi-generator` tool and validating the API's, the code may be (re-)generated:

```bash
make code-generation
```

### The Gory Details...

Ideally, the aforementioned `make` process should work but, just in case, we provide more details on the whole code 
generation procedure here below.

#### The OpenAPI specifications

Refer to the [Python Flask server](./server) implementation of the Reasoner API wrapper of the KBA with 
a corresponding [Python client](./client).  

#### (Re-)Generating the Server and Client

The *client* is a direct Python web service client and the *server* is a simple Python Flask server implementation.

The implementation of the Workflow ARA API server and client uses code generation from the 
[OpenAPI 3.* NCATS Reasoner API specification](./reasoner_api/API/TranslatorReasonersAPI.yaml), 
which is used as a template to generate the code base, which is then wired up by delegation to additional handler code.   
 
The generated and other client/server code is found in the *client* and  *server* subfolders.

By [installing a local copy of the OpenAPI Code Generator](https://openapi-generator.tech/docs/installation), 
modified OpenAPI 3.0 YAML specifications can be processed to recreate the Python client and Python Flask server stubs.
Note that depending on how you install the OpenAPI Code Generator, the manner in which you execute the 
 `openapi-generator` command below will change accordingly (Note that the code generation processes are a bit more 
 streamlined and robust under Linux and OSX than Microsoft Windows).

The code generation commands are generally run from the root project directory directory.  First, one should check 
your new or modified OpenAPI YAML specifications using the _validate_ command:

```bash
openapi-generator validate (-i | --input-spec=)reasoner_api/API/TranslatorReasonersAPI.yaml
```

If the specifications pass muster, then to recreate the Python Flask *server* stubs, the following command may 
be typed from within the root directory:

```bash
openapi-generator generate --input-spec=reasoner_api/API/TranslatorReasonersAPI.yaml \
                    --output=server \
                    --generator-name=python-flask \
                    --package-name=ara_server \
	                --model-package=models \
	                --artifact-version=0.9.2 \
	                --additional-properties=\
"projectName=workflow_ara_server,packageName=ara_server,packageVersion=0.9.2,packageUrl=https://github.com/ncats/translator-modules/master/server,serverPort=8080"
```

and to recreate the KBA *client* Python access stubs, something along the lines of the following command is typed:

```bash
openapi-generator generate  --input-spec=reasoner_api/API/TranslatorReasonersAPI.yaml \
                    --output=client \
                    --generator-name=python \
                    --package-name=ara_client \
	                --model-package=models \
	                --artifact-version=0.9.2 \
	                --additional-properties=\
"projectName=workflow_ara_client,packageName=ara_client,packageVersion=0.9.2,packageUrl=https://github.com/ncats/translator-modules/tree/master/client"
```

The [OpenAPI 3.0 'generate' command usage](https://openapi-generator.tech/docs/usage#generate) may be consulted
for more specific details on available code generation options and for acceptable program flag abbreviations (here we
used the long form of the flags).

The above commands are also wrapped inside of a `generate.sh` shell script in the root project directory and 
may also be invoked using the provide Makefile targets.

#### Repairing the Generated Code

In both cases, after generating the code stubs, a developer likely needs to repair the regenerated code a bit.

First, the code stubs must be reconnected to the (delegated) business logic to the REST processing front end as 
required to get the system working again.  Developers can scrutinize recent working releases of the code to 
best understand how the code stubs need to be reconnected or how to add new business logic.

Also, the *server* and *client* subdirectory _README.md_ file are overwritten by the code generation. 
These should be restored from the \*-master.\* versions of these files in each directory.
 
Finally, check if the `server/ara_server/__main__.py` file has the correct Identifiers server port (8080).

For good measure, after such extensive rebuilding of the libraries, the 'pip' environment dependencies should also 
be updated, as documented for the client and server, prior to re-testing and using the updated software.
