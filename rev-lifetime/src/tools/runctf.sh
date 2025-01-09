#!/bin/bash

set -e
set -x

python3 compile_ctf_to_c.py $1 $1.c
gcc $1.c -o $1.exe
./$1.exe