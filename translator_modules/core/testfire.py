#!/usr/bin/env python3

import fire
if __name__ == '__main__':
    fire.Fire(lambda obj: type(obj).__name__)