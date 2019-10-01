### Richard Bruskiewich:
There is a code module, CTDwrapper.py
I imagine one or both of you know it
```
import requests

class CTDWrapper(object):
    def __init__(self):
        self.url = 'https://ctdapi.renci.org/'

    def gene2chem(self, gene_curie, params=None):
        call = '{0}CTD_chem_gene_ixns_GeneID/{1}/'.format(self.url, gene_curie)
        results = requests.get(call, params)
        return results.json()

    def chem2gene(self, chem_curie, params=None):
        call = '{0}CTD_chem_gene_ixns_ChemicalID/{1}/'.format(self.url, chem_curie)
        results = requests.get(call, params)
        return results.json()

```

just wondering 1) what are the valid identifiers for these two calls, 2) do you have 
some sample identifiers known to have the data in question in CTD?
Just trying to get a Translator module working which uses this code (it's a module 
someone else wrote.. seems straight forward, but just stuck guessing what kind 
of valid inputs these functions take... it's not documented ...)

### Steve Cox:

The best bet is to have a look at the CTD data dictionary here http://ctdbase.org/downloads/
It describes the kinds of identifiers that work. If you need more detail, the raw data files 
can be downloaded which will give you plenty of examples.

The CTD API is just a REST wrapper over those files.