#!/usr/bin/env python3

import pandas as pd
import fire

from translator_modules.wf9.util.bicluster_disease_to_phenotype import BiclusterByDiseaseToPhenotype
from translator_modules.core import Payload


class DiseaseToPhenotypeBiclusters(Payload):

    def __init__(self, input_gene_list_file):
        super(DiseaseToPhenotypeBiclusters, self).__init__(BiclusterByDiseaseToPhenotype())

        curated_gene_list = \
            self.mod.run_getinput(input_gene_list_file)

        most_common_phenotypes = self.mod.disease_to_phenotype_biclusters(curated_gene_list)



        # data munging the output for the module
        from collections import defaultdict
        """
        def default_dict_convert(default_dict):
            temp_default_dict = dict(default_dict)
            for item1 in default_dict.keys():
                for item2 in default_dict[item1].keys():
                    if type(default_dict[item1][item2]) is type(defaultdict()):
                        temp_default_dict[item1][item2] = dict(default_dict[item1][item2])
                if type(default_dict[item1][item2]) is type(defaultdict()):
                    temp_default_dict[item1] = dict(default_dict[item1])
            return temp_default_dict
        """

        # dataFrame = pd.DataFrame.from_dict(default_dict_convert(most_common_phenotypes), orient="index")
        # dataFrame["gene_id"] = dataFrame.index  # turn the row index, which are currently gene ids, into a named column
        # self.results = dataFrame


if __name__ == '__main__':
    fire.Fire(DiseaseToPhenotypeBiclusters)
