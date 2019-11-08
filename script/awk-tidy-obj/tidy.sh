#!/bin/bash

cur_dir=$(pwd)
p_dir="$(dirname "$cur_dir")"

find $p_dir -type f -name 'names.py' > ./log.list
find $p_dir -type f -name '*.py' -not -name 'names.py' >> ./log.list
awk -f ./tidy.awk $(<log.list)
