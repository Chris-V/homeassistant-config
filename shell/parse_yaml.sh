#!/usr/bin/env bash

# Returns a value form a yaml file.
# Inspired by: https://gist.github.com/pkuczynski/8665367

s='[[:space:]]*'
sed -ne "s|^$s\($2\)$s:$s\"\(.*\)\"$s\$|\2|p" -e "s|^$s\($2\)$s:$s\(.*\)$s\$|\2|p" $1

