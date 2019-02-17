#!/usr/bin/env bash
mkdir builds

for D in repos; do
    if [ -d "${D}" ]; then
        echo "${D}"   # your processing here
    fi
done