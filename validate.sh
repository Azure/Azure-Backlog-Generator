#!/bin/sh

for d in ./workitems/*/ ; do
    echo `azbacklog -t test --validate-only "$d"`
done