#!/usr/bin/env python3

import json
import fire
from translator_modules.core.module_payload import Payload


class TranslateIDs(Payload):

    def convertIDs(self, input_ids, translations):
        translation_dict = dict(translations)
        converted_ids = list([(input_id, translation_dict.get(input_id)) for input_id in input_ids])
        return converted_ids

    def __init__(self, ids, translation, in_id, out_id):
        input_str, extension1 = self.handle_input_or_input_location(ids)
        translation_str, extension2 = self.handle_input_or_input_location(translation)

        self.ids: list
        # NB: push this out to the handle_input_or_input_location function?
        if extension1 == "csv":
            import csv
            with open(ids) as genes:
                input_reader = csv.DictReader(genes)
                self.ids = list([row[in_id] for row in input_reader])
        elif extension1 == "json":
            with open(ids) as genes:
                input_json = json.loads(genes)
                # assume records format
                self.ids = [record[in_id] for record in input_json]
        elif extension1 is None:
            if type(ids) is list:
                self.ids = input_str
            elif type(ids) is str:
                self.ids = input_str
            else:
                self.ids = None

        self.translation: list
        # NB: push this out to the handle_input_or_input_location function?
        if extension2 == "csv":
            import csv
            with open(translation) as genes:
                input_reader = csv.DictReader(genes)
                self.translation = list([(row[in_id], row[out_id]) for row in input_reader])
        elif extension2 == "json":
            with open(translation) as genes:
                input_json = json.loads(genes)
                # assume records format
                self.translation = [(record[in_id], record[out_id]) for record in input_json]
        elif extension2 is None:
            if type(translation) is list:
                self.translation = translation
            elif type(translation) is str:
                self.translation = translation_str
            else:
                self.translation = None

        self.results = self.convertIDs(self.ids, self.translation)


if __name__ == '__main__':
    fire.Fire(TranslateIDs)
