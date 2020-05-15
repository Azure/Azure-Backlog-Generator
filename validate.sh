#!/bin/sh

for d in ./workitems/*/ ; do
    echo `main.py -t test --validate-only "$d"`
done