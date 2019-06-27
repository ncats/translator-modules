#### TODO
* Have `biocwl.py` perform an "empty run" against `cwl-runner` -- if no schema, return an empty type all the way through
* Create CWL types corresponding to NCATS domain
* Use CWL types inside of `*.cwl` specs

## Setting up a new CWL Module

### Placing modules on the path

In order to use the CWL specs in `biocwl/workflows/`, one must put the modules in `translator_modules/modules<*>/` on the system path.

This lets your CWL Runner use these modules by identifying them on the absolute path, and also lets the codebase be portable across systems
when not using a virtual machine like Docker.

One way to do this (not recommended) is by adding `translator_modules` onto the system path directly. Only do this if you trust the codebase.

```bash
export PATH=$PATH$( find $LOCATION/$OF/$PROJECT/translator-modules/translator_modules/ -type d -printf ":%p" )
```

By default, each translator module should have `#!/usr/bin/python3` as their specified interpreter, written at the top of the file.

Additionally, ensure that each module is kept executable by performing `chomd a+x *` within `translator_modules`.

Finally, if you are developing on Windows, ensure that you are enforcing Unix-style newlines in these files.
You can do this using a tool like `dos2unix`, or by running the Vim command `set: fileformat=unix` on the file.

Our CWL specs can now be kept terse, as they don't require an absolute path to access them nor a python call to run them, like so.

```cwl
#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ module0.py, get-data-frame, to-json ]
```

#### TODO

* Replace current path strategy with use of GNU `stow`