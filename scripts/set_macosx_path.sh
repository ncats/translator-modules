#!/bin/bash
export PATH=$PATH$( gfind `pwd`/translator_modules/ -type d ! -name "__pycache__"  -printf ":%p" )
