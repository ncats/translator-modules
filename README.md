# Translator Modules

This package provides a Python-based implementation of the NCATS Translator service.

## Installation

**Note:** code has been tested with Python 3.7 only.

The **translator-modules** package is not yet available through PyPI. To install, clone this repo and run the following command within the `translator_modules` directory:

```
pip install -r requirements.txt .
```

## Development

We recommend using a **virtualenv** or **conda env** to manage packages and the development environment:

```
conda create -n translator-modules python=3.7
conda activate translator-modules
```

To install the package in "developer" mode (such that code changes are automatically reflected in the local library), include the `-e` flag with `pip`:

```
pip install -r requirements.txt -e .
```

## Usage

Running the command...

```
python scripts/WF2_automation.py
```

... will execute the relevant modules and commands for "workflow 2" and save results in a folder named `Tidbit`.



