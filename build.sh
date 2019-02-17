#!/usr/bin/env bash
mkdir builds
for SOURCE in repos/*; do
    if [ -d "${SOURCE}" ]; then
        DESTINATION=${SOURCE/repos/builds}
        (cd ${SOURCE}; bundle install; bundle exec jekyll build; mv _site ../../${DESTINATION})
    fi
done