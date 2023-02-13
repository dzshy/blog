#!/bin/bash

for f in $(find . -name '*title')
do
    opencc -i $f -o $f.tmp -c t2s.json
    mv $f.tmp $f
done
