#!/bin/sh

for d in ./workitems/*/ ; do
    echo `azbacklog --validate-only "$d"`
done