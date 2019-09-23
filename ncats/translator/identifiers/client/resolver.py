#!/usr/bin/env python3

from typing import List

import fire

class Resolver:
    """
    This class handles identifier conversions. Note that, for now, the 'identifier_map' catalog and the 'input_ids'
    need to have matching identifier formatting, in particular, with respect to xmlns (curie) prefixes.
    """
    _the_resolver = None

    @classmethod
    def get_the_resolver(cls):
        if not cls._the_resolver:
            cls._the_resolver = Resolver()
        return cls._the_resolver

    def __init__(self):
        """
        This is a constructor for a client to an actual server Resolver
        """
        self.input_identifiers = None

    def list_identifier_keys(self) -> List[str]:
        raise RuntimeError("Not yet implemented!")

    def load_identifiers(self, identifiers, source=None):
        raise RuntimeError("Not yet implemented!")

    def translate_one(self, source, target):
        raise RuntimeError("Not yet implemented!")

    def translate(self, target=None):
        raise RuntimeError("Not yet implemented!")


def main():
    fire.Fire(Resolver)


if __name__ == '__main__':
    main()