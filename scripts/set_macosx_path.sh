#!/bin/bash
export PATH=$PATH$( gfind `pwd`/modules/ -type d ! -name "__pycache__"  -printf ":%p" )
