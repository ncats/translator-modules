# The Identifier Resolution Server

## Overview

This server was generated by the [OpenAPI Generator](https://openapi-generator.tech) project. By using the
[OpenAPI-Spec](https://openapis.org) from a remote server, you can easily generate a server stub.  This
is an example of building a OpenAPI-enabled Flask server.

This example uses the [Connexion](https://github.com/zalando/connexion) library on top of Flask.

## Requirements
Python 3.7+

## Usage

To run the server, it is recommended that you create a fresh Python virtual environment using Python 3.7, then
install the following dependencies.
 
First, the system generally needs to see the Python packages of the *ncats/translator* module tree. The (latest) 
package may not yet be in pypi, thus you will need to install the system locally as a pip installed library:

```bash
# The 'python' binary is assumed to be 3.7 or better
cd /path/to/translator-modules
python -m pip install -e .
```

Then,  you will specifically need the *identifiers* project dependencies. From within the *~/identifiers/server* 
directory, type the following:

```bash
# assuming that you are already in the translator-modules root directory
cd ncats/translator/identifiers/server
python -m pip install -r requirements.txt -e .
```

Using up a standalone version of the server is as simple as typing:

```bash
python -m openapi_server
```

and opening your browser to here:

```
http://0.0.0.0:8081/ui/
```

Your OpenAPI definition lives here:

```
http://0.0.0.0:8081/openapi.json
```

To launch the integration tests, use tox:

```
sudo pip install tox
tox
```

## Running with Docker

To run the server on a Docker container, from the root directory of the Translator Modules project, type the following:

```bash
# building the image
docker build -f Dockerfile_Shared -t translator_modules_shared .
docker build -f Dockerfile_Identifiers_Server -t identifier_resolution_server .

# starting up a container
docker run -p 8081:8081 identifier_resolution_server
```

Once again, opening your browser to here:

```
http://localhost:8081/ui/
```

should show the interface (same caveats as above).

## Running as an Integral Part of the Translator Module Workflow System (using Docker Compose)

See the [Translator Modules documentation](../../../../README.md) 
about how this service is run as a Docker Compose managed service within the Translator Modules Workflow system.