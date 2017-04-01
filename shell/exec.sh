#!/usr/bin/env bash

set -e

SOURCE="${BASH_SOURCE[0]}"
# resolve $SOURCE until the file is no longer a symlink
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

cd "$DIR"
secrets=../../secrets.yaml

args_out=''
for ((i=2;i<=$#;i++)); do
  arg=${!i}
  if [[ $arg == secret:* ]]; then
    arg=$(parse_yaml.sh "$secrets" "${arg:7}")
  fi

  args_out="$args_out \"$arg\""
done

eval "./$1.sh ${args_out}"

