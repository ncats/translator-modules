#!/usr/bin/env python3

import asyncio
import pandas as pd
import fire

import sys

from translator_modules.wf9.util.biclusterco import CoocurrenceByBicluster
from translator_modules.core import Payload


class GeneToGeneBiclusters(Payload):

    def __init__(self, input_gene_list_file):
        sys.settrace

        super(GeneToGeneBiclusters, self).__init__(CoocurrenceByBicluster())

        curated_gene_list = \
            self.mod.run_getinput(input_gene_list_file)

        # Most of WF9's modules are asynchronous
        # https://stackoverflow.com/a/53267521
        # https://stackoverflow.com/a/44048615

        loop = asyncio.get_event_loop()
        task = loop.create_task(self.mod.tissue_to_gene_biclusters_async(curated_gene_list))
        done, pending = loop.run_until_complete(asyncio.wait([task]))

        # data munging the output for the module
        from collections import defaultdict
        def default_dict_convert(default_dict):
            temp_default_dict = dict(default_dict)
            for item1 in default_dict.keys():
                for item2 in default_dict[item1].keys():
                    if type(default_dict[item1][item2]) is type(defaultdict()):
                        temp_default_dict[item1][item2] = dict(default_dict[item1][item2])
                if type(default_dict[item1][item2]) is type(defaultdict()):
                    temp_default_dict[item1] = dict(default_dict[item1])
            return temp_default_dict

        for future in done:
            print(future.result())
            # dataFrame = pd.DataFrame.from_dict(default_dict_convert(future.result()), orient="index")
            # dataFrame["gene_id"] = dataFrame.index  # turn the row index, which are currently gene ids, into a named column
            # self.results = dataFrame


if __name__ == '__main__':
    fire.Fire(GeneToGeneBiclusters)
