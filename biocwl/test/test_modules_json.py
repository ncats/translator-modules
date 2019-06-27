from translator_modules.module0.module0 import DiseaseAssociatedGeneSet
from translator_modules.module1.module1a import FunctionallySimilarGenes
import yaml
from pathlib import Path

THRESHOLD = 0.01
TAXON = 'human'

def test():
    dataDir = Path('../data/inputs/')
    with open(dataDir / Path('fa.yaml'), 'r') as stream:
        d = yaml.safe_load(stream)

        dags = DiseaseAssociatedGeneSet(d['disease_name'], d['disease_id'])

        dags_results = dags.get_data_frame().to_json()

        fsg = FunctionallySimilarGenes(dags_results, THRESHOLD, 'human')

        print(fsg.get_data_frame())

test()